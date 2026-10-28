# Agente coordinador

Implementación ejecutable: [backend/agent.py](../backend/agent.py). Usa Qwen local con Ollama; descubre herramientas mediante ClientSession, el modelo las selecciona, el cliente las ejecuta por MCP stdio, y el modelo redacta la respuesta. Skill: [auditar_ventas](../skills/auditar_ventas/SKILL.md). No usa OpenAI ni una API de pago.
