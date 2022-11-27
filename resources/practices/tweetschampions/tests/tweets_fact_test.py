import pytest

from pyspark.sql.types import (
    StructField,
    StructType,
    TimestampType,
    StringType,
    LongType
)

from pyspark.sql import SparkSession
from pyspark_tweets_fact_ingesting import filter_tweets_fact_table

@pytest.mark.usefixtures("local_session")
def test_filter_tweets_fact_table(local_session: SparkSession):
    expected_schema = StructType([
        StructField('timestamp_ms', TimestampType(), True), 
        StructField('id', LongType(), True), 
        StructField('text', StringType(), True), 
        StructField('source', StringType(), True), 
        StructField('user_id', LongType(), True), 
        StructField('lang', StringType(), True), 
        StructField('quote_count', LongType(), True), 
        StructField('reply_count', LongType(), True), 
        StructField('retweet_count', LongType(), True)]
    )

    data = local_session.read.json("tests/example.json")
    output_df = filter_tweets_fact_table(data)

    assert output_df.schema == expected_schema
    assert output_df.count() == 10