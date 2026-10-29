# Auditor de ventas y cancelaciones | Observatorio Retail

**Web pública:** https://observatorio-retail-bi.balmyspark1.chatgpt.site

Audita ventas y cancelaciones de un comercio real, consulta alertas y prepara acciones con un borrador de email. El agente usa Groq, una Skill y herramientas MCP para consultar PostgreSQL en Supabase. El panel muestra KPI verificables. No se calculan beneficios: no hay costes en el dataset.

## Entrega
- `investigacion/`: problema, alternativas y fuentes.
- `data/`: dataset UCI comprimido, perfil y migraciones SQL.
- `arquitectura/`: flujo cloud y alternativa local.
- `web_publica/`: código desplegado (backend TypeScript y frontend).
- `backend/`, `frontend/`: alternativa local Python/FastAPI.
- `agents/`, `skills/`, `config/`: agente, Skill y MCP.
- `tests/`: evidencias reales y resultados.
- `00_prompts_ia/`: resúmenes de sesiones y relevo sin secretos.
- `REFLEXION.md`: respuestas completas de los tres integrantes y reflexión conjunta, tomadas del documento elegido `Reflexion_Equipo_Auditor_Ventas.md`.

## Ejecutar localmente
Python 3.13. Crear `.venv`, instalar `backend/requirements.txt`, copiar `.env.example` a `.env` si no existe. Configurar DATABASE_URL y GROQ_API_KEY. Ejecutar:

```sh
python -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Sin GROQ_API_KEY se utiliza Ollama con qwen3:4b-instruct. No hace falta una API de OpenAI: el modelo openai/gpt-oss-20b se sirve a través de Groq.

## Despliegue cloud
`web_publica` usa Vinext/Cloudflare Workers en Sites. Secretos del servidor: GROQ_API_KEY, SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY. Aplicar las migraciones 001–003 una sola vez sobre la base compartida; ya están aplicadas en el proyecto actual. La web no depende del Mac. El endpoint MCP Streamable HTTP es `/api/mcp`. La clave publicable solo tiene acceso a agregados UCI mediante bi_tool; las filas están protegidas por RLS. Nunca subir `.env` ni la contraseña de PostgreSQL.

Para compilar el código cloud: `cd web_publica && npm ci && npm run build`. El despliegue Sites se realiza con su flujo de publicación y el project_id guardado; un push a este GitHub por sí solo no despliega Sites.

## Datos y límites
UCI Online Retail, 541.909 filas, diciembre 2010–diciembre 2011, GBP. Fuente y licencia en `data/FUENTES_Y_DECISION.md`. El dataset original y sus anomalías se conservan. Diciembre 2011 es parcial. `train.csv` es el archivo previo Superstore ficticio, no la fuente del agente.
Groq tiene cuotas: un 429 requiere esperar; el panel SQL sigue funcionando. Las conclusiones del LLM necesitan revisión contra la evidencia: no son decisiones automáticas.

## Colaboración
La entrega se consulta en `main`; las tareas se realizan en ramas y se integran mediante PR. Leer COLABORACION.md. Commit/push publica archivos, pull trae los del otro equipo. No hay sincronización automática ni exportación íntegra automática de chats.

## Auditoría y acciones
Se revisan todos los grupos de país y producto. El centro de auditoría muestra hasta 12 señales y el recuento completo; las reglas son explícitas. Cada señal propone comprobación, responsable y validación. El borrador se descarga como texto y no se envía. La actualización automática funciona cada 60 segundos solo con la página visible.

El escenario de rentabilidad requiere un porcentaje de coste introducido por el usuario. Es una simulación identificada, no beneficio real. No inferimos descuentos ni causas que no estén en los datos.

## Pruebas y defensa
- `python tests/validar_publico.py`: CSV independiente, API, MCP y 2 preguntas a Groq (consume cuota). BI_TEST_URL permite otro despliegue.
- `node --test tests/unit/audit.test.mjs`: reglas de presentación, borradores y escenarios.
- `tests/pruebas.md`: matriz con resultados reales, errores y evidencias.
- `ENTREGA.md`: cobertura de todos los requisitos y pendientes humanos.
- `DEFENSA.md`: guion de demostración y preguntas para preparar.

Auditoría de entrega actualizada: `tests/auditoria_29/` conserva el recorrido de borrador descargado, traza Skill/MCP, SQL, captura Supabase y comparación CSV por país/mes. `tests/pruebas.md` contiene las seis columnas para las nueve pruebas y casos de error.

## Preparar la presentación
- [Guía completa de defensa en PDF](output/pdf/Guia_defensa_auditor_ventas.pdf): guion, preguntas y respuestas, cifras de control, errores y límites.
- [Mapa de entrega](ENTREGA.md): correspondencia entre cada requisito y sus archivos.
- [Reflexión vigente](Reflexion_Equipo_Auditor_Ventas.md): Eva, Andrés y Sacha.

Las carpetas obligatorias `investigacion`, `data`, `agents`, `skills`, `backend`, `frontend`, `config` y `tests` están presentes. `arquitectura` documenta el diseño; `web_publica` conserva el código cloud desplegado; `00_prompts_ia` permite el relevo y `output/pdf` contiene la defensa. Son complementos organizados a los requisitos, no aplicaciones adicionales. No se han movido módulos ejecutables para evitar romper sus rutas.
