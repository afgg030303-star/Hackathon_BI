# Pruebas ejecutadas — 28/10/2026

| Componente | Esperado | Observado / evidencia | Estado |
|---|---|---|---|
| Agente | Elegir herramienta y consultar Francia | resumen_ventas con pais France, 197403.90 GBP; agente_groq_real.json | PASS |
| Skill | Exigir datos y no beneficio | respuesta con periodo, datos MCP y limitación de costes; publicacion_v2.json | PASS caso probado |
| MCP público | Inicializar, listar y ejecutar con SDK oficial | 3 herramientas, isError false; mcp_publico.json | PASS |
| Base de datos | Datos UCI completos conciliados | 541909 filas; carga_uci.json | PASS |
| Backend | Calcular KPI correctos | Francia positivo209715.11, cancelación12311.21, neto197403.90 | PASS |
| Frontend | Servir página pública | GET / HTTP200; interacción visual no validada en esta sesión | PARCIAL |
| Flujo completo | Pregunta HTTP → Groq → MCP → Supabase → respuesta | chat público HTTP200 con evidencia; publicacion_v2.json | PASS API |
| Errores | Sin datos y fechas invertidas | NO_EXISTE: 0 filas; fechas invertidas503 genérico | PASS rechazo; mejorar código a422 |
| Validación BI | Neto conciliado con base | Francia197403.90 en consulta local y cloud; carga conciliada con origen | PASS caso probado |

## Error encontrado y mitigación
La primera respuesta cloud inventó un recuento de 1557 líneas de cancelaciones aunque la herramienta solo devolvía importes. Se conserva chat_publico.json como evidencia del error. Se reforzó la Skill para no confundir importe con recuento ni inventar cifras. La repetición publicacion_v2.json no contiene ese recuento. Esta prueba no garantiza que un LLM nunca alucine: revisar las evidencias antes de tomar decisiones.

## Límites de la validación
No se ha realizado prueba de carga ni comprobación visual de todas las pantallas. Cuotas Groq y caídas externas siguen siendo posibles. health indica configuración del modelo, no garantiza disponibilidad de proveedor ni de base. La reflexión personal sigue pendiente.
