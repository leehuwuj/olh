from testbook import testbook

@testbook('/tmp/tests/spark-hivemetastore-test.ipynb', execute=True)
def test_get_details(tb):
    nb_tables = tb.get("tables")
    
    assert type(nb_tables) == list