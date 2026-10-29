-- Tabla nueva: no modifica ventas_superstore. Ejecutada por importar_uci.py.
CREATE TABLE IF NOT EXISTS public.ventas_uci (
 source_row integer PRIMARY KEY,
 invoice_no text NOT NULL,
 stock_code text NOT NULL,
 description text,
 quantity integer NOT NULL,
 invoice_date timestamp NOT NULL,
 unit_price numeric NOT NULL,
 customer_id text,
 country text NOT NULL
);
ALTER TABLE public.ventas_uci ENABLE ROW LEVEL SECURITY;
CREATE INDEX IF NOT EXISTS ventas_uci_date_idx ON public.ventas_uci(invoice_date);
CREATE INDEX IF NOT EXISTS ventas_uci_country_idx ON public.ventas_uci(country);
CREATE TABLE IF NOT EXISTS public.bi_dataset_metadata (
 dataset text PRIMARY KEY,
 source_sha256 text NOT NULL,
 row_count integer NOT NULL,
 raw_amount numeric NOT NULL,
 imported_at timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE public.bi_dataset_metadata ENABLE ROW LEVEL SECURITY;
