import pytest

@pytest.mark.usefixtures("trino_client")
def test_tweets_fact_table(trino_client):
    cur = trino_client.cursor()
    cur.execute("SELECT count(1) FROM hive.tweets.tweetsfact")
    rows = cur.fetchall()
    assert len(rows) == 10