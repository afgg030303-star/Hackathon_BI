"""Comprueba PostgreSQL en solo lectura, sin depender de una tabla de ventas."""
import os
import sys
from pathlib import Path


def main():
    try:
        from dotenv import load_dotenv
        import psycopg2
    except ImportError:
        print("Faltan dependencias: instala psycopg2-binary y python-dotenv en el entorno virtual.")
        return 2
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    uri = os.getenv("DATABASE_URL", "").strip()
    if not uri or any(marker in uri.upper() for marker in ("PON_AQU", "REEMPLAZAR", "[YOUR-PASSWORD]")):
        print("PENDIENTE: configura DATABASE_URL en .env. No pegues la contraseña en el chat.")
        return 2
    conn = None
    try:
        conn = psycopg2.connect(uri, connect_timeout=10, sslmode="require",
                               options="-c statement_timeout=15000",
                               application_name="hackathon_comprobar_supabase")
        conn.set_session(readonly=True)
        params = conn.get_dsn_parameters()
        expected = "gvsxekaqeodljocyqkfo"
        host = params.get("host", "")
        user = params.get("user", "")
        if host != f"db.{expected}.supabase.co" and not (
            host.endswith(".pooler.supabase.com") and user.endswith("." + expected)
        ):
            print("AVISO: conexión abierta, pero host/usuario no identifican el proyecto esperado. Revisa Connect.")
            return 1
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            assert cur.fetchone()[0] == 1
            cur.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = %s ORDER BY tablename", ("public",))
            names = [row[0] for row in cur.fetchall()]
        print("OK: conexión TLS y consulta de lectura al proyecto Supabase esperado.")
        print("Tablas públicas visibles: " + (", ".join(names) if names else "ninguna"))
        print("Esta prueba no valida los datos importados ni permisos de escritura del usuario.")
        return 0
    except (psycopg2.Error, ValueError):
        print("ERROR: no se pudo verificar PostgreSQL. Revisa URI, contraseña y conectividad. No se muestran secretos.")
        return 1
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    sys.exit(main())
