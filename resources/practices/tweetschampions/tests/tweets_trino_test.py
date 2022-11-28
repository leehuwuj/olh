import pytest

@pytest.mark.usefixtures("trino_client")
def test_tweets_fact_table(trino_client):
    cur = trino_client.cursor()
    cur.execute("SELECT count(1) FROM delta.tweets.tweetsfact")
    rows = cur.fetchall()
    assert len(rows) == 10

@pytest.mark.usefixtures("trino_client")
def test_tweets_fact_duplication(trino_client):
    cur = trino_client.cursor()
    cur.execute("SELECT count(1) FROM delta.tweets.tweetsfact")
    count = cur.fetchall()[0]

    cur.execute("""
        SELECT count(1)
        FROM (
            SELECT distinct tf.*
            FROM delta.tweets.tweetsfact tf
        )
    """);
    distinct_count = cur.fetchall()[0]
    assert count == distinct_count