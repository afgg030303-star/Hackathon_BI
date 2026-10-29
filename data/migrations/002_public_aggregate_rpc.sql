-- Solo agregados del dataset público UCI; sin SQL arbitrario ni acceso a clientes.
CREATE OR REPLACE FUNCTION public.bi_tool(tool_name text, tool_args jsonb DEFAULT '{}'::jsonb)
RETURNS jsonb LANGUAGE plpgsql SECURITY DEFINER SET search_path = pg_catalog, public SET statement_timeout = '15s' AS $$
DECLARE d date := COALESCE((tool_args->>'desde')::date,'2010-12-01'::date);
 h date := COALESCE((tool_args->>'hasta')::date,'2011-12-09'::date);
 p text := tool_args->>'pais'; dim text := COALESCE(tool_args->>'dimension','pais');
 n integer := COALESCE((tool_args->>'limite')::integer,8); result jsonb; ctx jsonb;
BEGIN
 IF d>h OR h>='9999-12-31'::date OR length(p)>80 OR n<1 OR n>20 OR dim NOT IN ('pais','producto','mes') THEN RAISE EXCEPTION 'Parámetros inválidos'; END IF;
 IF tool_name NOT IN ('resumen_ventas','comparar_grupos','comprobar_calidad') THEN RAISE EXCEPTION 'Herramienta desconocida'; END IF;
 ctx := jsonb_build_object('fuente','UCI Online Retail','moneda','GBP','desde',d,'hasta',h,'pais',p,'limites','Importe neto no es beneficio; no hay costes. Diciembre 2011 es parcial.');
 IF tool_name='comprobar_calidad' THEN
 SELECT jsonb_build_object('filas',count(*),'fecha_min',min(invoice_date),'fecha_max',max(invoice_date),'sin_cliente',count(*) FILTER(WHERE customer_id IS NULL),'importe_bruto_origen',sum(quantity*unit_price)) INTO result FROM public.ventas_uci;
 RETURN jsonb_build_object('fuente','UCI Online Retail','perfil',result);
 END IF;
 IF tool_name='resumen_ventas' THEN
 WITH base AS (SELECT *,quantity*unit_price AS importe,upper(invoice_no) LIKE 'C%' AS cancelacion FROM public.ventas_uci WHERE invoice_date>=d AND invoice_date<h+1 AND (p IS NULL OR country=p)),
 totals AS (SELECT count(*) AS lineas,
 count(DISTINCT invoice_no) FILTER (WHERE quantity>0 AND unit_price>0 AND NOT cancelacion) AS pedidos_venta,
 COALESCE(sum(importe) FILTER (WHERE quantity>0 AND unit_price>0 AND NOT cancelacion),0) AS ventas_positivas,
 COALESCE(-sum(importe) FILTER (WHERE quantity<0 AND unit_price>0 AND cancelacion),0) AS cancelaciones,
 COALESCE(-sum(importe) FILTER (WHERE quantity<0 AND unit_price>0 AND NOT cancelacion),0) AS otros_ajustes_negativos,
 COALESCE(sum(importe) FILTER (WHERE unit_price>0 AND (quantity<0 OR (quantity>0 AND NOT cancelacion))),0) AS importe_neto,
 count(*) FILTER (WHERE unit_price<=0 OR quantity=0 OR (quantity>0 AND cancelacion)) AS lineas_fuera_kpi FROM base) SELECT to_jsonb(totals) INTO result FROM totals;
 RETURN ctx || jsonb_build_object('metricas',result);
 ELSE
 WITH base AS (SELECT *,quantity*unit_price AS importe,upper(invoice_no) LIKE 'C%' AS cancelacion, CASE dim WHEN 'pais' THEN country WHEN 'producto' THEN stock_code ELSE to_char(invoice_date,'YYYY-MM') END AS grupo FROM public.ventas_uci WHERE invoice_date>=d AND invoice_date<h+1 AND (p IS NULL OR country=p)),
 totals AS (SELECT grupo,count(*) AS lineas,
 count(DISTINCT invoice_no) FILTER (WHERE quantity>0 AND unit_price>0 AND NOT cancelacion) AS pedidos_venta,
 COALESCE(sum(importe) FILTER (WHERE quantity>0 AND unit_price>0 AND NOT cancelacion),0) AS ventas_positivas,
 COALESCE(-sum(importe) FILTER (WHERE quantity<0 AND unit_price>0 AND cancelacion),0) AS cancelaciones,
 COALESCE(-sum(importe) FILTER (WHERE quantity<0 AND unit_price>0 AND NOT cancelacion),0) AS otros_ajustes_negativos,
 COALESCE(sum(importe) FILTER (WHERE unit_price>0 AND (quantity<0 OR (quantity>0 AND NOT cancelacion))),0) AS importe_neto,
 count(*) FILTER (WHERE unit_price<=0 OR quantity=0 OR (quantity>0 AND cancelacion)) AS lineas_fuera_kpi FROM base GROUP BY grupo ORDER BY importe_neto DESC,grupo LIMIT n)
 SELECT COALESCE(jsonb_agg(to_jsonb(totals)),'[]'::jsonb) INTO result FROM totals;
 RETURN ctx || jsonb_build_object('dimension',dim,'orden','importe_neto descendente','filas',result);
 END IF;
END $$;
REVOKE ALL ON FUNCTION public.bi_tool(text,jsonb) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.bi_tool(text,jsonb) TO anon, authenticated;
