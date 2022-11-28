import pytest


@pytest.fixture(scope="session")
def spark_local_session():
    from pyspark.sql import SparkSession

    spark = (
        SparkSession
        .builder
        .master("local[2]")
        .appName("pyspark tester")
        .getOrCreate()
    )
    return spark

@pytest.fixture(scope="session")
def trino_client():
    import os
    from trino.dbapi import connect

    TRINO_HOST = os.environ.get("TRINO_HOST", "host.docker.internal")
    TRINO_PORT = int(os.environ.get("TRINO_PORT", 8080))
    TRINO_USER = os.environ.get("TRINO_USER", "python")
    TRINO_CATALOG = os.environ.get("TRINO_CATALOG", "default")
    TRINO_SCHEMA = os.environ.get("TRINO_SCHEMA", "tweets")

    conn = connect(
        host=TRINO_HOST,
        port=TRINO_PORT,
        user=TRINO_USER,
        catalog=TRINO_CATALOG,
        schema=TRINO_SCHEMA
    )
    return conn