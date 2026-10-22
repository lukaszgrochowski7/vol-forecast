"""SQLite storage for daily prices."""
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE IF NOT EXISTS prices (
    ticker TEXT NOT NULL,
    date   TEXT NOT NULL,
    close  REAL NOT NULL,
    volume INTEGER,
    PRIMARY KEY (ticker, date)
);
"""

def connect(path: str = "data/prices.db") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute(SCHEMA)
    return conn

def upsert_prices(conn, ticker: str, df: pd.DataFrame) -> int:
    """df: index = dates, columns 'close' and 'volume'. Returns rows written."""
    rows = [
        (ticker, d.strftime("%Y-%m-%d"), float(r.close), int(r.volume))
        for d, r in df.iterrows()
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO prices (ticker, date, close, volume) VALUES (?,?,?,?)",
        rows,
    )
    conn.commit()
    return len(rows)

def last_date(conn, ticker: str):
    """Latest stored date for a ticker, or None."""
    row = conn.execute(
        "SELECT MAX(date) FROM prices WHERE ticker = ?", (ticker,)
    ).fetchone()
    return row[0]

def load_prices(conn, ticker: str) -> pd.DataFrame:
    df = pd.read_sql_query(
        "SELECT date, close, volume FROM prices WHERE ticker = ? ORDER BY date",
        conn, params=(ticker,), parse_dates=["date"],
    )
    return df.set_index("date")
