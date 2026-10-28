# Observatorio Retail — agente BI

**Web pública:** https://observatorio-retail-bi.balmyspark1.chatgpt.site

Pregunta por ventas y cancelaciones de un comercio real. El agente usa Groq, una Skill y herramientas MCP para consultar PostgreSQL en Supabase. El panel muestra KPI verificables. No se calculan beneficios: no hay costes en el dataset.

## Entrega
- `investigacion/`: problema, alternativas y fuentes.
- `data/`: dataset UCI comprimido, perfil y migraciones SQL.
- `arquitectura/`: flujo cloud y alternativa local.
- `web_publica/`: código desplegado (backend TypeScript y frontend).
- `backend/`, `frontend/`: alternativa local Python/FastAPI.
- `agents/`, `skills/`, `config/`: agente, Skill y MCP.
- `tests/`: evidencias reales y resultados.
- `00_prompts_ia/`: resúmenes de sesiones y relevo sin secretos.
- `REFLEXION.md`: preguntas pendientes de completar personalmente.

## Ejecutar localmente
Python 3.13. Crear `.venv`, instalar `backend/requirements.txt`, copiar `.env.example` a `.env` si no existe. Configurar DATABASE_URL y GROQ_API_KEY. Ejecutar:

```sh
python -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Sin GROQ_API_KEY se utiliza Ollama con qwen3:4b-instruct. No hace falta una API de OpenAI: el modelo openai/gpt-oss-20b se sirve a través de Groq.

## Despliegue cloud
`web_publica` usa Vinext/Cloudflare Workers en Sites. Secretos del servidor: GROQ_API_KEY, SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY. Aplicar las migraciones una sola vez sobre la base compartida. La web no depende del Mac. El endpoint MCP Streamable HTTP es `/api/mcp`. La clave publicable solo tiene acceso a agregados UCI mediante bi_tool; las filas están protegidas por RLS. Nunca subir `.env` ni la contraseña de PostgreSQL.

Para compilar el código cloud: `cd web_publica && npm ci && npm run build`. El despliegue Sites se realiza con su flujo de publicación y el project_id guardado; un push a este GitHub por sí solo no despliega Sites.

## Datos y límites
UCI Online Retail, 541.909 filas, diciembre 2010–diciembre 2011, GBP. Fuente y licencia en `data/FUENTES_Y_DECISION.md`. El dataset original y sus anomalías se conservan. Diciembre 2011 es parcial. `train.csv` es el archivo previo Superstore ficticio, no la fuente del agente.
Groq tiene cuotas: un 429 requiere esperar; el panel SQL sigue funcionando. Las conclusiones del LLM necesitan revisión contra la evidencia: no son decisiones automáticas.

## Colaboración
Rama de trabajo `desarrollo/agente-bi`; leer COLABORACION.md. Commit/push publica archivos, pull trae los del otro equipo. No hay sincronización automática ni exportación íntegra automática de chats.
