# Applies every .sql file in sql/migrations/ in filename order.

# Run with: python -m etl.loaders.run_migrations

import pathlib

from etl.common.db import get_conn

MIGRATIONS_DIR = pathlib.Path(__file__).resolve().parent.parent.parent / "sql" / "migrations"


def main():
    migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    if not migration_files:
        raise SystemExit(f"no migration files found in {MIGRATIONS_DIR}")

    with get_conn() as conn:
        with conn.cursor() as cur:
            for path in migration_files:
                print(f"applying {path.name}")
                cur.execute(path.read_text())

    print(f"applied {len(migration_files)} migrations")


if __name__ == "__main__":
    main()
