**[WIP]**
# Open source stack for lakehouse
This project to POC of a simple lakehouse architecture which aims to:
- Learning: If you are students or beginner who are working with data everyday then this project could helps you to understand the tools that you are working on.
- Cloud deputize testing: Nowaday, cloud services are easily to plug-and-play but there is various of tools and each of them have its own advantage as well as disadvantage that you have to take aware of. Almost of them are built on top open source stack so this project ifself is a cloud at your home!

There will be no fixed deployment kind but each service is revolve around cloud-native application (containerized) which use can easily to integrate/test with your current platform.

*Note*:  
    - The deployment only for testing purpose. This project scope will not cover on security feature of lakehouse (data, table, row,...) access control, resource management.  
    - If your machine does not have enough resources then just try the docker or single service deployment instead.

# Architecture
![high-level-architecutre](resources/images/architecture.png)

# Setup:
## Hive metastore:
- [Hive metastore quick setup](https://github.com/leehuwuj/olh/blob/main/hive-metastore)
## Trino
- [Trino quick setup](https://github.com/leehuwuj/olh/blob/main/trino)
## Spark
- [Spark simple setup for Kubernetes](https://github.com/leehuwuj/olh/blob/main/spark)
## Jupyter
- [Jupyter spark docker setup](https://github.com/leehuwuj/olh/blob/main/jupyter)
## Dagster
- [Dagster hackernews example project](https://github.com/leehuwuj/olh/blob/main/dagster)

# Practices
## Tweets Champions
- [Tweets Data](https://github.com/leehuwuj/olh/blob/main/resources/data/README.md)
- Examples:
    - [Pyspark - Tweets Fact ingestion](https://github.com/leehuwuj/olh/tree/main/resources/practices/tweetschampions)

## Dagster example project
Example using Dagster to orchestrate data workflow: [Arrow -> (PyDelta + Trino or PySpark Delta) -> DBT]
- [Dasgter hackernews](https://github.com/leehuwuj/olh/tree/main/dagster)