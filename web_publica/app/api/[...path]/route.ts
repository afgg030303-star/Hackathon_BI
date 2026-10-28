import { env } from 'cloudflare:workers';
import { skill } from '../../../skill';
const settings=()=>env as unknown as Record<string,string>;
const model='openai/gpt-oss-20b';
const properties={desde:{type:'string',description:'Fecha ISO YYYY-MM-DD, por defecto 2010-12-01'},hasta:{type:'string',description:'Fecha ISO inclusiva, por defecto 2011-12-09'},pais:{type:['string','null'],description:'Nombre exacto en inglés, por ejemplo France; null para todos'}};
const catalogue=[
{name:'resumen_ventas',description:'Ventas positivas, cancelaciones e importe neto GBP. No beneficio.',inputSchema:{type:'object',properties,additionalProperties:false}},
{name:'comparar_grupos',description:'Ranking por importe neto descendente. País, producto o mes.',inputSchema:{type:'object',properties:{...properties,dimension:{type:'string',enum:['pais','producto','mes']},limite:{type:'integer',minimum:1,maximum:20}},additionalProperties:false}},
{name:'comprobar_calidad',description:'Recuento y calidad del dataset real completo.',inputSchema:{type:'object',properties:{},additionalProperties:false}}];
function validate(name:string,args:any){
 const tool=catalogue.find(t=>t.name===name); if(!tool||!args||Array.isArray(args)||typeof args!=='object')throw Error('Parámetros inválidos');
 for(const k of Object.keys(args))if(!(k in tool.inputSchema.properties))throw Error('Parámetros inválidos');
 for(const k of ['desde','hasta'])if(args[k]!==undefined && (typeof args[k]!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(args[k])||!Number.isFinite(Date.parse(args[k]))))throw Error('Fecha inválida');
 if((args.desde||'2010-12-01')>(args.hasta||'2011-12-09'))throw Error('Periodo inválido');
 if(args.pais!=null&&(typeof args.pais!=='string'||args.pais.length>80))throw Error('País inválido');
 if(args.dimension!==undefined&&!['pais','producto','mes'].includes(args.dimension))throw Error('Dimensión inválida');
 if(args.limite!==undefined&&(!Number.isInteger(args.limite)||args.limite<1||args.limite>20))throw Error('Límite inválido');
}
async function rpc(name:string,args:any){
 validate(name,args);const s=settings();
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
 if(u.pathname==='/api/report'&&req.method==='GET'){
 const p=Object.fromEntries(u.searchParams);validate('resumen_ventas',p);
 await mcpCall(u.origin,'initialize',{protocolVersion:'2025-03-26',capabilities:{},clientInfo:{name:'BI dashboard',version:'1.0'}});
 const summary=await tool(u.origin,'resumen_ventas',p),countries=await tool(u.origin,'comparar_grupos',{...p,dimension:'pais',limite:8}),months=await tool(u.origin,'comparar_grupos',{...p,dimension:'mes',limite:20});
 return Response.json({summary,countries,months,transport:'MCP Streamable HTTP'});
 }
 if(u.pathname==='/api/chat'&&req.method==='POST'){
 const raw=await req.text();if(raw.length>8192)return Response.json({detail:'Solicitud demasiado grande'},{status:413});
 const {question}=JSON.parse(raw);if(typeof question!=='string'||question.trim().length<3||question.length>1500)return Response.json({detail:'Escribe una pregunta de 3 a 1500 caracteres'},{status:422});
 const started=Date.now(),evidence:any[]=[],messages:any[]=[{role:'system',content:skill},{role:'user',content:question}];
 await mcpCall(u.origin,'initialize',{protocolVersion:'2025-03-26',capabilities:{},clientInfo:{name:'BI agent',version:'1.0'}});
 const tools=(await mcpCall(u.origin,'tools/list')).tools.map((t:any)=>({type:'function',function:{name:t.name,description:t.description,parameters:t.inputSchema}}));
 for(let step=0;step<5;step++){
 const r=await fetch('https://api.groq.com/openai/v1/chat/completions',{method:'POST',headers:{Authorization:'Bearer '+settings().GROQ_API_KEY,'Content-Type':'application/json'},body:JSON.stringify({model,messages,tools,temperature:0,max_completion_tokens:2048}),signal:AbortSignal.timeout(40000)});
 if(r.status===429)return Response.json({detail:'Groq ha alcanzado su cuota temporal. Espera y vuelve a probar; el panel de datos sigue disponible.'},{status:429});
 if(!r.ok)throw Error('El modelo no está disponible');const b:any=await r.json(),msg=b.choices[0].message;messages.push(msg);
 if(!msg.tool_calls?.length){if(evidence.length)return Response.json({answer:msg.content,evidence,model,duration_seconds:(Date.now()-started)/1000,mode:'agente_groq_cloud'});messages.push({role:'user',content:'Consulta una herramienta MCP antes de responder.'});continue;}
 if(evidence.length+msg.tool_calls.length>8)throw Error('Consulta demasiado extensa');
 for(const call of msg.tool_calls){const args=JSON.parse(call.function.arguments);const result=await tool(u.origin,call.function.name,args);evidence.push({tool:call.function.name,arguments:args,result,transport:'MCP Streamable HTTP'});messages.push({role:'tool',tool_call_id:call.id,content:JSON.stringify(result)});}
 }throw Error('Reformula la pregunta: se alcanzó el límite de pasos');
 }
 return Response.json({detail:'Ruta no disponible'},{status:404});
 }catch{return Response.json({detail:'No se pudo completar la consulta. Revisa los filtros o inténtalo de nuevo.'},{status:503});}
}
export const GET=route;export const POST=route;
