# Plan y alcance vigentes

La aplicación cloud está publicada y conectada con Groq, MCP y Supabase. El plan de cinco horas es la planificación académica, no un registro inventado de tiempos reales. Consultar ESTADO_PROYECTO.md y tests/pruebas.md para evidencias.

## Plan de cinco horas
| Fase | Minutos | Resultado y condición para avanzar |
|---|---:|---|
| Investigación | 45 | Comparar Superstore y UCI, documentar procedencia, problema, usuario y límites. Elegir ventas/cancelaciones con UCI. |
| Datos | 40 | Descargar original oficial, calcular hash, perfilar nulos/duplicados/fechas, crear esquema e importar en Supabase. Verificar recuentos e importes contra el original. |
| Arquitectura | 35 | Documentar frontend → API → agente LLM → cliente MCP → servidor MCP → PostgreSQL. Definir Skill y herramientas de lectura. |
| Desarrollo | 135 | 25 min importación/configuración; 35 min MCP y consultas; 45 min agente/API; 30 min interfaz e integración. |
| Pruebas | 30 | Ejecutar pruebas de datos, herramientas MCP, agente, errores y flujo completo; guardar evidencias reales. |
| Reflexión | 15 | Cada integrante completa sus respuestas; preparar reflexión conjunta y guion de demo. |

## Alcance mínimo que debe funcionar
1. Pregunta: «¿Qué países concentran las ventas y las cancelaciones?»
2. El LLM selecciona herramientas a través del protocolo MCP real, no una función local etiquetada como MCP.
3. Herramientas permitidas: resumen del periodo, ventas por país/producto y cancelaciones. Parámetros validados; SQL parametrizado y lectura solamente; sin SQL arbitrario generado por el modelo.
4. La Skill se guarda en SKILL.md y el backend carga sus instrucciones: consultar datos antes de responder, indicar periodo y unidad, separar observación de hipótesis y no inventar costes ni causas.
5. El backend devuelve respuesta y trazas de herramientas sin secretos. El frontend muestra las evidencias.
6. Una segunda pregunta debe provocar otra consulta: el flujo debe demostrar elección de herramientas por el agente.

## Definiciones de datos antes de programar
UCI Online Retail registra líneas de transacciones, no una fila por pedido. Definir importe como Quantity × UnitPrice en GBP. Identificar cancelaciones según InvoiceNo con prefijo C; examinar cantidades negativas por separado y evitar doble conteo. Mostrar ventas positivas, importes de cancelación e importe neto con reglas explícitas. No llamar beneficio al importe neto. No asumir que cada cancelación representa una devolución física. Mantener nulos de cliente cuando no impidan el análisis agregado. Revisar precios no positivos y duplicados sin eliminarlos silenciosamente. Diciembre de 2011 es parcial: no comparar sus totales con meses completos sin advertencia.

## GitHub y Supabase
Son piezas distintas: GitHub aloja código, documentación e historial; Supabase aloja PostgreSQL. El backend conecta con Supabase usando DATABASE_URL local. No hace falta enlazar las cuentas ni desplegar para demostrar el sistema local.

Guardar SQL del esquema, scripts de importación, dataset con licencia/fuente y huella, dependencias verificadas, README, arquitectura, Skill, configuración MCP de ejemplo sin claves, evidencias, prompts y REFLEXION.md. Excluir .env, claves, contraseñas, entornos virtuales y registros con secretos. Si el tamaño de datos dificulta GitHub, conservar un subconjunto temporal reproducible y documentado junto con script para descargar el original; nunca inventar filas.

Bibliotecas candidatas de GitHub: https://github.com/modelcontextprotocol/python-sdk y https://github.com/fastapi/fastapi. Registrar versión y licencia utilizadas una vez instaladas y verificadas.

