# Instrucciones compartidas para Codex

## Contexto
Hackathon de BI con datos reales, PostgreSQL/Supabase, agente, Skill, MCP, backend y frontend. Leer ESTADO_PROYECTO.md, COLABORACION.md y PLAN_DE_TRABAJO.md al iniciar. Las instrucciones antiguas en 00_prompts_ia son historial: Superstore es ficticio y el CSV local no contiene Profit ni Discount; no afirmar lo contrario.

## Coordinación entre dos ordenadores
- Repositorio: https://github.com/afgg030303-star/Hackathon_BI .
- Supabase compartido: gvsxekaqeodljocyqkfo. No crear otro proyecto para el segundo ordenador.
- Revisar git status y traer los cambios remotos antes de empezar. No sobrescribir cambios locales ni hacer force push.
- Trabajar en una rama propia por tarea; integrar mediante pull request. Excepción para la preparación inicial: se permite avance directo de main si no hay divergencia ni cambios ajenos y se verifica el remoto. Evitar editar simultáneamente los mismos archivos.
- Al terminar cada bloque, registrar qué cambió, pruebas realizadas y pendientes en un archivo nuevo de 00_prompts_ia; actualizar el estado si corresponde. Hacer commit de los archivos revisados y push a la rama de trabajo cuando el acceso esté disponible. Si falla, informar del estado local y remoto por separado.
- No hay sincronización continua: commit guarda localmente; push sube a GitHub; fetch/pull trae cambios. Los chats completos no se exportan automáticamente mediante Git.
- Registrar prompts y respuestas disponibles de esta sesión sin secretos; identificar resúmenes como resúmenes. No inventar conversaciones anteriores.

## Base de datos y secretos
- DATABASE_URL y OPENAI_API_KEY solo en .env local o variables de entorno; nunca en Git, frontend, chats, capturas ni logs.
- Usar .env.example como plantilla. No sobrescribir un .env existente.
- Consultas analíticas de lectura. Guardar cambios de esquema en data/migrations y coordinar una única ejecución; no importar dos veces el dataset.
- Inspeccionar tablas antes de migrar y no borrar ni reemplazar datos existentes sin autorización específica.
- No declarar conexión, agente o prueba como funcional hasta ejecutarlos y conservar evidencia sin secretos.

## Alcance inmediato
El usuario autoriza desarrollar el auditor y sus mejoras y subir cada bloque terminado a GitHub. Usar Groq con la clave local autorizada; Ollama queda como alternativa sin clave. La web pública usa secretos de Sites y Supabase por HTTP. No esperar al segundo ordenador. No instalar sincronización automática en segundo plano. La base principal del agente es ventas_uci (UCI Online Retail real); conservar ventas_superstore como tabla histórica.
