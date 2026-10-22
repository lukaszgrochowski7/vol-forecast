"""Download prices and store only the missing days."""
import sys
import pandas as pd
import yfinance as yf
from volforecast import db

DEFAULT_TICKERS = ["AAPL", "MSFT", "JPM", "XOM", "JNJ"]

def fetch(ticker: str, start: str | None = None) -> pd.DataFrame:
    raw = yf.download(ticker, start=start, auto_adjust=True, progress=False)
    if raw.empty:
        return pd.DataFrame(columns=["close", "volume"])
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)
    df = raw[["Close", "Volume"]].rename(columns={"Close": "close", "Volume": "volume"})
    return df.dropna()

def update(conn, ticker: str) -> int:
    last = db.last_date(conn, ticker)
    start = None
    if last:
        start = (pd.Timestamp(last) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    df = fetch(ticker, start)
    return db.upsert_prices(conn, ticker, df) if not df.empty else 0

if __name__ == "__main__":
    tickers = sys.argv[1:] or DEFAULT_TICKERS
    conn = db.connect()
    for t in tickers:
        print(f"{t}: {update(conn, t)} new rows")
