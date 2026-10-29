# Auditor de ventas y cancelaciones

Guía de defensa y demostración | Eva, Sacha y Andrés | 29 octubre 2026

## La idea que los tres debéis saber explicar

Nuestro sistema consulta transacciones reales de un comercio, detecta señales de cancelaciones y propone revisiones con evidencia. El usuario puede preguntar en lenguaje natural; el agente elige herramientas, consulta Supabase mediante MCP y devuelve resultados y un borrador de email. La decisión final corresponde a una persona.

## Por qué hemos ajustado el nombre

Ventas netas no equivale a beneficio. El dataset no incorpora costes de producto y operación, logística o comisiones suficientes para calcular rentabilidad. Presentarlo como auditor de ventas y cancelaciones ajusta la promesa a lo demostrado. MCP sí funciona: es el protocolo de acceso a herramientas, no una fuente de costes inexistentes.

## Qué aporta al negocio

Prioriza incidencias que merecen revisión, facilita conciliar abonos y convierte cifras en propuestas concretas. No hemos medido un ahorro real de horas ni una mejora de beneficios: son beneficios potenciales que deberían validarse con usuarios.

## Accesos para la presentación

Web: https://observatorio-retail-bi.balmyspark1.chatgpt.site/

Entrega: https://github.com/afgg030303-star/Hackathon_BI

Evidencia principal: tests/pruebas.md y tests/auditoria_29/. Reflexión vigente: Reflexion_Equipo_Auditor_Ventas.md; REFLEXION.md es su índice.

La guía describe las pruebas conservadas del 29/10. No representa una garantía de disponibilidad futura ni una nueva ejecución de todos los casos. El cierre documental no cambia el agente.


---

# 1. Demostración en 6 minutos

| Tiempo | Mostrar y explicar |
| --- | --- |

| 0:00-0:45 | Problema: revisar cancelaciones y ventas con evidencia. Aclarar que no calculamos beneficio real. |
| --- | --- |

| 0:45-1:45 | Seleccionar France, desde 2011-11-01 hasta 2011-11-30. Mostrar ventas 31.758,71 GBP, cancelaciones 1.061,20, neto 30.697,51 y 64 pedidos. |
| --- | --- |

| 1:45-2:30 | Restablecer el periodo completo 2010-12-01 a 2011-12-09. Ejecutar auditoría de France y mostrar el código M y su regla. |
| --- | --- |

| 2:30-4:00 | Escribir: Redacta un borrador de email con las alertas de Francia. Expandir consultas: herramienta, parámetros, resultado y Skill. Descargar el TXT del mismo mensaje. |
| --- | --- |

| 4:00-5:00 | Abrir tests/pruebas.md y una evidencia SQL/MCP. Explicar la comparación independiente contra CSV y un error corregido. |
| --- | --- |

| 5:00-6:00 | Cerrar con límites, aprendizaje del equipo y evolución futura con costes reales. |
| --- | --- |

## Explicación durante el chat

La IA decide qué herramienta utilizar. La Skill establece el protocolo de análisis. MCP lleva la petición al servidor; la consulta calcula cifras en Supabase. Auditorías y borradores se componen a partir del resultado estructurado para reducir invenciones. El texto es un borrador: no enviamos correos ni cambiamos datos.

## Antes de empezar

Abrir web y repositorio, probar la conexión y seleccionar fechas válidas. Tener descargados el PDF y tests/auditoria_29/borrador-agente.txt. Evitar repetir preguntas sin necesidad: Groq tiene cuota. No mostrar .env ni pantallas con claves. No usar 2018: la fuente real cubre 2010-2011.

Reparto sugerido para ensayar, no registro de aportaciones: Sacha explica negocio y alcance; Eva demuestra el flujo; Andrés explica validación y errores. Los tres deben poder contestar el conjunto.


---

# 2. Datos y cifras de control

## ¿De dónde vienen los datos y por qué son reales?

UCI Online Retail: transacciones de un comercio británico, publicadas por D. Chen en 2015, licencia CC BY 4.0. Conservamos fuente, huellas, perfil e importación. Son 541.909 líneas de transacción, no 541.909 pedidos. DOI: 10.24432/C5BW33.

## ¿Por qué no hay 2018?

La tabla activa ventas_uci va del 1 de diciembre de 2010 al 9 de diciembre de 2011. La tabla histórica ventas_superstore contiene fechas posteriores, pero es ficticia y no alimenta el agente. Se eligió UCI para cumplir datos reales. Diciembre de 2011 es parcial.

## ¿Cómo se calculan los indicadores?

Importe = Quantity × UnitPrice, en GBP. Ventas positivas: cantidad y precio positivos, sin prefijo C. Cancelaciones: importe absoluto de líneas con factura C, cantidad negativa y precio positivo. Otras cantidades negativas se separan. El neto incorpora las líneas admitidas según las reglas SQL; no se llama beneficio. Pedidos cuenta facturas de venta distintas, no líneas.

| France - noviembre 2011 | Valor comprobado CSV / sistema |
| --- | --- |

| Ventas positivas | 31.758,71 GBP |
| --- | --- |

| Cancelaciones | 1.061,20 GBP |
| --- | --- |

| Neto | 30.697,51 GBP |
| --- | --- |

| Pedidos / líneas | 64 / 1.580 |
| --- | --- |

## Calidad: conservar y explicar

Hay 135.080 líneas sin cliente y 1.454 sin descripción. No se eliminan silenciosamente. Los precios no positivos y otras anomalías se perfilan; las métricas aplican reglas explícitas. La suma bruta de todas las filas no es el KPI neto filtrado: no deben compararse como si fueran equivalentes.

Fuente: data/fuente.md, data/perfil_uci.json y data/BASE_DE_DATOS.md. Comprobación independiente: tests/auditoria_29/conciliacion_pais_mes.json. El original se distribuye en https://archive.ics.uci.edu/dataset/352/online+retail .


---

# 3. Qué hace cada componente

| Componente | Respuesta para el profesor |
| --- | --- |

| Frontend | La web muestra KPI, filtros, auditoría, chat, trazas y descarga de borradores. |
| --- | --- |

| Backend | Valida parámetros, ejecuta reglas, coordina modelo y herramientas y devuelve respuestas controladas. |
| --- | --- |

| Agente / Groq | El modelo openai/gpt-oss-20b se sirve por Groq; interpreta la petición y selecciona herramientas. No usamos una clave de OpenAI. |
| --- | --- |

| Skill | skills/auditar_ventas/SKILL.md carga instrucciones de auditoría: consultar, separar hechos e hipótesis, proponer comprobación y no inventar costes. |
| --- | --- |

| MCP | Protocolo real JSON-RPC por HTTP en /api/mcp. initialize, tools/list y tools/call están registrados en las pruebas. |
| --- | --- |

| Supabase | Aloja PostgreSQL y las 541.909 filas reales. Las consultas SQL fijas producen agregados. |
| --- | --- |

| GitHub / Sites | GitHub guarda fuente, historial y evidencias. Sites ejecuta la web cloud, que no depende del Mac. Un push no implica un nuevo despliegue. |
| --- | --- |

## Flujo que debéis poder dibujar

Usuario → frontend → backend/agente con Skill → cliente MCP → servidor MCP → funciones SQL de Supabase → resultados → respuesta y borrador descargable.

## Las seis herramientas

resumen_ventas: KPI; comparar_grupos: comparación de países o productos; comprobar_calidad: perfil de datos; auditar_anomalias: señales; redactar_borrador: comunicación propuesta; estimar_escenario: cálculo hipotético con supuesto explícito.

## ¿La Skill es otro servicio?

No. Se carga como instrucciones del sistema y su procedimiento se ejecuta mediante herramientas. La traza identifica la Skill y su SHA256; la huella permite comprobar qué instrucciones se cargaron. No sustituye la prueba funcional: por eso también conservamos resultado y descarga.


---

# 4. Alertas, acciones y límites

## ¿Qué activa una alerta?

Dos reglas de revisión: neto negativo con cancelaciones de al menos 100 GBP; o ventas positivas de al menos 1.000 GBP y cancelaciones de al menos el 20 % de esas ventas. Son umbrales heurísticos explícitos, no un modelo estadístico entrenado ni una demostración de fraude o pérdidas.

## ¿Podéis explicar una alerta con números?

France, periodo completo, código M: ventas 9.492,37 GBP, cancelaciones 9.502,86 y neto -10,49. Cumple neto < 0 y cancelaciones ≥ 100. La relación cancelaciones/ventas es aproximadamente 100,11 %. La acción es conciliar el código y sus abonos; la causa no se conoce solo con esos importes.

## ¿Por qué no afirmáis descuentos tóxicos o clientes no rentables?

El dataset no tiene los descuentos y costes necesarios. El caso inicial era una visión; la solución final se adapta a las variables reales. Una asociación o señal permite formular una hipótesis, no demostrar una causa raíz.

## ¿Qué significa cero alertas?

Que ningún grupo del alcance seleccionado cumple esas reglas. No demuestra que no existan problemas. Un periodo sin filas tampoco es una empresa sin incidencias: es ausencia de datos. Los grupos por país y producto pueden solaparse y sus alertas no se suman como pérdidas independientes.

## ¿Actúa automáticamente?

Propone revisión, responsable y siguiente comprobación; genera un borrador. No envía emails, bloquea descuentos ni altera la base. La actualización cada 60 segundos requiere la página visible: no hay vigilancia en segundo plano con el navegador cerrado ni ingesta externa continua.

## ¿Para qué sirve el escenario de costes?

Para explorar un supuesto introducido por el usuario. Sin ese dato se rechaza el cálculo. No mide beneficio real; no incorpora todos los costes, impuestos ni recuperaciones. Es una función complementaria, no la justificación del nombre del proyecto.


---

# 5. Las nueve pruebas de entrega

| Prueba | Qué evidencia existe |
| --- | --- |

| 1. Agente | Pregunta de email de Francia: selección real de redactar_borrador y respuesta. |
| --- | --- |

| 2. Skill | Instrucciones, SHA256 coincidente y procedimiento ejecutado en traza. |
| --- | --- |

| 3. MCP | initialize, catálogo de 6 herramientas, tools/call y respuesta HTTP JSON-RPC; validación con SDK. |
| --- | --- |

| 4. Base de datos | SQL COUNT = 541909, fechas y suma; captura Supabase. La captura muestra 541.9K estimadas; SQL da el exacto. |
| --- | --- |

| 5. Backend | Regla y cálculo concreto del código M de France. |
| --- | --- |

| 6. Frontend | Filtros usados, conversación y descarga real del TXT. |
| --- | --- |

| 7. Flujo completo | Misma pregunta, traza de herramientas y TXT descargado con cuerpo verificado. Hay capturas y logs; no vídeo. |
| --- | --- |

| 8. Errores | Vacíos, fechas invertidas, fuera de ámbito, escritura, proveedores y escenario sin supuesto. |
| --- | --- |

| 9. Validación BI | CSV con Decimal independiente frente al sistema: France noviembre 2011, cinco métricas coinciden. |
| --- | --- |

## Cómo defender el resultado sin exagerar

La matriz tests/pruebas.md tiene entrada, esperado, obtenido, estado, evidencia y causa/corrección. PASS acredita cada caso ejecutado. Las caídas de Groq y Supabase se simularon en entorno aislado sobre el backend real; no desconectamos producción. La cuota 429 sí se observó realmente.

## Dónde abrir la evidencia

En tests/auditoria_29/: mcp_http_real.json, sql_base.json, skill_y_mcp_navegador.json, conciliacion_pais_mes.json, recorrido.md y verificacion_descarga.json. Las capturas y borrador-agente.txt completan el recorrido. Las rutas son relativas a la raíz del repositorio.

No hemos realizado pruebas de carga ni demostrado ausencia de todo fallo posible. El indicador health verifica configuración, no garantiza disponibilidad del proveedor.


---

# 6. Decisiones y preguntas difíciles

## ¿Qué errores encontrasteis y cómo los corregisteis?

Se conservaron respuestas con un recuento inventado y un umbral añadido por el modelo. Para auditorías y borradores, el resultado se compone ahora desde datos estructurados. También se corrigieron un selector de países y el manejo de fechas invertidas. El texto libre restante requiere revisión contra la evidencia.

## ¿Por qué no dejar a la IA escribir cualquier SQL?

Usamos un catálogo acotado de herramientas y consultas fijas con parámetros validados. Evita que una pregunta arbitraria se convierta en escritura o acceso libre. Los agregados se exponen por funciones controladas; las tablas originales están protegidas por RLS. La protección no depende solo de detectar palabras DELETE o UPDATE.

## ¿Qué librería de GitHub habéis utilizado de verdad?

El SDK oficial de MCP para Python (modelcontextprotocol/python-sdk), empleado en el servidor/cliente local y validación del protocolo. La aplicación local usa FastAPI; la pública usa Vinext/Cloudflare. LIBRERIAS.md registra versiones, licencias y usos. No afirmamos haber creado esas librerías.

## ¿Por qué hay Python y TypeScript en el repositorio?

Python permite importar y validar datos y ejecutar la alternativa local. TypeScript/JavaScript sirve la aplicación pública y su flujo cloud. La arquitectura diferencia ambos caminos; la demo usa el público. Las carpetas no implican dos bases de datos distintas.

## ¿Cómo sabemos que no son datos puestos en pantalla?

Los filtros consultan el backend; MCP devuelve resultados y parámetros; SQL cuenta la tabla real; un cálculo independiente sobre el CSV reproduce las métricas de país y mes. Es la combinación de evidencias la que sustenta la afirmación.

## ¿Qué hacemos si falla Groq durante la demo?

Explicar el 429 o error visible, evitar reintentos rápidos y mostrar el panel/auditoría si Supabase sigue disponible. Abrir la traza y el TXT guardados como ejecución anterior, indicándolo expresamente. Si Supabase también falla, usar las evidencias guardadas sin presentarlas como datos en directo.


---

# 7. Reflexión y cierre del equipo

## Las cinco preguntas individuales

Cada persona debe explicar: qué aprendió; qué se lleva y cómo lo aplicará; dónde se bloqueó y cómo lo afrontó; qué aportó; qué haría diferente. Usad la reflexión elegida y palabras propias. No memoricéis como experiencia personal una propuesta que no sea cierta.

## Eva

El documento destaca la integración entre aplicación, Supabase, GitHub y publicación. Preparar un ejemplo: GitHub conserva archivos, Supabase conserva datos y el alojamiento ejecuta la web. Explicar el bloqueo de accesos y créditos y cómo el registro de contexto permite continuar.

## Sacha

El documento destaca el criterio de negocio y el ajuste de alcance: neto no es beneficio. Explicar qué datos faltarían y por qué una recomendación debe distinguir observación, hipótesis y comprobación. La corroboración técnica solicitada ya tiene evidencia en la batería de pruebas.

## Andrés

Su aportación aparece explícitamente como propuesta para confirmar. Debe validar o corregirla antes de defenderla. Para preparar la parte de validación: explicar France/noviembre, por qué cero alertas no es ausencia de riesgo y un caso de error con resultado esperado.

## Reflexión colectiva

Acordar entre los tres qué aprendisteis juntos, qué os lleváis, bloqueos y resolución, cómo escuchasteis y cuestionasteis a la IA y qué cambiaríais. Hechos comunicados: todos habéis aportado; agotasteis créditos y tuvisteis que continuar más tarde; integrar herramientas resultó difícil. No se inventan tiempos de trabajo ni participación individual.

## Compromisos para acordar

Mantener: contrastar las cifras con evidencias. Cambiar: comprobar accesos y datos antes de ampliar funciones. Experimentar: incorporar costes reales y validar márgenes con negocio. Son propuestas para vuestro acuerdo, no compromisos ya confirmados.

## Frase de cierre

Hemos aprendido a ajustar una promesa de IA a los datos disponibles. Entregamos un auditor de ventas y cancelaciones con herramientas y pruebas verificables, que ayuda a orientar decisiones y mantiene a la persona responsable de actuar.
