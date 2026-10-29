// Inyección aislada: ejecuta el backend real con fetch/env de prueba. Nunca cambia secretos publicados.
import {createRequire} from 'node:module';
import {mkdtemp,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {resolve,join} from 'node:path';
import {pathToFileURL} from 'node:url';
import assert from 'node:assert/strict';
const root=resolve(process.env.BI_SOURCE_DIR||'web_publica');
const require=createRequire(join(root,'package.json'));const {build}=require('esbuild');
const dir=await mkdtemp(join(tmpdir(),'bi-fault-'));const output=join(dir,'route.mjs');
globalThis.TEST_ENV={SUPABASE_URL:'https://db.test',SUPABASE_PUBLISHABLE_KEY:'TEST_ONLY',GROQ_API_KEY:''};
await build({entryPoints:[join(root,'app/api/[...path]/route.ts')],outfile:output,bundle:true,platform:'node',format:'esm',plugins:[{name:'test-env',setup(b){b.onResolve({filter:/^cloudflare:workers$/},()=>({path:'env',namespace:'mock'}));b.onLoad({filter:/.*/,namespace:'mock'},()=>({contents:'export const env=globalThis.TEST_ENV;'}))}}]});
const {GET,POST}=await import(pathToFileURL(output));let failure='groq401';const calls=[];const results=[];
globalThis.fetch=async(input,init)=>{const u=String(input);calls.push(u);if(u.startsWith('https://site.test/'))return POST(new Request(u,init));if(u.startsWith('https://db.test'))return new Response('SUPABASE_TEST_PRIVATE_ERROR',{status:503});if(u.includes('api.groq.com'))return new Response('GROQ_TEST_PRIVATE_ERROR',{status:failure==='quota'?429:401});throw Error('Unexpected network call');};
async function check(name,path,body,expected){calls.length=0;const req=new Request('https://site.test'+path,body?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}:{});const r=await (body?POST:GET)(req);const text=await r.text();assert.equal(r.status,expected);assert.ok(!text.includes('TEST_PRIVATE_ERROR'));results.push({prueba:name,esperado:expected,obtenido:r.status,respuesta:JSON.parse(text),llamadas:calls.slice(),estado:'PASS',entorno:'inyección aislada, backend cloud real'});}
await check('Groq sin clave / proveedor401','/api/chat',{question:'Resume ventas de Francia'},503);
await check('Supabase no disponible','/api/audit?pais=France',null,503);
failure='quota';await check('Cuota Groq429','/api/chat',{question:'Resume ventas de Francia'},429);
await check('Sin coste supuesto','/api/scenario',{pais:'France'},422);
await check('Fuera de ámbito no llama proveedores','/api/chat',{question:'¿Qué tiempo hace hoy en Madrid?'},200);assert.equal(calls.length,0);
await check('DELETE no llama proveedores','/api/chat',{question:'DELETE FROM ventas_uci'},200);assert.equal(calls.length,0);
await writeFile('tests/auditoria_29/fallos_aislados.json',JSON.stringify(results,null,2));console.log(results.map(r=>r.prueba+': '+r.estado).join('\n'));await rm(dir,{recursive:true});
