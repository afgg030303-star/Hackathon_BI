# Fuente, licencia y calidad
Chen, D. (2015). **Online Retail** [Dataset]. UCI Machine Learning Repository. DOI: https://doi.org/10.24432/C5BW33 . [Ficha oficial](https://archive.ics.uci.edu/dataset/352/online+retail). Licencia **CC BY 4.0**, atribución conservada aquí.

Transacciones reales de un comercio online británico, 01/12/2010–09/12/2011. Moneda GBP. `ventas_uci.csv.gz` es una transformación del XLSX original: nombres normalizados, fechas ISO y source_row para trazabilidad; se mantienen todas las filas, incluidos nulos y duplicados.

| Comprobación | Resultado |
|---|---:|
| Filas | 541909 |
| Clientes ausentes | 135080 |
| Descripciones ausentes | 1454 |
| Precios no positivos | 2517 |
| Cantidades negativas | 10624 |
| Líneas con prefijo C | 9288 |
| Suma bruta original Quantity × UnitPrice | 9747747.934 GBP |

La suma neta analítica difiere del importe bruto porque se excluyen precios no positivos y otras líneas inválidas para el KPI. No se eliminan de la base. Véase perfil_uci.json con hashes y tests/carga_uci.json con conciliación. La ficha genérica puede indicar ausencia de nulos; el perfil calculado sí identifica campos vacíos.

Sin costes, descuentos por transacción, logística ni categorías. Existen códigos contables: no tratar todo stock_code como mercancía. Diciembre de 2011 es parcial. Cancelación no acredita devolución física. Los identificadores de clientes no se exponen por el endpoint público.

`train.csv` procede del material inicial Superstore y no alimenta la aplicación. Es histórico, no evidencia de rentabilidad real.
