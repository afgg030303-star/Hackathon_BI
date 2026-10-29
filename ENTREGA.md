# Entrega final - Auditor de ventas y cancelaciones

Equipo: Eva, Sacha y Andrés. Repositorio: https://github.com/afgg030303-star/Hackathon_BI
Web: https://observatorio-retail-bi.balmyspark1.chatgpt.site/

| Requisito del profesor | Carpeta o documento de entrega | Evidencia / alcance |
|---|---|---|
| Investigación del problema y fuentes | investigacion/problema.md y mercado.md | Alternativas, convergencia y fuentes; sin entrevistas inventadas |
| Dataset real y base de datos | data/ventas_uci.csv.gz, fuente.md, BASE_DE_DATOS.md, migrations/ | UCI, 541909 filas, PostgreSQL/Supabase, carga conciliada |
| Arquitectura agéntica | arquitectura/README.md; agents/README.md | Flujo cloud y alternativa local |
| Agente, Skill, MCP y código | agents/, skills/, config/, backend/, frontend/, web_publica/ | web_publica es la fuente del despliegue actual; Python es la alternativa local |
| Librería de GitHub | LIBRERIAS.md | SDK MCP y otras dependencias con uso documentado |
| Ejecución | README.md y .env.example | Configuración sin credenciales; publicar y hacer push son operaciones distintas |
| Batería de pruebas | tests/pruebas.md; tests/auditoria_29/ | Nueve casos con entrada, esperado, obtenido, estado, evidencia y causa/corrección |
| Reflexión individual y colectiva | REFLEXION.md enlaza Reflexion_Equipo_Auditor_Ventas.md | Única reflexión elegida; confirmar propuestas indicadas dentro |
| Registro de IA y continuidad | 00_prompts_ia/; AGENTS.md; ESTADO_PROYECTO.md | Resúmenes identificados; no exportación íntegra automática de chats |
| Defensa | output/pdf/Guia_defensa_auditor_ventas.pdf; DEFENSA.md | Guion, respuestas, cifras y plan de contingencia |

## Alcance definitivo
Auditor de ventas y cancelaciones asistido por IA. No es una medición de rentabilidad: faltan costes reales. MCP transporta consultas y resultados; no aporta campos ausentes del dataset. La simulación de costes sigue siendo un escenario hipotético complementario.

## Preparación humana pendiente
Confirmar el apartado propuesto de Andrés y acordar la reflexión colectiva. Ensayar el recorrido en la web. No se atribuye al equipo una revisión personal no comunicada ni se garantiza disponibilidad futura de proveedores.

## Conservación
El código del agente y la web se mantienen sin cambios en este cierre documental. Los archivos históricos identificados como Superstore y los errores iniciales se conservan para explicar las decisiones y la evolución; no son la fuente actual ni pruebas vigentes aprobadas. Las nueve pruebas acreditan los casos ejecutados, no todo comportamiento posible.
