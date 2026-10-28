# Estado para continuar — 28/10/2026

## Destinos acordados
- GitHub: https://github.com/afgg030303-star/Hackathon_BI
- Supabase: gvsxekaqeodljocyqkfo (Hackathon-BI).

## Preparado
Git inicializado conservando el historial remoto; instrucciones AGENTS.md, guía COLABORACION.md, plantilla .env.example, registro de sesión y prueba de conexión sin dependencia de tablas. La carpeta .env está excluida de Git. El agente BI, MCP y frontend todavía no están implementados.

## Verificación pendiente
- Primera publicación verificada: commit d592acc en origin/setup/colaboracion mediante GitHub Desktop (evatrigolahoz). La creación de pull request con el conector devuelve 403; para esta preparación inicial se integra mediante avance directo de main, sin sobrescribir commits remotos. Verificar main contra origin al continuar.
- Conector GitHub del chat: 872587-ai, permiso de lectura. La usuaria confirma ser colaboradora; publicación con GitHub Desktop como evatrigolahoz comprobada.
- Supabase: conexión real TLS verificada mediante Session pooler. Tabla public.ventas_superstore accesible: 9.800 filas. No se han modificado datos. La conexión directa fallaba en resolución DNS; se actualizó solo .env local conservando la contraseña.
- Segundo ordenador: clonar repositorio, traer la rama integrada y configurar su propio .env; validar conexión desde ese equipo.

- Entorno local .venv creado con Python 3.13; instalados psycopg2-binary 2.9.13 y python-dotenv 1.2.4. Ambas pruebas de conexión se ejecutaron correctamente con credenciales reales (salida 0).

## Verificación de conexión completada
Ver 04_pruebas_y_reflexion/supabase_2026-10-28.md. La preparación inicial está en main. Falta que el segundo ordenador configure su .env y ejecute la prueba.

## Trabajo posterior
Completar colaboración antes de desarrollar. Luego seguir PLAN_DE_TRABAJO.md. No usar el CSV local como prueba de datos reales ni afirmar beneficio/descuento inexistentes. Cada integrante redactará su reflexión real.
