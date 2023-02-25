import os
from typing import Dict
from dagster import (
    Definitions,
    colored_console_logger
)

from dagster_aws.s3 import s3_pickle_io_manager, s3_resource
from dagster_pyspark import pyspark_resource
from dagster_dbt import dbt_cli_resource

from . import assets
from .resources.trino import trino_client
from .io.arrow_dataset import arrow_dataset_io


S3_ENDPOINT = os.environ.get("AWS_S3_ENDPOINT_URL")
AWS_ACCESS_KEY_ID= os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

SPARK_CLUSTER = os.environ.get("SPARK_CLUSTER", "k8s://https://host.docker.internal:8443")
SPARK_METASTORE = os.environ.get("SPARK_METASTORE", "thrift://host.docker.internal:9083")
# Please set this to your dagster host IP that the network from k8s cluster can connect to
SPARK_DRIVER_HOST = os.environ.get("SPARK_DRIVER_HOST")

DBT_HOME = os.environ.get("DBT_HOME")

DBT_PROJECT_PATH = os.path.join(DBT_HOME, "olh/dbt/hackernews")
DBT_PROFILES = os.path.join(DBT_HOME, "olh/dbt/hackernews")

def get_default_config_k8s() -> Dict:
    return {
        "spark.master": SPARK_CLUSTER,
        "spark.kubernetes.namespace": "spark",
        "hive.metastore.uris": SPARK_METASTORE,
        "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
        "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        "spark.driver.host": SPARK_DRIVER_HOST,
        "spark.app.name": "dagster_",
        "spark.kubernetes.container.image": "olh/spark:delta",
        "spark.kubernetes.authenticate.driver.serviceAccountName": "spark",
        "spark.hadoop.fs.s3a.access.key": AWS_ACCESS_KEY_ID,
        "spark.hadoop.fs.s3a.secret.key": AWS_SECRET_ACCESS_KEY,
        "spark.hadoop.fs.s3a.endpoint": S3_ENDPOINT,
        "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
        "spark.hadoop.fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
        "spark.hadoop.fs.s3a.fast.upload": "true",
        "spark.kubernetes.file.upload.path": "s3a://lake-dev/spark",
        "spark.kubernetes.driver.volumes.persistentVolumeClaim.sparkrwx.options.claimName": "sparkrwx",
        "spark.kubernetes.executor.volumes.persistentVolumeClaim.sparkrwx.options.claimName": "sparkrwx",
        "spark.kubernetes.driver.volumes.persistentVolumeClaim.sparkrwx.mount.path": "/opt/spark/work-dir",
        "spark.kubernetes.executor.volumes.persistentVolumeClaim.sparkrwx.mount.path": "/opt/spark/work-dir",
        "spark.driver.extraJavaOptions": "-Divy.cache.dir=/opt/spark/work-dir/tmp -Divy.home=/opt/spark/work-dir/tmp",
        "spark.executor.instances": "1",
        "spark.sql.execution.arrow.pyspark.enabled": "true"
    }

dbt_resources = {
    "dbt": dbt_cli_resource.configured(
        {
            "project_dir": DBT_PROJECT_PATH,
            "profiles_dir": DBT_PROFILES,
        },
    ),
}

defs = Definitions(
    assets=assets,
    loggers={
        "console": colored_console_logger.configured({
            "log_level": "ERROR"
        })
    },
    resources={
        "s3_io_manager": s3_pickle_io_manager.configured({
            "s3_bucket": "lake-dev",
            "s3_prefix": "dagster/hackernews"
        }),
        "arrow": arrow_dataset_io.configured({
            "filesystem": "S3FileSystem",
            "endpoint_url": S3_ENDPOINT,
            "prefix": "lake-dev/dagster/hackernews"
        }),
        "s3": s3_resource.configured({
            "endpoint_url": S3_ENDPOINT,
        }),
        "trino_client": trino_client.configured({
            "schema": "hackernews"
        }),
        "pyspark": pyspark_resource.configured(
            {
                "spark_conf": get_default_config_k8s()
            }
        ),
        **dbt_resources
    }
)
