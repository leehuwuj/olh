import pandas as pd
import requests
from dagster import MetadataValue, Output, asset
from deltalake.writer import write_deltalake


@asset(
    io_manager_key='s3_io_manager',
    required_resource_keys={'s3'}
)
def hackernews_top_story_ids(context):
    """
    Get top stories from the HackerNews top stories endpoint.
    API Docs: https://github.com/HackerNews/API#new-top-and-best-stories
    """
    # context.resources.s3
    top_story_ids = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json"
    ).json()
    return top_story_ids[:10]


# asset dependencies can be inferred from parameter names
@asset(
    key_prefix=['hackernews'],
    io_manager_key='arrow',
    metadata={"stored_as": "parquet"}
)
def hackernews_top_stories(context, hackernews_top_story_ids):
    """Get items based on story ids from the HackerNews items endpoint"""
    results = []
    for item_id in hackernews_top_story_ids:
        item = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
        ).json()
        results.append(item)

    df = pd.DataFrame(results)

    # recorded metadata can be customized
    metadata = {
        "num_records": len(df),
        "preview": MetadataValue.md(df[["title", "by", "url"]].to_markdown())
    }

    context.add_output_metadata(metadata)

    return Output(value=df, metadata=metadata)


@asset(
    key_prefix=['hackernews'],
    required_resource_keys={'trino_client'},
    io_manager_key='arrow',
    config_schema={"max_result": int},
    metadata={"stored_as": "parquet"}
)
def hackernews_items(context):
    def get_last_carwled_item_id(context):
        rs = context.resources.trino_client.query(
            "SELECT max(id) FROM hackernews.items"
        )
        print(rs)
        return rs[0][0]

    arg_max_result = context.op_config.get("max_result", 10)
    # get latest id
    try:
        last_id = int(get_last_carwled_item_id(context))
    except Exception as e:
        raise(e)

    print(f"Last id: {last_id}")
    max_id = int(requests.get(
        "https://hacker-news.firebaseio.com/v0/maxitem.json"
    ).json())
    print(f"Max id: {max_id}")
    to_crawl_ids = list(range(last_id + 1, min(max_id, last_id+arg_max_result)))

    results = []
    for item_id in to_crawl_ids:
        item = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
        ).json()
        results.append(item)

    df = pd.DataFrame(results)

    metadata = {
        "num_records": len(df),
        "preview": MetadataValue.md(df[["id", "by", "time"]].iloc[0:10].to_markdown())
    }

    return Output(value=df, metadata=metadata)


@asset(
    required_resource_keys={'s3', 'pyspark'},
    compute_kind="pyspark",
)
def items_spark(context, hackernews_items):
    items_pdf = hackernews_items.read().to_pandas()
    spark = context.resources.pyspark.spark_session
    spark_df = spark.createDataFrame(items_pdf)

    (spark_df
        .write
        .format("delta")
        .mode("overwrite")
        .saveAsTable("hackernews.items"))


@asset(
    key_prefix=['hackernews'],
    compute_kind="delta-rs",
    required_resource_keys={'trino_client'}
)
def items(context, hackernews_items):
    from trino.exceptions import TrinoUserError

    # storage_options = {
    #     "AWS_ACCESS_KEY_ID": "", 
    #     "AWS_SECRET_ACCESS_KEY":"",
    #     "AWS_ENDPOINT_URL": "",
    #     "AWS_REGION": "",
    #     "AWS_S3_ALLOW_UNSAFE_RENAME": "true",
    #     "AWS_STORAGE_ALLOW_HTTP": "true"
    # }
    storage_options = context.resources.arrow.storage_options

    write_deltalake(
        table_or_uri="s3://lake-dev/warehouse/hackernews.db/items",
        storage_options=storage_options,
        data=hackernews_items.read(),
        overwrite_schema=True
    )
    
    # Register metastore
    try:
        context.resources.trino_client.query(
            """CALL system.register_table(
                schema_name => 'hackernews',
                table_name => 'items',
                table_location => 's3a://lake-dev/warehouse/hackernews.db/items'
            )"""
        )
    except TrinoUserError as e:
        if e.error_name == 'ALREADY_EXISTS':
            context.log.info("Skip register delta table since table already existed!")
            return


assets = [
    hackernews_top_story_ids,
    hackernews_top_stories,
    hackernews_items,
    items_spark,
    items
]
