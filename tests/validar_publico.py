"""Prueba reproducible contra URL pública; no necesita secretos. Consume 2 consultas Groq."""
import asyncio,csv,gzip,json,os
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
ROOT=Path(__file__).resolve().parents[1]
URL=os.getenv('BI_TEST_URL','https://observatorio-retail-bi.balmyspark1.chatgpt.site')
results=[]
def check(name,expected,observed,ok):
 results.append(dict(prueba=name,esperado=expected,observado=observed,estado='PASS' if ok else 'FAIL'))
 print(name,results[-1]['estado'],flush=True)
async def main():
 groups=defaultdict(lambda:[Decimal(0),Decimal(0),Decimal(0)])
 france=[Decimal(0),Decimal(0),Decimal(0)];rows=0
 with gzip.open(ROOT/'data/ventas_uci.csv.gz','rt') as f:
  for r in csv.DictReader(f):
   rows+=1;q=Decimal(r['quantity']);p=Decimal(r['unit_price']);a=q*p;cancel=r['invoice_no'].upper().startswith('C')
   values=[a if q>0 and p>0 and not cancel else Decimal(0),-a if q<0 and p>0 and cancel else Decimal(0),a if p>0 and (q<0 or(q>0 and not cancel)) else Decimal(0)]
   for key in [('pais',r['country']),('producto',r['stock_code'])]:
    for i in range(3):groups[key][i]+=values[i]
   if r['country']=='France':
    for i in range(3):france[i]+=values[i]
 expected=sum(1 for s,c,n in groups.values() if(n<0 and c>=100)or(s>=1000 and c/s>=Decimal('.2')))
 async with httpx.AsyncClient(timeout=120) as client:
  response=await client.get(URL+'/api/audit');data=response.json();Path(ROOT/'tests/auditoria_publica.json').write_text(json.dumps(data,ensure_ascii=False,indent=2));a=data.get('audit',{})
  check('Auditoría vs CSV completo',expected,a.get('alertas_activas'),a.get('alertas_activas')==expected and a.get('lineas_analizadas')==rows)
  check('Todos los grupos',len(groups),a.get('grupos_analizados'),len(groups)==a.get('grupos_analizados'))
  check('Borrador verificable y sin envío','borrador_no_enviado',data.get('draft',{}).get('estado'),data.get('draft',{}).get('estado')=='borrador_no_enviado')
  r=(await client.get(URL+'/api/report?pais=France')).json()['summary']['metricas']
  check('KPI Francia vs CSV',[str(v) for v in france],r,all(abs(float(v)-float(r[k]))<.0001 for v,k in zip(france,['ventas_positivas','cancelaciones','importe_neto'])))
  s=(await client.post(URL+'/api/scenario',json={'pais':'France','coste_porcentaje':70})).json()
  target=float(france[2]-france[0]*Decimal('.7'))
  check('Simulación explícita',target,s,abs(s.get('resultado_estimado',-999)-target)<.0001 and s.get('tipo')=='SIMULACION_NO_BENEFICIO_REAL')
  for path in ['/api/report?desde=2011-02-30','/api/audit?desde=2012-01-01&hasta=2011-01-01']:
   r=await client.get(URL+path);check('Fecha inválida '+path,422,r.status_code,r.status_code==422)
  r=await client.post(URL+'/api/scenario',json={'coste_porcentaje':-1});check('Coste inválido',422,r.status_code,r.status_code==422)
  r=(await client.get(URL+'/api/audit?pais=NO_EXISTE')).json()['audit'];check('País sin datos',0,r['alertas_activas'],r['alertas_activas']==0 and r['lineas_analizadas']==0)
  for index,q in enumerate(['Audita las anomalías de Francia y propón acciones correctivas, distinguiendo hipótesis y hechos.','¿Qué beneficio real y descuentos tiene Francia? No uses costes supuestos.']):
   r=await client.post(URL+'/api/chat',json={'question':q});body=r.json();(ROOT/f'tests/agente_auditor_{index}.json').write_text(json.dumps(body,ensure_ascii=False,indent=2))
   check('Agente '+str(index),'HTTP200 y llamadas MCP',{'status':r.status_code,'tools':[x['tool'] for x in body.get('evidence',[])]},r.status_code==200 and bool(body.get('evidence')))
 async with streamablehttp_client(URL+'/api/mcp') as (read,write,_):
  async with ClientSession(read,write) as session:
   await session.initialize();tools=await session.list_tools();check('MCP catálogo',6,len(tools.tools),len(tools.tools)==6)
   r=await session.call_tool('auditar_anomalias',{'pais':'France'});check('MCP auditoría real',False,r.isError,r.isError is False)
   r=await session.call_tool('resumen_ventas',{'sql':'DROP TABLE ventas_uci'});check('MCP rechaza SQL arbitrario',True,r.isError,r.isError is True)
 (ROOT/'tests/resultados_entrega.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
 if any(r['estado']=='FAIL' for r in results):raise SystemExit(1)
asyncio.run(main())
