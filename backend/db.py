"""Consultas parametrizadas y acotadas. Ninguna herramienta acepta SQL arbitrario."""
import json
import os
from datetime import date, timedelta
from decimal import Decimal
from typing import Literal
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, ConfigDict, Field, model_validator
from config import ROOT

class Periodo(BaseModel):
    model_config = ConfigDict(extra='forbid')
    desde: date = date(2010,12,1)
    hasta: date = date(2011,12,9)
    pais: str | None = Field(default=None, max_length=80)

    @model_validator(mode='after')
    def rango(self):
        if self.desde > self.hasta or self.hasta >= date(9999,12,31):
            raise ValueError('El rango de fechas no es válido')
        return self

class Ranking(Periodo):
    dimension: Literal['pais','producto','mes'] = 'pais'
    limite: int = Field(default=8,ge=1,le=20)

class DatabaseUnavailable(RuntimeError): pass

def query(sql, params=()):
    conn=None
    try:
        conn=psycopg2.connect(os.environ['DATABASE_URL'],connect_timeout=8,sslmode='require',
                             options='-c statement_timeout=15000',application_name='auditor_bi_mcp')
        conn.set_session(readonly=True)
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql,params)
            return json.loads(json.dumps(cur.fetchall(),default=lambda v: str(v) if isinstance(v,(Decimal,date)) else v))
    except (psycopg2.Error,KeyError,ValueError):
        raise DatabaseUnavailable('No se pudo consultar el dataset UCI en Supabase. Revisa conexión y carga.') from None
    finally:
        if conn is not None: conn.close()

def filters(p):
    return (p.desde,p.hasta+timedelta(days=1),p.pais,p.pais)

BASE = '''WITH base AS (
 SELECT *, quantity * unit_price AS importe,
 upper(invoice_no) LIKE 'C%%' AS cancelacion
 FROM public.ventas_uci
 WHERE invoice_date >= %s AND invoice_date < %s AND (%s IS NULL OR country = %s)
) '''
METRICS = '''count(*) AS lineas,
 count(DISTINCT invoice_no) FILTER (WHERE quantity>0 AND unit_price>0 AND NOT cancelacion) AS pedidos_venta,
 COALESCE(sum(importe) FILTER (WHERE quantity>0 AND unit_price>0 AND NOT cancelacion),0) AS ventas_positivas,
 COALESCE(-sum(importe) FILTER (WHERE quantity<0 AND unit_price>0 AND cancelacion),0) AS cancelaciones,
 COALESCE(-sum(importe) FILTER (WHERE quantity<0 AND unit_price>0 AND NOT cancelacion),0) AS otros_ajustes_negativos,
 COALESCE(sum(importe) FILTER (WHERE unit_price>0 AND (quantity<0 OR (quantity>0 AND NOT cancelacion))),0) AS importe_neto,
 count(*) FILTER (WHERE unit_price<=0 OR quantity=0 OR (quantity>0 AND cancelacion)) AS lineas_fuera_kpi'''

def context(p):
    return {'fuente':'UCI Online Retail','moneda':'GBP','desde':str(p.desde),'hasta':str(p.hasta),'pais':p.pais,
            'limites':'Importe neto no es beneficio; no hay costes. Cancelación no prueba devolución física. Diciembre 2011 es parcial.'}

def resumen(p: Periodo):
    result=query(BASE+'SELECT '+METRICS+' FROM base',filters(p))[0]
    return {**context(p),'metricas':result}

def ranking(p: Ranking):
    dimension={'pais':'country','producto':'stock_code','mes':"to_char(invoice_date,'YYYY-MM')"}[p.dimension]
    sql=BASE+f'SELECT {dimension} AS grupo, '+METRICS+f' FROM base GROUP BY {dimension} ORDER BY importe_neto DESC, grupo LIMIT %s'
    return {**context(p),'dimension':p.dimension,'orden':'importe_neto descendente','filas':query(sql,(*filters(p),p.limite))}

def calidad():
    result=query('''SELECT count(*) AS filas, min(invoice_date)::date AS fecha_min,
 max(invoice_date)::date AS fecha_max, count(*) FILTER (WHERE customer_id IS NULL) AS sin_cliente,
 count(*) FILTER (WHERE description IS NULL) AS sin_descripcion,
 count(*) FILTER (WHERE unit_price<=0) AS precio_no_positivo,
 count(*) FILTER (WHERE quantity<0) AS cantidad_negativa,
 sum(quantity*unit_price) AS importe_bruto_origen FROM public.ventas_uci''')[0]
    metadata=query("SELECT dataset,source_sha256,row_count,raw_amount FROM public.bi_dataset_metadata WHERE dataset='uci_online_retail'")
    return {'fuente':'https://archive.ics.uci.edu/dataset/352/online+retail','perfil':result,'procedencia':metadata,
            'reglas':'No se han eliminado duplicados o nulos. Los KPI excluyen precios no positivos, cantidades cero y cancelaciones con cantidad positiva.'}
