import psycopg2
import psycopg2.extras
import pytest

from etl.common.config import DB_URL


@pytest.fixture()
def cur():
    try:
        conn = psycopg2.connect(DB_URL)
    except psycopg2.OperationalError as e:
        pytest.skip(f"database not reachable at {DB_URL}: {e}")
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as c:
            yield c
        conn.rollback()  # tests must not persist writes against the shared dev DB
    finally:
        conn.close()
