import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def main():
    load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
    database_url = os.environ["DATABASE_URL"]

    with psycopg.connect(database_url) as connection, connection.cursor() as cursor:
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    name TEXT PRIMARY KEY,
                    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
        )
        cursor.execute("SELECT name FROM schema_migrations")
        applied = {row[0] for row in cursor.fetchall()}

        for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            if path.name in applied:
                continue
            cursor.execute(path.read_text(encoding="utf-8"))
            cursor.execute(
                "INSERT INTO schema_migrations (name) VALUES (%s)",
                (path.name,),
            )
            print(f"Applied {path.name}")

    print("Done.")


if __name__ == "__main__":
    main()
