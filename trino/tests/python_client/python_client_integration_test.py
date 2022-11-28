import os
from trino.dbapi import connect

TRINO_HOST = os.environ.get("TRINO_HOST", "host.docker.internal")
TRINO_PORT = int(os.environ.get("TRINO_PORT", 8080))
TRINO_USER = os.environ.get("TRINO_USER", "python")
TRINO_CATALOG = os.environ.get("TRINO_CATALOG", "default")
TRINO_SCHEMA = os.environ.get("TRINO_SCHEMA", "system")

def test_trino_client():
    conn = connect(
        host=TRINO_HOST,
        port=TRINO_PORT,
        user=TRINO_USER,
        catalog=TRINO_CATALOG,
        schema=TRINO_SCHEMA
    )

    cur = conn.cursor()
    cur.execute("SELECT * FROM system.runtime.nodes")
    rows = cur.fetchall()
    print(rows)
    assert len(rows) > 0