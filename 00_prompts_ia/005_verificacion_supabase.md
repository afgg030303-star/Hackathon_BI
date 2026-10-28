# Sesión 5 — conexión Supabase

Petición literal del usuario: «ya lo he puesto» (credencial introducida en .env local).

Resumen de actuaciones: prueba inicial fallida; diagnóstico sin mostrar secretos identificó fallo DNS de conexión directa. Se consultó Connect en el proyecto Supabase y se obtuvo Session pooler. Se actualizó únicamente la URI local manteniendo la contraseña, sin mostrarla. Ambas pruebas pasaron: conexión TLS y tabla ventas_superstore con 9.800 filas. Se actualizó plantilla sin secretos, README y estado del proyecto, y se guardaron evidencias. No se modificó la base de datos.

Siguiente paso: el segundo ordenador clona/actualiza main, configura .env local y comprueba acceso. Continuar posteriormente con la decisión de datos documentada; la conexión exitosa no convierte Superstore en datos reales.
