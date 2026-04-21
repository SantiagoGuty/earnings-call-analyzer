# Earnings Call Analyzer

Natural Language Processing pipeline that extracts sentiment, confidence, and risk signals from public earnings call transcripts to detect narrative shifts and predict short-term stock price movement.

## What it does
- Parses CEO/CFO remarks and analyst Q&A from earnings transcripts
- Extracts sentiment, confidence, and risk scores using NLP
- Computes quarter-over-quarter deltas to identify narrative changes
- Trains ML models (Logistic Regression, Random Forest, XGBoost) to predict post-earnings price direction
- Backtests predictions against real price data with Sharpe ratio tracking

## Tech Stack
Python · Pandas · scikit-learn · XGBoost · VADER/TextBlob · yfinance · Streamlit

## Structure
```
data/transcripts/     # Raw earnings call transcripts (.txt, TICKER_YEAR_Q#.txt)
data/prices.csv       # Stock prices before/after each earnings call
data/master_data.csv  # Master DataFrame joining transcripts + price data
src/price_fetcher.py  # Pulls pre/post earnings prices via yfinance
src/build_master.py   # Builds master_data.csv from prices + transcripts
models/               # Trained model artifacts
```

## Dataset
- 10 companies: AAPL, MSFT, GOOGL, AMZN, META, NVDA, JPM, GS, TSLA, NFLX
- 9 quarters each: Q1 2024 – Q4 2025 + Q1 2026
- 90 transcripts total — manually collected from Motley Fool / Seeking Alpha / TickerTrends
- Q1 2026 reserved as holdout test set

## Status
🚧 In development — Sprint 1 of 13 (Data Collection Pipeline)