# Batería de pruebas de entrega
Ejecuciones 28–29/10/2026. Resultados reproducibles en los archivos citados. PASS significa caso ejecutado, no garantía general.

| Componente | Entrada / esperado | Observado y evidencia | Estado |
|---|---|---|---|
| Agente | Auditar Francia, elegir herramientas | auditar_anomalias con France; agente_auditor_final.json | PASS |
| Skill | No confundir neto y beneficio | beneficio_limites_retest.json: consulta resumen y explica costes ausentes | PASS |
| MCP | Inicializar, listar y ejecutar | 6 herramientas; cliente oficial; resultados_entrega.json y auditoria_mcp_local.json | PASS |
| Base de datos | Dataset real completo | 541909 filas conciliadas; carga_uci.json; 0 filas crudas para anon en seguridad_rls.json | PASS |
| Backend | Auditoría y escenario70% | 4108 grupos, 40 alertas; Francia resultado estimado50603.323; resultados_entrega.json | PASS |
| Frontend | Seleccionar France, actualizar, abrir escenario y borrador | 197403.90 neto; código M; escenario70% y borrador visibles; auditoria_web.png y interfaz_verificada.md | PASS casos realizados |
| Flujo completo | Web/API → Groq → MCP → Supabase → evidencia | agente_auditor_final.json; respuesta del modelo y consulta real | PASS |
| Errores | Fecha imposible, rango invertido, coste negativo, sin datos, SQL arbitrario | 422, cero filas y error MCP controlado; resultados_entrega.json. Fallo DB simulado503 sin secreto: pruebas_api_local.txt | PASS |
| Validación BI | Comparar CSV independiente con SQL | script recorre CSV completo con Decimal: 40 señales,4108 grupos y KPI de Francia coinciden | PASS |

## Ejecución y archivos
`python tests/validar_publico.py` hace la comparación independiente y consume dos consultas de Groq. `node --test tests/unit/audit.test.mjs`: 4 pruebas correctas. `python -m pytest tests/unit/test_api_local.py -q`: 4 pruebas correctas, con aviso de deprecación de dependencias. No se ocultan los avisos en el log.

## Errores encontrados y correcciones
1. La primera respuesta inventó1557 líneas de cancelación: chat_publico.json. Se reforzó Skill. Otra respuesta añadió un umbral10% no presente en la regla: agente_auditor_0.json. Ahora auditorías y borradores se componen directamente desde evidencia estructurada; el LLM sigue seleccionando herramientas. Esto evita esos añadidos en dichas salidas, no garantiza infalibilidad de todo texto libre.
2. Selector de países con etiquetas option incompletas: la prueba de navegador no podía seleccionar France. Se reconstruyó con todos los países del CSV; selección y filtro comprobados.
3. Fechas inválidas devolvían503; ahora422, incluidos 2011-02-30 y rango invertido.
4. Groq429 en la segunda pregunta de la batería: se conserva agente_auditor_1.json y el FAIL original en resultados_entrega.json. La repetición posterior beneficio_limites_retest.json devuelve200 y reconoce que no se puede calcular beneficio. No se borra el fallo original. Auditoría, panel y borrador siguen funcionando sin Groq.
5. Errores de lectura de la pestaña en la herramienta de revisión final: la comprobación visual previa y su captura se conservaron; la verificación posterior del agente se hizo mediante API pública.

## Seguridad y límites
RLS bloquea lectura de filas y escritura anónimas. Prueba de escritura con rollback incondicional: seguridad_rls.json. Las funciones públicas solo devuelven agregados UCI. No se ha probado carga masiva, usuarios concurrentes ni disponibilidad continua. Refresco60s requiere página visible; no se ha medido ahorro de tiempo comercial ni precisión causal. health indica configuración, no disponibilidad garantizada.
