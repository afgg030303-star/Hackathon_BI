import { env } from 'cloudflare:workers';
import { skill } from '../../../skill';
import { enrichAudit, draftAudit, estimateScenario, groundedAnswer } from '../../../audit.mjs';
const settings=()=>env as unknown as Record<string,string>;
const model='openai/gpt-oss-20b';
async function completed(evidence:any[],answer:string,started:number){
 const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(skill)))).map(b=>b.toString(16).padStart(2,'0')).join('');
 return Response.json({answer,evidence,model,duration_seconds:(Date.now()-started)/1000,mode:'agente_groq_cloud',skill:{name:'auditar-ventas',source:'skills/auditar_ventas/SKILL.md',sha256:hash,loaded_as:'system_instructions',executed_procedures:evidence.map(e=>e.tool)}});
}
const properties={desde:{type:'string',description:'Fecha ISO YYYY-MM-DD, por defecto 2010-12-01'},hasta:{type:'string',description:'Fecha ISO inclusiva, por defecto 2011-12-09'},pais:{type:['string','null'],description:'Nombre exacto en inglés, por ejemplo France; null para todos'}};
const catalogue=[
{name:'resumen_ventas',description:'Ventas positivas, cancelaciones e importe neto GBP. No beneficio.',inputSchema:{type:'object',properties,additionalProperties:false}},
{name:'comparar_grupos',description:'Ranking por importe neto descendente. País, producto o mes.',inputSchema:{type:'object',properties:{...properties,dimension:{type:'string',enum:['pais','producto','mes']},limite:{type:'integer',minimum:1,maximum:20}},additionalProperties:false}},
{name:'auditar_anomalias',description:'Audita TODOS los grupos de países y productos; detecta netos negativos y cancelaciones elevadas con reglas explícitas. Devuelve acciones e hipótesis, no causas probadas.',inputSchema:{type:'object',properties,additionalProperties:false}},
{name:'redactar_borrador',description:'Audita los datos y redacta un borrador de email con acciones verificables. No envía correos.',inputSchema:{type:'object',properties,additionalProperties:false}},
{name:'estimar_escenario',description:'Simulación de resultado con coste supuesto explícito por el usuario. No es beneficio real. Solicitar porcentaje al usuario antes de usar.',inputSchema:{type:'object',properties:{...properties,coste_porcentaje:{type:'number',minimum:0,maximum:200}},required:['coste_porcentaje'],additionalProperties:false}},
{name:'comprobar_calidad',description:'Recuento y calidad del dataset real completo.',inputSchema:{type:'object',properties:{},additionalProperties:false}}];
class InvalidInput extends Error {}
function validate(name:string,args:any){
 if(name==='estimar_escenario'&&(typeof args?.coste_porcentaje!=='number'||!Number.isFinite(args.coste_porcentaje)||args.coste_porcentaje<0||args.coste_porcentaje>200))throw new InvalidInput('Coste inválido');
 const tool=catalogue.find(t=>t.name===name); if(!tool||!args||Array.isArray(args)||typeof args!=='object')throw new InvalidInput('Parámetros inválidos');
 for(const k of Object.keys(args))if(!(k in tool.inputSchema.properties))throw new InvalidInput('Parámetros inválidos');
 for(const k of ['desde','hasta'])if(args[k]!==undefined && (typeof args[k]!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(args[k])||!Number.isFinite(Date.parse(args[k]))||new Date(args[k]).toISOString().slice(0,10)!==args[k]))throw new InvalidInput('Fecha inválida');
 if((args.desde||'2010-12-01')>(args.hasta||'2011-12-09'))throw new InvalidInput('Periodo inválido');
 if(args.pais!=null&&(typeof args.pais!=='string'||args.pais.length>80))throw new InvalidInput('País inválido');
 if(args.dimension!==undefined&&!['pais','producto','mes'].includes(args.dimension))throw new InvalidInput('Dimensión inválida');
 if(args.limite!==undefined&&(!Number.isInteger(args.limite)||args.limite<1||args.limite>20))throw new InvalidInput('Límite inválido');
}
async function rpc(name:string,args:any){
 validate(name,args);const s=settings();
 if(name==='estimar_escenario'){const {coste_porcentaje,...period}=args;return estimateScenario(await rpc('resumen_ventas',period),coste_porcentaje);}
 if(name==='auditar_anomalias'||name==='redactar_borrador'){
 const r=await fetch(s.SUPABASE_URL+'/rest/v1/rpc/bi_audit',{method:'POST',headers:{apikey:s.SUPABASE_PUBLISHABLE_KEY,'Content-Type':'application/json'},body:JSON.stringify(args),signal:AbortSignal.timeout(20000)});
 if(!r.ok)throw Error('Auditoría no disponible');const data=enrichAudit(await r.json());return name==='redactar_borrador'?{...draftAudit(data),auditoria:data}:data;
 }
 const r=await fetch(s.SUPABASE_URL+'/rest/v1/rpc/bi_tool',{method:'POST',headers:{apikey:s.SUPABASE_PUBLISHABLE_KEY,'Content-Type':'application/json'},body:JSON.stringify({tool_name:name,tool_args:args}),signal:AbortSignal.timeout(20000)});
 if(!r.ok)throw Error('Supabase no pudo completar la consulta');return r.json();
}
async function mcp(request:Request){
 if(request.method!=='POST')return new Response(null,{status:405});
 const b:any=await request.json();
 if(b.id===undefined)return new Response(null,{status:202});
 let result:any;
 if(b.method==='initialize')result={protocolVersion:'2025-03-26',capabilities:{tools:{}},serverInfo:{name:'Auditor BI UCI',version:'1.0.0'}};
 else if(b.method==='ping')result={};
 else if(b.method==='tools/list')result={tools:catalogue};
 else if(b.method==='tools/call'){
  try{const data=await rpc(b.params?.name,b.params?.arguments||{});result={content:[{type:'text',text:JSON.stringify(data)}],structuredContent:data,isError:false};}
  catch{result={content:[{type:'text',text:'Consulta inválida o base de datos no disponible'}],isError:true};}
 }else return Response.json({jsonrpc:'2.0',id:b.id,error:{code:-32601,message:'Método desconocido'}});
 return Response.json({jsonrpc:'2.0',id:b.id,result});
}
async function mcpCall(origin:string,method:string,params:any={}){
 const r=await fetch(origin+'/api/mcp',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json, text/event-stream'},body:JSON.stringify({jsonrpc:'2.0',id:crypto.randomUUID(),method,params}),signal:AbortSignal.timeout(25000)});
 if(!r.ok)throw Error('MCP no disponible'); const b:any=await r.json();if(b.error||b.result?.isError)throw Error('La consulta MCP no pudo completarse');return b.result;
}
async function tool(origin:string,name:string,args:any){return (await mcpCall(origin,'tools/call',{name,arguments:args})).structuredContent;}
async function route(req:Request){
 const u=new URL(req.url);
 try{
 if(u.pathname==='/api/mcp')return await mcp(req);
 if(u.pathname==='/api/health')return Response.json({llm:{available:!!settings().GROQ_API_KEY,model,provider:'Groq'},database:'Supabase',transport:'MCP Streamable HTTP'});
 if(u.pathname==='/api/audit'&&req.method==='GET'){
 const p=Object.fromEntries(u.searchParams);validate('auditar_anomalias',p);
 await mcpCall(u.origin,'initialize',{protocolVersion:'2025-03-26',capabilities:{},clientInfo:{name:'BI audit',version:'1.0'}});
 const audit=await tool(u.origin,'auditar_anomalias',p);return Response.json({audit,draft:draftAudit(audit),transport:'MCP Streamable HTTP'});
 }
 if(u.pathname==='/api/scenario'&&req.method==='POST'){
 const p=await req.json();validate('estimar_escenario',p);return Response.json(await tool(u.origin,'estimar_escenario',p));
 }
 if(u.pathname==='/api/report'&&req.method==='GET'){
 const p=Object.fromEntries(u.searchParams);validate('resumen_ventas',p);
 await mcpCall(u.origin,'initialize',{protocolVersion:'2025-03-26',capabilities:{},clientInfo:{name:'BI dashboard',version:'1.0'}});
 const summary=await tool(u.origin,'resumen_ventas',p),countries=await tool(u.origin,'comparar_grupos',{...p,dimension:'pais',limite:8}),months=await tool(u.origin,'comparar_grupos',{...p,dimension:'mes',limite:20});
 return Response.json({summary,countries,months,transport:'MCP Streamable HTTP'});
 }
 if(u.pathname==='/api/chat'&&req.method==='POST'){
 const raw=await req.text();if(raw.length>8192)return Response.json({detail:'Solicitud demasiado grande'},{status:413});
 const {question}=JSON.parse(raw);if(typeof question!=='string'||question.trim().length<3||question.length>1500)return Response.json({detail:'Escribe una pregunta de 3 a 1500 caracteres'},{status:422});
 const normalized=question.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 if(/\b(delete|update|insert|drop|truncate|alter)\b/.test(normalized))return Response.json({answer:'No ejecuto escrituras ni SQL arbitrario. Solo puedo consultar agregados de ventas y preparar propuestas de acción.',evidence:[],mode:'rechazo_escritura',model,duration_seconds:0});
 if(/que tiempo hace|clima en|pronostico meteorologico|temperatura en/.test(normalized))return Response.json({answer:'Esa pregunta está fuera del ámbito del auditor. Puedo analizar ventas, cancelaciones, calidad de datos y escenarios de costes de UCI Online Retail; no consulto información meteorológica.',evidence:[],mode:'fuera_de_ambito',model,duration_seconds:0});
 const started=Date.now(),evidence:any[]=[],messages:any[]=[{role:'system',content:skill},{role:'user',content:question}];
 await mcpCall(u.origin,'initialize',{protocolVersion:'2025-03-26',capabilities:{},clientInfo:{name:'BI agent',version:'1.0'}});
 const tools=(await mcpCall(u.origin,'tools/list')).tools.map((t:any)=>({type:'function',function:{name:t.name,description:t.description,parameters:t.inputSchema}}));
 for(let step=0;step<5;step++){
 const r=await fetch('https://api.groq.com/openai/v1/chat/completions',{method:'POST',headers:{Authorization:'Bearer '+settings().GROQ_API_KEY,'Content-Type':'application/json'},body:JSON.stringify({model,messages,tools,temperature:0,max_completion_tokens:1200}),signal:AbortSignal.timeout(40000)});
 if(r.status===429)return Response.json({detail:'Groq ha alcanzado su cuota temporal. Espera y vuelve a probar; el panel de datos sigue disponible.'},{status:429});
 if(!r.ok)throw Error('El modelo no está disponible');const b:any=await r.json(),msg=b.choices[0].message;messages.push(msg);
 if(!msg.tool_calls?.length){if(evidence.length)return completed(evidence,groundedAnswer(evidence,msg.content),started);messages.push({role:'user',content:'Consulta una herramienta MCP antes de responder.'});continue;}
 if(evidence.length+msg.tool_calls.length>8)throw Error('Consulta demasiado extensa');
 for(const call of msg.tool_calls){const args=JSON.parse(call.function.arguments);const result=await tool(u.origin,call.function.name,args);evidence.push({tool:call.function.name,arguments:args,result,transport:'MCP Streamable HTTP'});messages.push({role:'tool',tool_call_id:call.id,content:JSON.stringify(result)});}
 if(evidence.some(e=>['auditar_anomalias','redactar_borrador'].includes(e.tool)))return completed(evidence,groundedAnswer(evidence,''),started);
 }throw Error('Reformula la pregunta: se alcanzó el límite de pasos');
 }
 return Response.json({detail:'Ruta no disponible'},{status:404});
 }catch(error){return Response.json({detail:error instanceof InvalidInput?'Parámetros inválidos: revisa fechas, país y límites.':'No se pudo completar la consulta. Revisa los filtros o inténtalo de nuevo.'},{status:error instanceof InvalidInput?422:503});}
}
export const GET=route;export const POST=route;
