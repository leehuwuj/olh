import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def local_session():
    spark = (
        SparkSession
        .builder
        .master("local[2]")
        .appName("pyspark tester")
        .getOrCreate()
    )
    return spark