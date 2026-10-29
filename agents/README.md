# Agente coordinador
Implementación pública: `web_publica/app/api/[...path]/route.ts`. Alternativa local: `backend/agent.py`. Groq con openai/gpt-oss-20b; sin API de OpenAI. Skill: skills/auditar_ventas/SKILL.md. Catálogo de seis herramientas MCP.
El agente debe consultar datos antes de responder. Decide herramientas y parámetros, conserva las trazas y distingue hechos, hipótesis, acciones y supuestos. Auditorías y borradores se renderizan con cifras estructuradas verificadas. Ninguna acción cambia políticas comerciales ni envía mensajes.
