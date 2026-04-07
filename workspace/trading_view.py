# trading_view.py
# Simple wrapper for fetching latest market data using yfinance
# This file is placed under workspace for your convenience.
# Usage: python trading_view.py <TICKER>

import datetime as _dt
import pandas as _pd

import yfinance as _yf


def _validate_symbol(symbol: str) -> str:
    if not isinstance(symbol, str) or not symbol.strip():
        raise ValueError("symbol must be a non‑empty string")
    return symbol.strip().upper()


def get_latest_price(symbol: str, interval: str = "1m") -> float:
    """Return the most recent closing price for *symbol* using yfinance."""
    symbol = _validate_symbol(symbol)
    end = _dt.datetime.utcnow()
    start = end - _dt.timedelta(minutes=5)
    df: _pd.DataFrame = _yf.download(
        tickers=symbol,
        start=start,
        end=end,
        interval=interval,
        progress=False,
    )
    if df.empty:
        raise RuntimeError(f"No data returned for {symbol}")
    latest = df.iloc[-1]
    return float(latest["Close"])


if __name__ == "__main__":
    import sys
    try:
        ticker = sys.argv[1]
    except IndexError:
        print("Usage: python trading_view.py <TICKER>")
        sys.exit(1)
    try:
        price = get_latest_price(ticker)
        print(f"Latest price of {ticker.upper()}: ${price:.2f}")
    except Exception as exc:
        print(f"Error fetching price: {exc}")
        sys.exit(1)
