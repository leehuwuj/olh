import os

from typing import Any
from pyspark.sql.dataframe import DataFrame

import pyspark.sql.functions as F
from pyspark.sql import SparkSession

HIVE_METASTORE_URIS = os.environ.get(
    "HIVE_METASTORE_URIS", 
    "thrift://localhost:9083"
)
TWEETS_DATA_PATH = os.environ.get(
    "TWEETS_DATA_PATH", 
    "[CHANGE_ME]/TweetsChampions.json"
)
TWEETS_FACT_TABLE_NAME = os.environ.get(
    "TWEETS_FACT_TABLE_NAME",
    "tweets.tweetsfact"
)

def init_spark() -> SparkSession:
    """Init a new Spark session which supports Deltalake"""
    return (
        SparkSession
        .builder
        .config("hive.metastore.uris", HIVE_METASTORE_URIS)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.hadoop.fs.s3a.path.style.access", "True")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .enableHiveSupport()
        .getOrCreate()
    )

def read_json_data(spark: SparkSession, s3_path: str) -> DataFrame:
    return spark.read.json(s3_path)

def write_delta_table(
    data: DataFrame, 
    table: str, 
    mode: str = "append",
    partitions: list = [],
    options: dict = {}) -> Any:
    (
        data
        .write
        .format("delta")
        .partitionBy(partitions)
        .options(**options)
        .mode(mode)
        .saveAsTable(table)
    )

def filter_tweets_fact_table(tweets_df: DataFrame) -> DataFrame:
    return tweets_df.select(
        # Convert timestamp_ms from unix string into timestamp type
        F.to_timestamp((F.col('timestamp_ms')/1000)).alias('timestamp_ms'), 
        'id',
        'text',
        'source',
        F.col('user.id').alias('user_id'),
        'lang',
        'quote_count',
        'reply_count',
        'retweet_count'
    )

def tweets_fact_pipeline(spark: SparkSession):
    # Read raw data
    tweets_df = read_json_data(
        spark, 
        s3_path=TWEETS_DATA_PATH
    )
    
    # Filter data
    tweet_fact_df = filter_tweets_fact_table(tweets_df)
    tweet_fact_df.printSchema()

    # Write to delta table
    write_delta_table(
        data=tweet_fact_df,
        table=TWEETS_FACT_TABLE_NAME,
        mode="overwrite",
        partitions=["lang"],
        options={
            "overwriteSchema": "true"
        }
    )

if __name__ == "__main__":
    spark = init_spark()
    tweets_fact_pipeline(spark=spark)