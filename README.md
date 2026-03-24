# Earnings Call Analyzer

NLP pipeline that extracts sentiment, confidence, and risk signals from public earnings call transcripts to detect narrative shifts and predict short-term stock price movement.

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
data/transcripts/     # Raw earnings call transcripts
data/prices.csv       # Stock prices before/after each call
src/                  # Pipeline scripts
models/               # Trained model artifacts
```

## Status
🚧 In development — Sprint 1 of 8 (Data Foundation)