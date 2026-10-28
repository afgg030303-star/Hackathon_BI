# Arquitectura
Web HTML/JS → API cloud (Vinext/Cloudflare) → Groq con Skill → cliente MCP HTTP → servidor /api/mcp → RPC de agregados Supabase/PostgreSQL → respuesta con evidencias.
El agente consulta el catálogo MCP y elige herramientas; máximo 5 pasos y 8 llamadas. Nunca recibe SQL arbitrario. El dashboard también consulta MCP. El cliente oficial Python valida el endpoint público. El MCP no está registrado como plugin Sites; se usa directamente por HTTP.
La alternativa local usa FastAPI y el SDK MCP Python por stdio. Las dos implementaciones comparten definiciones de KPI y Skill.
Los secretos se guardan en Sites o .env, nunca en el navegador ni Git. RLS restringe filas; bi_tool permite solo agregados UCI públicos. No se publican identificadores de clientes. La web funciona sin el Mac. La cuota de Groq puede producir 429: el dashboard no depende del LLM.
