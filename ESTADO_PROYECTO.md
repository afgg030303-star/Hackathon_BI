# Estado de entrega — 29/10/2026
Web pública: https://observatorio-retail-bi.balmyspark1.chatgpt.site
Rama: desarrollo/agente-bi. Datos reales UCI:541909 filas en Supabase. Cloud Groq → MCP HTTP → funciones SQL; alternativa Python con MCP stdio. Seis herramientas y Skill real.
Implementado: KPI, filtros corregidos, auditoría de todos los grupos,40 señales globales, hipótesis y acciones, borrador no enviado, escenario de coste explícito. Refresco60s con página visible. Sin vigilancia cerrada ni ingesta externa.
Versión Sites5, fuente 425dcf09a79916ba6ec7e456c296ba07fd178053. web_publica conserva fuente reproducible sin secretos.
Pruebas: tests/pruebas.md; conservar fallos iniciales y repeticiones. Reflexión: propuesta basada en relato de Eva sobre Sacha, Andrés y Eva; deben revisar sus apartados y consensuar reflexión común. No afirmar revisión humana realizada.
Contexto: enlace ChatGPT leído completo; revisaba un commit antiguo y otra rama local sin publicar. No se importó ese código ni se atribuyeron sus pruebas. GitHub guarda archivos, Supabase datos y Sites ejecuta web; push/pull no son automáticos.

Auditoría29: tests/pruebas.md reestructurado con seis columnas y nueve pruebas; evidencia de Skill/SHA, tráfico MCP, SQL/captura Supabase, CSV país/mes/pedidos, descarga del mismo chat, errores de proveedor aislados. Rechazo meteorológico y SQL explícito en servidor cloud. Detalles en tests/auditoria_29/HALLAZGOS.md.
