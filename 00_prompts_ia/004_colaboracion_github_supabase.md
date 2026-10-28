# Sesión 4 — colaboración

## Petición literal del usuario
«Vale, antes de nada, como tenemos dos ordenadores que tienen codex, necesito que me ayudes a juntar GitHub con la base de datos que tengo en Supabase y que todo lo que hagas quede en el agente y que a la vez esté en GitHub para poder ir trabajando las dos a la vez. Ayúdame en esto, porfa, antes de nada.»

## Destinos elegidos por el usuario
- https://github.com/afgg030303-star/Hackathon_BI
- https://supabase.com/dashboard/project/gvsxekaqeodljocyqkfo/settings/general

## Resumen del trabajo y decisiones
Se comprueba que origin/main solo contiene un README inicial. Se inicializa Git sobre la carpeta existente y se conserva el historial remoto. Se prepara AGENTS.md, guía de colaboración, ejemplo de variables de entorno, carpeta de migraciones y prueba de conexión independiente de la tabla.

El conector GitHub usa 872587-ai y reporta push=false. La publicación requiere una cuenta con escritura. Los chats no se sincronizan solos: el contexto compartido se registra en archivos. La base de datos es una única instancia compartida, las credenciales se configuran localmente en cada equipo.

Ver ESTADO_PROYECTO.md para el resultado efectivo de publicación y conexión. No se ha desarrollado todavía el agente de BI.
