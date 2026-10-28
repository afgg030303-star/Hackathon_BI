# Plan de ejecución — 28 de octubre de 2026

## Decisión recomendada
Auditor agéntico de ventas y cancelaciones de un comercio online real, con UCI Online Retail. Mantener PostgreSQL en Supabase, servidor MCP Python, backend FastAPI con LLM y frontend HTML/JavaScript. No prometer margen ni rentabilidad: no disponemos de costes. La recomendación sustituye la premisa de datos reales de Superstore de las instrucciones anteriores; esas instrucciones se conservan como historial.

## Estado comprobado
- Existe estructura inicial, requirements.txt y test_db.py.
- train.csv contiene 9.800 filas y 18 columnas; no contiene Profit, Discount ni Quantity.
- Supabase: el usuario informa de que creó el proyecto; conexión e importación sin verificar.
- DATABASE_URL y OPENAI_API_KEY contienen placeholders. No se ha intentado conectar con ellos.
- No hay repositorio Git inicializado, agente, MCP, frontend ni pruebas del flujo completo.
- Python por defecto: 3.15.1; preparar un entorno compatible (preferiblemente 3.12 o 3.13) antes de instalar dependencias.

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

## Orden inmediato
1. Obtener y documentar UCI Online Retail; conservar train.csv como archivo previo no válido para rentabilidad.
2. Preparar entorno y esquema/importación sin modificar tablas existentes sin inspeccionarlas.
3. Configurar DATABASE_URL en .env desde el panel Connect de Supabase. No pegar contraseñas en chats. Usar una conexión compatible con la red disponible.
4. Configurar una clave de API de un proveedor LLM en .env; sin acceso a un modelo no puede darse por verificada la parte agéntica.
5. Ejecutar recuento y conciliación antes del MCP, después conectar agente y frontend.
6. Crear repositorio en la cuenta y con la visibilidad elegidas por el equipo; comprobar exclusión de secretos antes de publicar.

## Pruebas obligatorias y evidencias
- Datos: filas importadas, nulos, periodo y sumas conciliados; filas rechazadas documentadas.
- PostgreSQL: conexión TLS, consultas correctas y rechazo de escritura con rol de lectura.
- MCP: inicialización, listado y ejecución real de herramientas desde un cliente MCP.
- Agente: selección de herramientas y respuesta consistente con cifras SQL; pregunta sin datos; rechazo de afirmaciones de beneficio no medible.
- API/frontend: pregunta y respuesta visibles; entradas inválidas, caída de DB y error de proveedor con mensajes sin secretos.
- Evidencia: comando, fecha, resultado esperado, resultado observado y log/captura. No marcar PASS si no se ejecutó.

## Defensa de cinco minutos
Mostrar procedencia y límites del dataset; hacer una pregunta en vivo; enseñar llamada MCP y consulta real; contrastar cifra; enseñar una prueba de error; explicar una limitación y una mejora. Priorizar arquitectura (20%), funcionamiento (20%) y pruebas (20%) sin descuidar datos ni reflexión. Ninguna elección garantiza una nota.
