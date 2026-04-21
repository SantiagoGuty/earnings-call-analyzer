import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # goes up from src/ to project root
DATA_DIR = BASE_DIR / "data"

EARNINGS_DATES = {
    "AAPL":  ["2024-02-01", "2024-05-02", "2024-08-01", "2024-10-31", "2025-01-30", "2025-05-01", "2025-07-31", "2025-10-30", "2026-01-29"],
    "MSFT":  ["2024-01-24", "2024-04-25", "2024-07-30", "2024-10-30", "2025-01-29", "2025-04-30", "2025-07-29", "2025-10-29", "2026-01-29"],
    "GOOGL": ["2024-01-30", "2024-04-25", "2024-07-23", "2024-10-29", "2025-02-04", "2025-04-29", "2025-07-29", "2025-10-28", "2026-02-03"],
    "AMZN":  ["2024-02-01", "2024-04-30", "2024-08-01", "2024-10-31", "2025-02-06", "2025-05-01", "2025-07-31", "2025-10-30", "2026-02-05"],
    "META":  ["2024-02-01", "2024-04-24", "2024-07-31", "2024-10-30", "2025-01-29", "2025-04-30", "2025-07-30", "2025-10-29", "2026-01-28"],
    "NVDA":  ["2024-02-21", "2024-05-22", "2024-08-28", "2024-11-20", "2025-02-26", "2025-05-28", "2025-08-27", "2025-11-19", "2026-02-25"],
    "JPM":   ["2024-01-12", "2024-04-12", "2024-07-12", "2024-10-11", "2025-01-15", "2025-04-11", "2025-07-15", "2025-10-14", "2026-01-14"],
    "GS":    ["2024-01-16", "2024-04-15", "2024-07-15", "2024-10-15", "2025-01-15", "2025-04-14", "2025-07-14", "2025-10-14", "2026-01-15"],
    "TSLA":  ["2024-01-24", "2024-04-23", "2024-07-23", "2024-10-23", "2025-01-29", "2025-04-22", "2025-07-22", "2025-10-22", "2026-01-28"],
    "NFLX":  ["2024-01-23", "2024-04-18", "2024-07-17", "2024-10-16", "2025-01-21", "2025-04-17", "2025-07-17", "2025-10-15", "2026-01-21"],
}

def get_price_around_earnings(ticker, earnings_date_str):
    date = datetime.strptime(earnings_date_str, "%Y-%m-%d")

    # Fetch a wider window to ensure we capture trading days on both sides
    start = (date - timedelta(days=7)).strftime("%Y-%m-%d")
    end   = (date + timedelta(days=7)).strftime("%Y-%m-%d")

    stock = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)

    if stock.empty:
        print(f"  WARNING: No data returned for {ticker} on {earnings_date_str}")
        return None

    # Flatten MultiIndex columns if present (yfinance sometimes returns them)
    if isinstance(stock.columns, pd.MultiIndex):
        stock.columns = stock.columns.get_level_values(0)

    close = stock["Close"]
    close.index = pd.to_datetime(close.index)

    # Find last trading day strictly before earnings date
    before_dates = close.index[close.index < date]
    after_dates  = close.index[close.index >= date]

    if len(before_dates) == 0 or len(after_dates) == 0:
        print(f"  WARNING: Not enough trading days around {ticker} {earnings_date_str}")
        return None

    price_before = round(float(close.loc[before_dates[-1]]), 2)
    price_after  = round(float(close.loc[after_dates[0]]),  2)
    change_pct   = round((price_after - price_before) / price_before * 100, 2)

    return {
        "ticker":           ticker,
        "earnings_date":    earnings_date_str,
        "date_before":      before_dates[-1].strftime("%Y-%m-%d"),
        "date_after":       after_dates[0].strftime("%Y-%m-%d"),
        "price_before":     price_before,
        "price_after":      price_after,
        "price_change_pct": change_pct,
        "direction":        "UP" if change_pct > 0 else "DOWN"
    }

def run():
    results = []

    for ticker, dates in EARNINGS_DATES.items():
        print(f"Fetching {ticker}...")
        for date in dates:
            row = get_price_around_earnings(ticker, date)
            if row:
                results.append(row)
                print(f"  {date} → {row['direction']} {row['price_change_pct']}%  ({row['date_before']} → {row['date_after']})")

    df = pd.DataFrame(results)
    DATA_DIR.mkdir(exist_ok=True)
    output_path = DATA_DIR / "prices.csv"
    df.to_csv(output_path, index=False)
    print(f"\nDone. {len(df)} rows saved to {output_path}")
    
if __name__ == "__main__":
    run()