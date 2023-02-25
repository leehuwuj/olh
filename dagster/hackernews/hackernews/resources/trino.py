from dagster import resource
from trino.dbapi import connect

class TrinoResource:
    def __init__(self, user: str , host: str, port: str, catalog: str, schema: str) -> None:
        self.conn = connect(
            user = user,
            host = host,
            port = port,
            catalog = catalog,
            schema = schema
        )

    def query(self, sql: str):
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

@resource()
def trino_client(context):
    return TrinoResource(
        schema=context.resource_config['schema']
    )

