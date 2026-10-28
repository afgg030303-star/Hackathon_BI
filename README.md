# Hackathon_BI — Auditor agéntico de BI

Fase 1: estructura del proyecto y prueba de lectura en PostgreSQL (Supabase).
El agente, el servidor MCP y el frontend se implementarán en fases posteriores.

## Ejecución (macOS / Linux)

Desde la raíz del proyecto, con Python 3.11 o superior:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r 02_backend_y_mcp/requirements.txt
```

Configura `DATABASE_URL` en `.env` con la contraseña real de Supabase.
Si la contraseña contiene caracteres reservados de una URL, debe codificarse
como componente URL. No subas `.env` a GitHub. `OPENAI_API_KEY` no se utiliza
en esta fase y puede conservar el placeholder.

```bash
python 02_backend_y_mcp/test_db.py
```

El script carga `.env` desde la raíz independientemente del directorio de ejecución;
las variables ya exportadas en el entorno tienen prioridad. Utiliza TLS, una sesión
de solo lectura, un límite de conexión de 10 segundos y de consulta de 15 segundos.
Ejecuta `SELECT COUNT(*) FROM ventas_superstore;` y muestra el total de filas.
Finaliza con código 0 si la consulta funciona y con 1 ante errores.
Una tabla vacía genera una advertencia, aunque la conexión funcione.
La tabla debe existir previamente y ser accesible por el usuario configurado.

## Estructura

- `00_prompts_ia`: instrucciones y prompts del proyecto.
- `01_investigacion_y_datos`: investigación y documentación de datos.
- `02_backend_y_mcp`: dependencias y prueba de conexión.
- `03_frontend`: reservado para la interfaz.
- `04_pruebas_y_reflexion`: reservado para evidencias y reflexión.

## Estado de validación

La conexión real se verificó el 28/10/2026 con TLS mediante Session pooler.
La tabla existente ventas_superstore tiene 9.800 filas. No se han modificado datos.
El segundo ordenador debe configurar su propio .env y verificar la conexión.
Las dependencias se dejan sin fijar según la lista solicitada; convendrá registrar
las versiones del entorno una vez validado para reproducir la entrega.

## Trabajo en equipo

Leer [COLABORACION.md](COLABORACION.md) y [ESTADO_PROYECTO.md](ESTADO_PROYECTO.md). Las instrucciones de Codex están en [AGENTS.md](AGENTS.md). Repositorio compartido: https://github.com/afgg030303-star/Hackathon_BI .

Antes de probar la tabla, puede verificarse la conexión sin depender del dataset:

```bash
python 02_backend_y_mcp/comprobar_supabase.py
```

El alcance de rentabilidad del planteamiento inicial está pendiente de corregir: el CSV local no contiene beneficio ni descuento y Superstore es ficticio. Ver [PLAN_DE_TRABAJO.md](PLAN_DE_TRABAJO.md).
