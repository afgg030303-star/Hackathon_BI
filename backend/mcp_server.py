from typing import Literal
from mcp.server.fastmcp import FastMCP
from db import Periodo, Ranking, resumen, ranking, calidad

mcp=FastMCP('Auditor BI — UCI y Supabase',log_level='ERROR')

@mcp.tool()
def resumen_ventas(desde: str='2010-12-01', hasta: str='2011-12-09', pais: str|None=None) -> dict:
    """Obtiene ventas positivas, cancelaciones e importe neto GBP para un periodo inclusivo y país exacto opcional. No calcula beneficio."""
    return resumen(Periodo(desde=desde,hasta=hasta,pais=pais))

@mcp.tool()
def comparar_grupos(dimension: Literal['pais','producto','mes']='pais', desde: str='2010-12-01', hasta: str='2011-12-09', pais: str|None=None, limite: int=8) -> dict:
    """Ranking descendente por importe neto, agrupado por país, código de producto o mes. Fechas inclusivas; máximo 20 grupos."""
    return ranking(Ranking(dimension=dimension,desde=desde,hasta=hasta,pais=pais,limite=limite))

@mcp.tool()
def comprobar_calidad() -> dict:
    """Consulta procedencia UCI, cobertura temporal, recuentos, nulos y precios no positivos del dataset completo."""
    return calidad()

@mcp.tool()
def auditar_anomalias(desde: str='2010-12-01',hasta: str='2011-12-09',pais: str|None=None) -> dict:
    """Audita todos los grupos, detecta señales y propone acciones, sin inferir causas."""
    from audit import audit
    return audit(Periodo(desde=desde,hasta=hasta,pais=pais))

@mcp.tool()
def redactar_borrador(desde: str='2010-12-01',hasta: str='2011-12-09',pais: str|None=None) -> dict:
    """Genera un borrador de email a partir de la auditoría; nunca envía."""
    from audit import draft
    data=auditar_anomalias(desde,hasta,pais)
    return {**draft(data),'auditoria':data}

@mcp.tool()
def estimar_escenario(coste_porcentaje: float,desde: str='2010-12-01',hasta: str='2011-12-09',pais: str|None=None) -> dict:
    """Simulación con coste supuesto explícito del usuario; no beneficio real."""
    from audit import scenario
    return scenario(Periodo(desde=desde,hasta=hasta,pais=pais),coste_porcentaje)

if __name__=='__main__':
    mcp.run(transport='stdio')
