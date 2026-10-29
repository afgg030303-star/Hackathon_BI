# Recorrido único del 29/10/2026
1. Se recargó la web pública (versión5).
2. Se escribió exactamente «Redacta un borrador de email con las alertas de Francia.» y se pulsó Consultar.
3. El agente eligió redactar_borrador con France y periodo completo. La UI mostró resultado y una consulta MCP.
4. Se expandió esa consulta: Skill auditar-ventas cargada como instrucciones, SHA256, procedimiento y resultados SQL agregados. Se guardó el JSON visible en skill_y_mcp_navegador.json.
5. Se pulsó «Descargar este borrador .txt» de esa misma respuesta. El navegador descargó borrador-agente.txt; una copia se conserva aquí.
6. Se comprobó que el texto descargado contiene exactamente el cuerpo de la respuesta MCP y que el hash de la Skill coincide con el archivo del repositorio. Ver verificacion_descarga.json.

Este recorrido está documentado con captura, traza y archivo descargado; no se ha grabado vídeo. La traza HTTP independiente mcp_http_real.json muestra el protocolo JSON-RPC real, no una función Python renombrada. El borrador no se envió a ningún destinatario.

Comprobación adicional: filtros France y noviembre2011 muestran31758.71 ventas,1061.20 cancelaciones,30697.51 neto y64 pedidos, coincidentes con CSV. Captura filtros_mes.png. Formulario de escenario vacío bloquea envío por required/valueMissing; no presenta un resultado nuevo.
