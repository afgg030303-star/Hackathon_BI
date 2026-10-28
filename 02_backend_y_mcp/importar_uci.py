"""Descarga reproducible, extracción y carga transaccional; nunca reemplaza datos."""
import argparse
import csv
import gzip
import hashlib
import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
import openpyxl
import psycopg2
from config import ROOT
import os

SOURCE = 'https://archive.ics.uci.edu/static/public/352/online+retail.zip'
DATA = ROOT / '01_investigacion_y_datos'
HEADER = ['source_row','invoice_no','stock_code','description','quantity','invoice_date','unit_price','customer_id','country']

def prepare():
    original = DATA / 'originales'
    original.mkdir(exist_ok=True)
    archive = original / 'online_retail.zip'
    if not archive.exists():
        with urlopen(SOURCE, timeout=90) as response, archive.open('wb') as out:
            while chunk := response.read(1024 * 1024):
                out.write(chunk)
    sha = hashlib.sha256(archive.read_bytes()).hexdigest()
    target = DATA / 'datos_preparados.csv'
    report_path = DATA / 'perfil_uci.json'
    if target.exists() and report_path.exists():
        previous = json.loads(report_path.read_text())
        if previous['source_sha256'] == sha and previous['csv_sha256'] == hashlib.sha256(target.read_bytes()).hexdigest():
            return previous
    with ZipFile(archive) as z:
        workbook_name = next(n for n in z.namelist() if n.endswith('.xlsx'))
        with z.open(workbook_name) as f:
            wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
            ws = wb.active
            it = ws.iter_rows(values_only=True)
            assert list(next(it)) == ['InvoiceNo','StockCode','Description','Quantity','InvoiceDate','UnitPrice','CustomerID','Country']
            count = 0
            total = Decimal(0)
            missing_customer = 0
            missing_description = 0
            nonpositive_price = 0
            negative_quantity = 0
            cancel_lines = 0
            dates = []
            with target.open('w', encoding='utf-8', newline='') as out:
                writer = csv.writer(out)
                writer.writerow(HEADER)
                for source_row, values in enumerate(it, 2):
                    inv, stock, desc, qty, date, price, customer, country = values
                    if not isinstance(date, datetime):
                        raise ValueError('Fecha de origen no reconocida')
                    price = Decimal(str(price))
                    qty = int(qty)
                    inv = str(inv)
                    customer = '' if customer is None else str(int(customer))
                    writer.writerow([source_row,inv,str(stock),desc or '',qty,date.isoformat(' '),str(price),customer,country])
                    count += 1
                    total += qty * price
                    missing_customer += not bool(customer)
                    missing_description += desc is None
                    nonpositive_price += price <= 0
                    negative_quantity += qty < 0
                    cancel_lines += inv.upper().startswith('C')
                    dates.append(date)
            wb.close()
    report = dict(source=SOURCE, source_sha256=sha, csv_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                  rows=count, raw_amount=str(total), currency='GBP', missing_customer=missing_customer,
                  missing_description=missing_description, nonpositive_price=nonpositive_price,
                  negative_quantity=negative_quantity, cancellation_lines=cancel_lines,
                  date_min=min(dates).isoformat(), date_max=max(dates).isoformat(),
                  transformation='Todas las filas originales; sin eliminar nulos ni duplicados. source_row conserva la fila del XLSX.')
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n')
    with target.open('rb') as inp, gzip.open(DATA/'ventas_uci.csv.gz','wb') as out:
        while chunk := inp.read(1024*1024): out.write(chunk)
    return report

def load(report):
    conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require', connect_timeout=10,
                           options='-c statement_timeout=120000')
    try:
        with conn:
            with conn.cursor() as cur:
                # Serializa cargas del equipo sin bloquear indefinidamente.
                cur.execute('SELECT pg_try_advisory_xact_lock(52352026)')
                if not cur.fetchone()[0]: raise RuntimeError('Otra carga UCI está en curso')
                cur.execute((DATA/'migrations/001_ventas_uci.sql').read_text())
                cur.execute('SELECT count(*), COALESCE(sum(quantity * unit_price),0) FROM public.ventas_uci')
                count, amount = cur.fetchone()
                if count:
                    cur.execute("SELECT source_sha256 FROM public.bi_dataset_metadata WHERE dataset='uci_online_retail'")
                    metadata = cur.fetchone()
                    if count != report['rows'] or amount != Decimal(report['raw_amount']) or not metadata or metadata[0] != report['source_sha256']:
                        raise RuntimeError('La tabla ya existe y no coincide con esta carga; no se modifica')
                    return {'status':'already_loaded','rows':count,'raw_amount':str(amount)}
                with (DATA/'datos_preparados.csv').open(encoding='utf-8') as f:
                    cur.copy_expert('COPY public.ventas_uci FROM STDIN WITH (FORMAT CSV, HEADER TRUE)',f)
                cur.execute('SELECT count(*), sum(quantity * unit_price) FROM public.ventas_uci')
                count, amount = cur.fetchone()
                if count != report['rows'] or amount != Decimal(report['raw_amount']):
                    raise RuntimeError('Conciliación fallida; rollback')
                cur.execute("INSERT INTO public.bi_dataset_metadata(dataset,source_sha256,row_count,raw_amount) VALUES (%s,%s,%s,%s)",
                            ('uci_online_retail',report['source_sha256'],count,amount))
        return {'status':'imported','rows':count,'raw_amount':str(amount)}
    finally:
        conn.close()

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--load',action='store_true',help='Crear/cargar únicamente las tablas UCI nuevas')
    args=parser.parse_args()
    try:
        report=prepare()
        print(json.dumps(report,ensure_ascii=False),flush=True)
        if args.load:
            result=load(report)
            (ROOT/'04_pruebas_y_reflexion/carga_uci.json').write_text(json.dumps(result,indent=2)+'\n')
            print(json.dumps(result),flush=True)
    except Exception as exc:
        print('Error de preparación/carga:',type(exc).__name__,'. No se imprimen credenciales.')
        raise SystemExit(1)
