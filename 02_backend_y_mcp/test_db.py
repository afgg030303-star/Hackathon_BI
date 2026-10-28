"""Prueba de lectura de Supabase. Ejecutar con python test_db.py."""

import sys
from pathlib import Path
import os

import psycopg2
from dotenv import load_dotenv


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    load_dotenv(root / ".env")
    database_url = os.getenv("DATABASE_URL", "").strip()
    if not database_url or "PON_AQUÍ" in database_url:
        print("✗ Configura DATABASE_URL en el archivo .env de la raíz.", file=sys.stderr)
        return 1

    print("\n🔎 Auditor Agéntico de Rentabilidad — prueba de base de datos")
    connection = None
    try:
        connection = psycopg2.connect(
            database_url,
            connect_timeout=10,
            sslmode="require",
            options="-c statement_timeout=15000",
            application_name="auditor_test_db",
        )
        connection.set_session(readonly=True)
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM ventas_superstore;")
            count = cursor.fetchone()[0]
        print("✓ Conexión segura a Supabase establecida.")
        print("✓ Consulta ejecutada correctamente.")
        print(f"  Tabla: ventas_superstore | Filas: {count:,}")
        if count == 0:
            print("⚠ La tabla existe, pero todavía no contiene datos.")
        return 0
    except psycopg2.errors.UndefinedTable:
        print("✗ No existe ventas_superstore en el search_path de esta conexión.", file=sys.stderr)
        return 1
    except psycopg2.errors.InsufficientPrivilege:
        print("✗ El usuario no tiene permisos para leer ventas_superstore.", file=sys.stderr)
        return 1
    except psycopg2.OperationalError:
        print("✗ No se pudo completar la conexión/consulta. Revisa la contraseña, el host, "
              "la red y la disponibilidad de Supabase. La conexión espera hasta 10 s "
              "y la consulta hasta 15 s.", file=sys.stderr)
        return 1
    except (psycopg2.Error, ValueError):
        print("✗ Error de configuración o de consulta PostgreSQL. Revisa DATABASE_URL "
              "y la tabla. No se muestran credenciales.", file=sys.stderr)
        return 1
    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    raise SystemExit(main())
