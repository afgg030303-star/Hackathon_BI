# Librerías y adaptación
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk), mcp1.30.0, MIT: FastMCP adaptado a seis herramientas BI en backend/mcp_server.py; ClientSession/stdio en backend/mcp_client.py. También se utiliza el cliente Streamable HTTP oficial para probar el servidor cloud en tests/validar_publico.py. No se ha modificado el código de la librería.
- [FastAPI](https://github.com/fastapi/fastapi), versión fijada en backend/requirements.txt, MIT: validación de entradas y API local, rutas de informe, auditoría y chat.
- [Vinext](https://github.com/cloudflare/vinext): infraestructura de rutas cloud; versión exacta y dependencias transitivas fijadas en web_publica/package-lock.json. El starter conserva sus licencias. Protocolo JSON-RPC cloud implementado en nuestro backend y comprobado con SDK MCP oficial.
- httpx, psycopg2, pydantic y openpyxl: HTTP, SQL parametrizado, validación y lectura del XLSX. Versiones en requirements.txt.

La librería MCP está adaptada al problema real: nombres, esquemas, validaciones, consultas y política de lectura propios. No se entrega simplemente un enlace a GitHub.
