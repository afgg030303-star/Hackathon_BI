# Estado — primer prototipo, 28/10/2026

Rama de desarrollo: desarrollo/agente-bi. Cada bloque se sube a GitHub. El usuario prioriza construir ya y no quiere API de pago.

## Implementado
- Carga transaccional UCI a tabla nueva ventas_uci: 541.909 filas y suma original 9.747.747,934 GBP conciliadas. ventas_superstore se conserva.
- PostgreSQL con consultas de solo lectura y parámetros; 3 herramientas MCP; cliente MCP stdio real.
- Skill cargada por el agente, bucle de herramientas con Ollama local, FastAPI e interfaz de KPI/chat.
- Ollama oficial instalado en .local-runtime (excluido de Git); modelo qwen3:4b-instruct en descarga. No hay API de pago.

## Validación en curso
Servidor MCP, API, interfaz y agente en prueba. No dar por pasado el flujo completo hasta consultar las evidencias finales de 04_pruebas_y_reflexion. No requiere OPENAI_API_KEY. Faltan documentación final y pruebas del modelo descargado.

## Equipo
Los cambios locales de EJERCICIO 5 son visibles para Codex al leer archivos; no hay sincronización automática con el otro ordenador. Para el relevo, traer la rama de desarrollo y leer AGENTS.md. Configurar .env local sin publicar contraseñas. Ejecutar iniciar.command una vez preparado el entorno.
