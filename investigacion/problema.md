# Problema, divergencia y convergencia
Responsable comercial de retail: necesita priorizar qué anomalías investigar y preparar acciones sin escribir SQL. Propuesta: detectar señales en ventas/cancelaciones, explicitar hipótesis, recomendar comprobaciones y redactar comunicaciones revisables.

## Cinco alternativas
Puntuación de diseño del equipo asistida por IA, no medición de mercado. Escala 1–5 (5 mejor), pesos iguales.

| Problema BI | Datos disponibles | Verificabilidad | Viabilidad en 5h | Utilidad prevista | Total |
|---|---:|---:|---:|---:|---:|
| Ventas y cancelaciones anómalas | 5 | 5 | 5 | 4 | 19 |
| Previsión de demanda | 4 | 3 | 2 | 5 | 14 |
| Márgenes reales por producto | 1 | 1 | 2 | 5 | 9 |
| Segmentación de clientes | 3 | 4 | 3 | 4 | 14 |
| Eficiencia logística | 1 | 1 | 2 | 4 | 8 |

Elegimos ventas y cancelaciones por tener transacciones reales conciliables. Conservamos la visión de rentabilidad mediante un escenario opcional con costes supuestos, separado de resultados reales. No hay ciudades, costes logísticos, descuentos porcentuales ni categorías para reproducir las conclusiones del pitch.

## Objetivos y KPI
- Consultar 541909 transacciones sin alterar el original.
- Ventas positivas, cancelaciones, ajustes negativos, neto y pedidos distintos.
- Auditar todos los grupos de país y producto, no solo los de mayor venta.
- Señales: neto negativo y cancelaciones >=100 GBP; o cancelaciones/ventas >=20% con ventas >=1000 GBP. Umbrales heurísticos elegidos para priorizar revisión; no inferencia estadística ni causal.
- Acción: conciliar facturas, distinguir mercancías de ajustes contables, recopilar motivos y volver a medir en periodos equivalentes. Borrador no enviado.
- Métricas futuras de valor: tiempo hasta una decisión revisada y porcentaje de alertas útiles. No se han medido todavía.

## Decisiones cuestionadas
Superstore no satisface el requisito de datos reales; UCI sí. Neto negativo no equivale a pérdida contable. Una correlación o tasa elevada no demuestra descuento tóxico. Las alertas país/producto se solapan: no sumar sus importes. Un escenario de coste no transforma un supuesto en dato observado.
