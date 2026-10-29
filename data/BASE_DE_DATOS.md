# PostgreSQL en Supabase
Proyecto compartido gvsxekaqeodljocyqkfo. Nunca recrearlo para el segundo ordenador.

`ventas_uci`: source_row (PK), invoice_no, stock_code, description nullable, quantity integer, invoice_date timestamp, unit_price numeric, customer_id nullable, country. Índices por fecha y país. `bi_dataset_metadata`: hash, recuento, suma e instante de importación. `ventas_superstore`: tabla histórica conservada.

Migraciones: 001 crea tablas/RLS; 002 crea bi_tool (resumen, ranking, calidad); 003 crea bi_audit (agregados y señales). Ejecutar una sola vez en orden, con administrador. El importador aplica 001 y no sustituye datos existentes. Comando: `python backend/importar_uci.py` con DATABASE_URL local. Las migraciones 002 y 003 pueden ejecutarse en el SQL Editor de Supabase copiando su contenido completo.

Las funciones SECURITY DEFINER tienen SQL fijo, search_path definido, límites y timeout; conceden ejecución a anon/authenticated para agregados del dataset público. RLS sin políticas impide filas crudas a anon. No hay herramientas de escritura ni SQL arbitrario. El cliente cloud usa la clave publicable, no contraseña ni service_role.

El backend Python alternativo usa DATABASE_URL y transacciones de lectura: esto NO equivale a un usuario de base de datos con permisos restringidos. No publicar esa URL. TLS require cifra la conexión local, pero no exige por sí solo verificación de identidad del servidor. Cloud consulta por HTTPS con validación estándar. Son límites documentados, no garantías adicionales inventadas.
