## Flow
![tweets-champions-flow](../../images/tweets-practice.png)

## Data:
- [Tweets Data](https://github.com/leehuwuj/olh/blob/main/resources/data/README.md)

## Practice steps (manually):
1. Ingest raw json data into MinIO at raw path.
2. Submit `pyspark_tweets_fact_ingesting.py` to filter out tweet information into `tweet_fact` table.
3. Testing table data in Trino.
3. Create Superset dashboard.

## Dagster (automatically):
// Todo