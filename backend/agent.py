"""Bucle agéntico real: modelo local -> MCP -> PostgreSQL -> modelo."""
import asyncio
import json
import time
import uuid
import httpx
from config import MODEL, OLLAMA_URL, SKILL_PATH, GROQ_API_KEY, USE_GROQ
from mcp_client import connect_mcp, call_tool

class AgentUnavailable(RuntimeError): pass

async def model_status():
    if USE_GROQ:
        return {'available':True,'model':MODEL,'provider':'Groq','paid_api':False}
    try:
        async with httpx.AsyncClient(timeout=3,trust_env=False) as client:
            response=await client.get(OLLAMA_URL+'/api/tags')
            response.raise_for_status()
            names=[m['name'] for m in response.json().get('models',[])]
            return {'available':MODEL in names,'model':MODEL,'provider':'Ollama local','paid_api':False}
    except (httpx.HTTPError,ValueError,KeyError):
        return {'available':False,'model':MODEL,'provider':'Ollama local','paid_api':False}

async def run_agent(question: str):
    request_id=str(uuid.uuid4())
    started=time.monotonic()
    evidence=[]
    messages=[{'role':'system','content':SKILL_PATH.read_text()}, {'role':'user','content':question}]
    try:
        async with asyncio.timeout(180):
            async with connect_mcp() as session:
                catalogue=await session.list_tools()
                allowed={t.name for t in catalogue.tools}
                tools=[{'type':'function','function':{'name':t.name,'description':t.description,'parameters':t.inputSchema}} for t in catalogue.tools]
                async with httpx.AsyncClient(timeout=120,trust_env=False) as client:
                    for step in range(5):
                        response=await client.post('https://api.groq.com/openai/v1/chat/completions' if USE_GROQ else OLLAMA_URL+'/api/chat',headers={'Authorization':'Bearer '+GROQ_API_KEY} if USE_GROQ else {},json=({'model':MODEL,'messages':messages,'tools':tools,'temperature':0,'max_completion_tokens':2048} if USE_GROQ else {
                            'model':MODEL,'messages':messages,'tools':tools,'stream':False,
                            'options':{'temperature':0,'num_ctx':8192,'num_predict':1200},'keep_alive':'10m'}))
                        response.raise_for_status()
                        payload=response.json()
                        message=payload['choices'][0]['message'] if USE_GROQ else payload['message']
                        messages.append(message)
                        calls=message.get('tool_calls') or []
                        if not calls:
                            if evidence:
                                return {'answer':message.get('content',''),'evidence':evidence,'request_id':request_id,
                                        'model':MODEL,'mode':'agente_groq' if USE_GROQ else 'agente_local','duration_seconds':round(time.monotonic()-started,2)}
                            if step<2:
                                messages.append({'role':'user','content':'Antes de responder, consulta una herramienta MCP relevante. No tienes cifras verificadas todavía.'})
                                continue
                            raise AgentUnavailable('El modelo no consultó herramientas. Reformula la pregunta o usa el informe de datos.')
                        if len(calls)>4 or len(evidence)+len(calls)>8:
                            raise AgentUnavailable('Se alcanzó el límite de herramientas de esta consulta.')
                        for call in calls:
                            name=call['function']['name']
                            args=call['function'].get('arguments',{})
                            if isinstance(args,str): args=json.loads(args)
                            if name not in allowed or not isinstance(args,dict):
                                raise AgentUnavailable('El modelo solicitó una herramienta no permitida.')
                            result=await call_tool(session,name,args)
                            evidence.append({'tool':name,'arguments':args,'result':result,'transport':'MCP stdio'})
                            messages.append({'role':'tool',**({'tool_call_id':call['id']} if USE_GROQ else {'tool_name':name}),'content':json.dumps(result,ensure_ascii=False)})
                    raise AgentUnavailable('El modelo no terminó dentro del límite de pasos. Consulta el informe de datos.')
    except AgentUnavailable:
        raise
    except Exception:
        raise AgentUnavailable('No se pudo completar la consulta. Comprueba que el proveedor del modelo y Supabase están disponibles; consulta el informe para aislar el problema.') from None

async def report(desde='2010-12-01',hasta='2011-12-09',pais=None):
    async with asyncio.timeout(75):
        async with connect_mcp() as session:
            params={'desde':desde,'hasta':hasta,'pais':pais}
            summary=await call_tool(session,'resumen_ventas',params)
            countries=await call_tool(session,'comparar_grupos',{**params,'dimension':'pais','limite':8})
            months=await call_tool(session,'comparar_grupos',{**params,'dimension':'mes','limite':20})
            return {'summary':summary,'countries':countries,'months':months,'mode':'informe_sql_via_mcp',
                    'tools':['resumen_ventas','comparar_grupos'],'transport':'MCP stdio'}
