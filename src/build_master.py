import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TRANSCRIPTS_TARGET_NUMBER = 9

def earnings_date_to_quarter(date_str):
    month = pd.to_datetime(date_str).month
    return (month - 1) // 3 + 1

def run():
    prices = pd.read_csv(DATA_DIR / "prices.csv")
    ticker_group = {}
    rows = []
    for _, row in prices.iterrows():
        quarter = earnings_date_to_quarter(row["earnings_date"])
        year    = pd.to_datetime(row["earnings_date"]).year
        ticker  = row["ticker"]


        transcript_path = DATA_DIR / "transcripts" / f"{ticker}_{year}_Q{quarter}.txt"
        file_exists     = transcript_path.exists()
        
        
        if ticker not in ticker_group:
            ticker_group[ticker] = 0
        if file_exists:
            ticker_group[ticker] += 1
        
        rows.append({
            "ticker":           ticker,
            "year":             year,
            "quarter":          None,   # assigned below
            "earnings_date":    row["earnings_date"],
            "transcript_path":  "",     # assigned below
            "file_exists":      False,  # assigned below
            "price_before":     row["price_before"],
            "price_after":      row["price_after"],
            "price_change_pct": row["price_change_pct"],
            "direction":        row["direction"],
            "is_test":          year == 2026
        })

    df = pd.DataFrame(rows)

    # Assign quarters sequentially per ticker per year based on call order
    df = df.sort_values(["ticker", "earnings_date"]).reset_index(drop=True)
    df["quarter"] = df.groupby(["ticker", "year"]).cumcount() + 1
    df["quarter"] = "Q" + df["quarter"].astype(str)

    # Now that quarter is correct, build transcript paths and check existence
    df["transcript_path"] = df.apply(
        lambda r: str(DATA_DIR / "transcripts" / f"{r['ticker']}_{r['year']}_{r['quarter']}.txt"),
        axis=1
    )
    df["file_exists"] = df["transcript_path"].apply(lambda p: Path(p).exists())

    # Build ticker_group from the corrected data
    ticker_group = df[df["file_exists"]].groupby("ticker").size().to_dict()

    output = DATA_DIR / "master_data.csv"
    df.to_csv(output, index=False)

    print(f"Done. {len(df)} rows saved to {output}")
    print(f"  Transcripts found: {df['file_exists'].sum()} / {len(df)}")
    print(f"  Test set (2026):   {df['is_test'].sum()} rows")
    print("  Companies and the successfully fetched transcript files:")
    for ticker in df["ticker"].unique():
        count = ticker_group.get(ticker, 0)
        check = '✅' if count == TRANSCRIPTS_TARGET_NUMBER else '❌'
        print(f"    > {ticker} completed: {count} {check}")
        
    missing = df[df["file_exists"] == False][["ticker", "year", "quarter"]]
    if not missing.empty:
        print(f"\n  Missing transcripts ({len(missing)}):")
        print(missing.to_string(index=False))
        missing.to_csv(DATA_DIR / "missing_transcripts.csv", index=False)

    print(df[["ticker", "year", "quarter", "file_exists", "direction"]].to_string())
    
    
    
if __name__ == "__main__":
    run()