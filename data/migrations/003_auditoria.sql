-- Reglas explícitas: señales para investigar, nunca prueba de pérdida/causa.
CREATE OR REPLACE FUNCTION public.bi_audit(desde date DEFAULT '2010-12-01', hasta date DEFAULT '2011-12-09', pais text DEFAULT NULL)
RETURNS jsonb LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,public SET statement_timeout='15s' AS $$
DECLARE result jsonb;
BEGIN
 IF desde IS NULL OR hasta IS NULL OR desde>hasta OR hasta>='9999-12-31'::date OR length(pais)>80 THEN RAISE EXCEPTION 'Periodo inválido'; END IF;
 WITH base AS (
 SELECT *,quantity*unit_price AS importe,upper(invoice_no) LIKE 'C%' AS cancelacion
 FROM public.ventas_uci WHERE invoice_date>=desde AND invoice_date<hasta+1 AND (pais IS NULL OR country=pais)
 ), groups AS (
 SELECT CASE WHEN grouping(stock_code)=1 THEN 'pais' ELSE 'producto' END AS dimension,
 CASE WHEN grouping(stock_code)=1 THEN country ELSE stock_code END AS grupo,
 count(*) AS lineas,
 COALESCE(sum(importe) FILTER(WHERE quantity>0 AND unit_price>0 AND NOT cancelacion),0) AS ventas_positivas,
 COALESCE(-sum(importe) FILTER(WHERE quantity<0 AND unit_price>0 AND cancelacion),0) AS cancelaciones,
 COALESCE(sum(importe) FILTER(WHERE unit_price>0 AND (quantity<0 OR (quantity>0 AND NOT cancelacion))),0) AS importe_neto
 FROM base GROUP BY GROUPING SETS ((country),(stock_code))
 ), scored AS (
 SELECT *,CASE WHEN ventas_positivas>0 THEN round(100*cancelaciones/ventas_positivas,2) END AS tasa_cancelacion,
 CASE WHEN importe_neto<0 AND cancelaciones>=100 THEN 'neto_negativo' ELSE 'cancelacion_elevada' END AS regla
 FROM groups WHERE (importe_neto<0 AND cancelaciones>=100) OR (ventas_positivas>=1000 AND cancelaciones/NULLIF(ventas_positivas,0)>=0.2)
 ), top_alerts AS (SELECT * FROM scored ORDER BY cancelaciones DESC,dimension,grupo LIMIT 12)
 SELECT jsonb_build_object('fuente','UCI Online Retail','moneda','GBP','desde',desde,'hasta',hasta,'pais',pais,
 'consultado_en',clock_timestamp(),'lineas_analizadas',(SELECT count(*) FROM base),
 'grupos_analizados',(SELECT count(*) FROM groups),'alertas_activas',(SELECT count(*) FROM scored),
 'alertas',COALESCE((SELECT jsonb_agg(to_jsonb(top_alerts)) FROM top_alerts),'[]'::jsonb),
 'reglas','Neto negativo y cancelaciones >=100 GBP; o cancelaciones/ventas >=20% con ventas >=1000 GBP. Umbrales heurísticos, no estadísticos.',
 'limites','Grupos país y producto pueden solaparse; no sumar sus importes. No demuestra pérdidas ni causas. Sin costes, descuentos o logística. Hasta 12 alertas ordenadas por importe cancelado.') INTO result;
 RETURN result;
END $$;
REVOKE ALL ON FUNCTION public.bi_audit(date,date,text) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.bi_audit(date,date,text) TO anon,authenticated;
