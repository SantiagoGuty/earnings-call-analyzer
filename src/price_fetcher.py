import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

EARNINGS_DATES = {
    "AAPL": ["2024-02-01", "2024-05-02", "2024-08-01", "2024-10-31"],
    "MSFT": ["2024-01-24", "2024-04-25", "2024-07-30", "2024-10-30"],
    "GOOGL": ["2024-01-30", "2024-04-25", "2024-07-23", "2024-10-29"],
    "AMZN": ["2024-02-01", "2024-04-30", "2024-08-01", "2024-10-31"],
    "META":  ["2024-02-01", "2024-04-24", "2024-07-31", "2024-10-30"],
    "NVDA":  ["2024-02-21", "2024-05-22", "2024-08-28", "2024-11-20"],
    "JPM":   ["2024-01-12", "2024-04-12", "2024-07-12", "2024-10-11"],
    "BAC":   ["2024-01-12", "2024-04-16", "2024-07-16", "2024-10-15"],
}

def get_price_around_earnings(ticker, earnings_date):
    date = datetime.strptime(earnings_date, "%Y-%m-%d")
    start = (date - timedelta(days=5)).strftime("%Y-%m-%d")
    end   = (date + timedelta(days=5)).strftime("%Y-%m-%d")

    stock = yf.download(ticker, start=start, end=end, progress=False)

    if len(stock) < 2:
        print(f"  WARNING: Not enough data for {ticker} on {earnings_date}")
        return None

    close = stock["Close"]
    if hasattr(close.iloc[-1], '__len__'):
        price_before = float(close.iloc[-2].iloc[0])
        price_after  = float(close.iloc[-1].iloc[0])
    else:
        price_before = float(close.iloc[-2])
        price_after  = float(close.iloc[-1])

    change_pct = round((price_after - price_before) / price_before * 100, 2)

    return {
        "ticker":           ticker,
        "earnings_date":    earnings_date,
        "price_before":     round(price_before, 2),
        "price_after":      round(price_after, 2),
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
                print(f"  {date} → {row['direction']} {row['price_change_pct']}%")

    df = pd.DataFrame(results)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/prices.csv", index=False)
    print(f"\nDone. {len(df)} rows saved to data/prices.csv")
    print(df.head(10))

if __name__ == "__main__":
    run()