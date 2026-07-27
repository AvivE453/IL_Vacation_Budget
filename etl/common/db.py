from contextlib import contextmanager

import psycopg2
import psycopg2.extras

from etl.common.config import DB_URL


# Raw connection, no cursor - for scripts that open their own plain cursor
# (no need for dict-style row access) or share one cursor/transaction across
# several loading steps (e.g. load_airports.py loading countries + airports
# together, so either both succeed or both roll back).
@contextmanager
def get_conn():
    conn = psycopg2.connect(DB_URL)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# Ready-to-use dict cursor, for scripts that read query results back by
# column name (e.g. dest["city_name"]).
@contextmanager
def get_cursor():
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            yield cur
