# Demostración en cinco minutos
1. **Problema (40s):** priorizar anomalías de ventas y pasar a una acción revisable. Power BI/Tableau ya tienen alertas: nuestro foco es diálogo con herramientas y evidencia, no afirmar que sean pasivos.
2. **Datos (40s):** mostrar UCI, licencia CC BY4.0, 541909 filas y conciliación. Neto no es beneficio. Costes solo en escenario explícito.
3. **Arquitectura (40s):** enseñar diagrama y Skill. El LLM consulta catálogo y elige herramienta MCP; PostgreSQL calcula, no el modelo.
4. **Demo (100s):** seleccionar France y actualizar. Neto197403.90 GBP. Mostrar la señal del código M, su conciliación propuesta y borrador descargable. Preguntar «Audita las anomalías de Francia y propón acciones». Abrir evidencias. Si Groq devuelve429, mostrar el mensaje, la evidencia guardada y ejecutar la auditoría determinista que sigue disponible; no fingir una respuesta en vivo.
5. **Escenario y pruebas (40s):** introducir coste supuesto70%. Explicar que NO es dato real. Mostrar tests/resultados_entrega.json, comparación independiente del CSV y prueba de fechas inválidas422.
6. **Reflexión (40s):** créditos agotados y dificultad de coordinar GitHub/Supabase. Qué se aprendió, qué cambiaría cada persona. Revisar antes REFLEXION.md.

## Preguntas que todos deben poder responder
- ¿Por qué es agente? Decide herramientas y parámetros, ejecuta MCP, usa una Skill y devuelve evidencia. La auditoría por reglas y el borrador son procedimientos deterministas; no se atribuyen razonamientos mágicos.
- ¿Por qué no beneficio? No hay costes observados; la simulación está separada.
- ¿Por qué no causa raíz demostrada? Faltan motivos de cancelación y evidencia causal. Proponemos investigación y validación.
- ¿Trabaja siempre? Consulta la base en cada ejecución; refresca cada60s con página visible. Sin navegador no hay vigilancia programada ni nueva ingesta externa.
- ¿Qué acción ejecuta? Genera el informe, alertas y borrador; no manda emails ni cambia precios.
- ¿Qué errores encontramos? Selector mal formado, fecha inválida503 corregida422, recuento inventado por LLM, cuota429. Evidencias conservadas.
- ¿Cómo colaborar? GitHub versiona código; Supabase almacena datos; Sites ejecuta la web. Push/pull explícitos y secretos separados.
