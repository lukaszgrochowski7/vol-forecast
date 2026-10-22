import pandas as pd
from volforecast import db

def sample():
    idx = pd.to_datetime(["2024-01-02", "2024-01-03"])
    return pd.DataFrame({"close": [100.0, 101.0], "volume": [10, 20]}, index=idx)

def test_upsert_and_load():
    conn = db.connect(":memory:")
    assert db.upsert_prices(conn, "AAA", sample()) == 2
    assert len(db.load_prices(conn, "AAA")) == 2

def test_upsert_is_idempotent():
    conn = db.connect(":memory:")
    db.upsert_prices(conn, "AAA", sample())
    db.upsert_prices(conn, "AAA", sample())
    assert len(db.load_prices(conn, "AAA")) == 2

def test_last_date():
    conn = db.connect(":memory:")
    assert db.last_date(conn, "AAA") is None
    db.upsert_prices(conn, "AAA", sample())
    assert db.last_date(conn, "AAA") == "2024-01-03"
