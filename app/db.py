from contextlib import contextmanager

import psycopg2
import psycopg2.extras

from etl.common.config import DB_URL


# Only a dict cursor is exposed here (unlike etl/common/db.py, which also
# has a raw get_conn()) - every route wants the same thing: one ready
# cursor with dict-style row acces.
@contextmanager
def get_cursor():
    conn = psycopg2.connect(DB_URL)
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
