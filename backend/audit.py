"""Auditoría de solo lectura y acciones propuestas, sin enviar comunicaciones."""
from db import query, Periodo, resumen

def audit(p: Periodo):
    data=query('SELECT public.bi_audit(%s,%s,%s) AS data',(p.desde,p.hasta,p.pais))[0]['data']
    for a in data['alertas']:
        a.update(dato_critico=f"{a['dimension']}: {a['grupo']}; cancelaciones {a['cancelaciones']} GBP; neto {a['importe_neto']} GBP.",
                 hipotesis='La causa no está demostrada; contrastar anulaciones, correcciones y asientos contables con las facturas.',
                 accion='Conciliar abonos y ventas; clasificar el código como mercancía o ajuste contable antes de modificar precios.' if a['regla']=='neto_negativo' else 'Revisar facturas canceladas y motivos con operaciones y atención al cliente.',
                 responsable='Responsable comercial y administración',validacion='Documentar motivos, repetir auditoría y comparar periodos completos equivalentes.')
    return data

def draft(data):
    return {'estado':'borrador_no_enviado','destinatario':'Responsable comercial y administración (revisar destinatario)',
            'asunto':f"Revisión de ventas y cancelaciones · {data['desde']} a {data['hasta']}",
            'cuerpo':f"Hola equipo:\nLa auditoría del {data['desde']} al {data['hasta']} identifica {data['alertas_activas']} señales.\n"+'\n'.join(a['dato_critico']+' Acción: '+a['accion'] for a in data['alertas'][:3])+'\nConciliar facturas antes de decidir. No demuestra pérdidas ni causas. Los grupos pueden solaparse. Borrador no enviado.'}

def scenario(p: Periodo,coste_porcentaje: float):
    if not 0<=coste_porcentaje<=200: raise ValueError('Coste inválido')
    m=resumen(p)['metricas']; net=float(m['importe_neto']); sales=float(m['ventas_positivas']); cost=sales*coste_porcentaje/100
    return {'tipo':'SIMULACION_NO_BENEFICIO_REAL','supuesto_coste_porcentaje':coste_porcentaje,'ventas_positivas':sales,'importe_neto':net,'coste_estimado':cost,'resultado_estimado':net-cost,'margen_estimado_porcentaje':100*(net-cost)/net if net>0 else None,'moneda':'GBP','limites':'Costes supuestos no recuperados al cancelar; sin gastos fijos ni impuestos.'}
