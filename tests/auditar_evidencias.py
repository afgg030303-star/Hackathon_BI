"""Conciliación país/mes, SQL directo y tráfico MCP real; solo lectura."""
import csv,gzip,json,os
from pathlib import Path
from decimal import Decimal
import httpx,psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
root=Path(__file__).resolve().parents[1];load_dotenv(root/'.env');out=root/'tests/auditoria_29';out.mkdir(exist_ok=True)
url='https://observatorio-retail-bi.balmyspark1.chatgpt.site'
m={'ventas_positivas':Decimal(0),'cancelaciones':Decimal(0),'importe_neto':Decimal(0)};orders=set();rows=0
with gzip.open(root/'data/ventas_uci.csv.gz','rt') as f:
 for r in csv.DictReader(f):
  if r['country']!='France' or not r['invoice_date'].startswith('2011-11'):continue
  rows+=1;q=Decimal(r['quantity']);price=Decimal(r['unit_price']);amount=q*price;c=r['invoice_no'].upper().startswith('C')
  if price>0:
   if q>0 and not c:m['ventas_positivas']+=amount;orders.add(r['invoice_no'])
   if q<0 and c:m['cancelaciones']-=amount
   if q<0 or(q>0 and not c):m['importe_neto']+=amount
m.update(pedidos_venta=len(orders),lineas=rows)
with psycopg2.connect(os.environ['DATABASE_URL'],sslmode='require') as c:
 c.set_session(readonly=True)
 with c.cursor(cursor_factory=RealDictCursor) as q:
  sql='SELECT count(*) AS filas,min(invoice_date) AS desde,max(invoice_date) AS hasta,sum(quantity*unit_price) AS importe_origen FROM public.ventas_uci'
  q.execute(sql);profile=dict(q.fetchone());(out/'sql_base.json').write_text(json.dumps({'sql':sql,'resultado':profile},default=str,indent=2))
with httpx.Client(timeout=60) as client:
 params={'pais':'France','desde':'2011-11-01','hasta':'2011-11-30'}
 r=client.get(url+'/api/report',params=params);r.raise_for_status();observed=r.json()['summary']['metricas']
 comparison={k:{'csv':str(v),'web':str(observed[k]),'coincide':abs(Decimal(str(observed[k]))-Decimal(str(v)))<Decimal('.000001')} for k,v in m.items()}
 assert all(x['coincide'] for x in comparison.values());(out/'conciliacion_pais_mes.json').write_text(json.dumps({'entrada':params,'comparacion':comparison,'estado':'PASS'},indent=2));print(comparison)
 exchanges=[]
 for i,(method,params) in enumerate([('initialize',{'protocolVersion':'2025-03-26','capabilities':{},'clientInfo':{'name':'auditoria-evidencias','version':'1'}}),('tools/list',{}),('tools/call',{'name':'redactar_borrador','arguments':{'pais':'France'}}),('tools/call',{'name':'resumen_ventas','arguments':{'sql':'UPDATE ventas_uci SET quantity=0'}})]):
  payload={'jsonrpc':'2.0','id':i+1,'method':method,'params':params};r=client.post(url+'/api/mcp',headers={'Accept':'application/json, text/event-stream'},json=payload);exchanges.append({'url':url+'/api/mcp','request':payload,'status':r.status_code,'response':r.json()})
 assert not exchanges[2]['response']['result']['isError'];assert exchanges[3]['response']['result']['isError']
 (out/'mcp_http_real.json').write_text(json.dumps(exchanges,ensure_ascii=False,indent=2))
 for name,path in [('periodo_vacio','/api/report?desde=2020-01-01&hasta=2020-01-31'),('fechas_invertidas','/api/report?desde=2012-01-01&hasta=2011-01-01')]:
  r=client.get(url+path);(out/(name+'.json')).write_text(json.dumps({'status':r.status_code,'body':r.json()},indent=2))
print('SQL, conciliación y MCP registrados')
