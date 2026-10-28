# Fuentes y decisión de datos

Consultadas el 28 de octubre de 2026.

- Tableau, tutorial oficial: https://help.tableau.com/current/guides/get-started-tutorial/en-us/get-started-tutorial-connect.htm . Describe Superstore como una empresa ficticia.
- Tableau, datos de ejemplo: https://public.tableau.com/app/learn/sample-data . Confirma el carácter ficticio de Superstore Sales.
- UCI, catálogo oficial: https://archive.ics.uci.edu/datasets?search=Online+Retail . Describe Online Retail como transacciones de un comercio online del Reino Unido, entre 01/12/2010 y 09/12/2011.
- Ficha objetivo del dataset: https://archive.ics.uci.edu/dataset/352/online+retail . La apertura directa falló por timeout durante esta revisión; verificar licencia, cita y descarga en la fase de datos. No confundir con Online Retail II (dataset 502).

## Comparación
Superstore permite ejemplos de BI, pero no justifica el requisito estricto de transacciones reales. Además, el archivo local carece de beneficio y descuento. UCI permite investigar concentración de ventas y cancelaciones con procedencia identificable. No contiene costes para medir beneficio. Recomendación: UCI Online Retail, con análisis descriptivo y recomendaciones formuladas como hipótesis.

No se ha descargado ni importado todavía el dataset recomendado. No se ha verificado la procedencia exacta del train.csv local.
