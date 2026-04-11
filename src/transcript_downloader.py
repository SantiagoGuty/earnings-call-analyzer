import os
from earningscall import get_company

# Same tickers as price_fetcher.py
# Mapped to the 4 quarters of 2024 that align with your earnings dates
TICKER_QUARTERS = {
    "AAPL":  [(2024, 1), (2024, 2), (2024, 3), (2024, 4)],
    "MSFT":  [(2024, 1), (2024, 2), (2024, 3), (2024, 4)],
    "GOOGL": [(2024, 1), (2024, 2), (2024, 3), (2024, 4)],
    "AMZN":  [(2024, 1), (2024, 2), (2024, 3), (2024, 4)],
    "META":  [(2024, 1), (2024, 2), (2024, 3), (2024, 4)],
    "NVDA":  [(2024, 1), (2024, 2), (2024, 3), (2024, 4)],
    "JPM":   [(2024, 1), (2024, 2), (2024, 3), (2024, 4)],
    "BAC":   [(2024, 1), (2024, 2), (2024, 3), (2024, 4)],
}

def download_transcript(ticker, year, quarter):
    """Download a single transcript and return its text, or None if unavailable."""
    try:
        company = get_company(ticker.lower())
        transcript = company.get_transcript(year=year, quarter=quarter)

        if transcript is None or not transcript.text:
            print(f"  WARNING: No transcript found for {ticker} {year} Q{quarter}")
            return None

        return transcript.text

    except Exception as e:
        print(f"  WARNING: Failed to fetch {ticker} {year} Q{quarter} — {e}")
        return None

def save_transcript(ticker, year, quarter, text):
    """Save transcript text to data/transcripts/TICKER_YEAR_QN.txt"""
    os.makedirs("data/transcripts", exist_ok=True)
    filename = f"data/transcripts/{ticker}_{year}_Q{quarter}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    return filename

def run():
    saved = []
    failed = []

    for ticker, quarters in TICKER_QUARTERS.items():
        print(f"Fetching {ticker}...")
        for (year, quarter) in quarters:
            text = download_transcript(ticker, year, quarter)
            if text:
                filepath = save_transcript(ticker, year, quarter, text)
                word_count = len(text.split())
                saved.append({"ticker": ticker, "year": year, "quarter": quarter, "file": filepath, "words": word_count})
                print(f"  Q{quarter} {year} → saved ({word_count:,} words)")
            else:
                failed.append(f"{ticker} {year} Q{quarter}")

    print(f"\nDone. {len(saved)} transcripts saved to data/transcripts/")
    if failed:
        print(f"Skipped ({len(failed)}): {', '.join(failed)}")

    for row in saved[:5]:
        print(f"  {row['file']} — {row['words']:,} words")

if __name__ == "__main__":
    run()