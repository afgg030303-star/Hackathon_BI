# Dos ordenadores, un proyecto

Repositorio: https://github.com/afgg030303-star/Hackathon_BI
Base de datos: https://supabase.com/dashboard/project/gvsxekaqeodljocyqkfo/settings/general

GitHub conserva archivos e historial. Supabase conserva las tablas. Cada backend local conecta con la misma base mediante su propio .env. No es necesaria una integración de despliegue GitHub–Supabase para este flujo.

## Acceso inicial
La persona propietaria del repositorio debe añadir las cuentas de ambas integrantes como colaboradoras y cada una debe aceptar su invitación. La conexión GitHub de este chat usa 872587-ai y en la comprobación inicial solo tiene permiso de lectura. El Git local puede usar otra cuenta: comprobar también la autenticación de GitHub Desktop o Git en cada equipo.

## Segundo ordenador
1. Clonar el repositorio con GitHub Desktop (File → Clone repository → URL), o con:

```bash
git clone https://github.com/afgg030303-star/Hackathon_BI.git
cd Hackathon_BI
```

2. Abrir esa carpeta en Codex. Pedir: «Lee AGENTS.md, ESTADO_PROYECTO.md y COLABORACION.md; revisa la rama y los cambios pendientes antes de continuar».
3. Crear .env a partir de .env.example únicamente si no existe. Introducir la URI real de Supabase localmente. No enviarla por chat ni incluirla en GitHub.
4. Preparar Python 3.13 y un entorno virtual; instalar las dependencias mínimas con `python -m pip install -r 02_backend_y_mcp/requirements-db.txt`. Verificar primero la conexión con comprobar_supabase.py; test_db.py además requiere la tabla ventas_superstore.

## Trabajo simultáneo
Acordar tareas distintas: equipo A backend/MCP/datos, equipo B frontend/documentación. Las migraciones y cargas de datos las ejecuta una sola persona.

Al empezar una tarea, con el directorio limpio:

```bash
git switch main
git pull --ff-only origin main
git switch -c equipo-a/nombre-tarea
```

Usar equipo-b/nombre-tarea en el otro ordenador. No reutilizar un nombre si ya existe.

Al terminar, pedir a Codex que revise archivos y secretos, registre el avance, haga commit y push de esa rama y abra un pull request. Revisar e integrar el PR; después la otra persona actualiza main. Los cambios de una rama no aparecen en main hasta que se integra.

Si hay cambios locales pendientes, guardarlos en la rama actual antes de cambiar de rama. Si Git indica conflictos, pedir a Codex resolverlos conservando el trabajo de ambas; no usar force push ni reset --hard.

## Contexto compartido
AGENTS.md contiene instrucciones persistentes para Codex. ESTADO_PROYECTO.md es el relevo. 00_prompts_ia conserva registros de sesiones. GitHub sincroniza estos archivos, no el historial interno de las aplicaciones. Añadir exportaciones de conversaciones cuando estén disponibles, revisadas para eliminar secretos.

Fuente sobre AGENTS.md: https://learn.chatgpt.com/docs/agent-configuration/agents-md

## Conexión Supabase
Abrir el proyecto indicado y su panel Connect. Copiar la URI PostgreSQL en el .env local. Para redes sin IPv6, usar la URI Session pooler que muestra Supabase; no adivinar host, región ni usuario. La contraseña es la de la base de datos, no una API key de Supabase. La clave del proveedor LLM se configurará después para el agente.

Ejecutar con el entorno de Python activado:

```bash
python 02_backend_y_mcp/comprobar_supabase.py
```

La prueba usa TLS y solo lectura, identifica el proyecto mediante el host/usuario de conexión y lista tablas públicas. No modifica datos. Una conexión correcta no implica que el dataset esté importado.

Fuente sobre conexiones Supabase: https://supabase.com/docs/guides/database/connecting-to-postgres
