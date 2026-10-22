# vol-forecast

Forecasting stock volatility: statistical baseline (GARCH) vs. machine learning,
evaluated with walk-forward validation.

## Question
Does an ML model beat simple baselines at predicting next-period volatility?
An honest "no, because..." is an acceptable result.

## Roadmap
- [x] 1. Data: download prices, store in SQLite, incremental updates
- [ ] 2. Baselines: rolling-window volatility, GARCH (`arch`)
- [ ] 3. ML: features + linear regression, LightGBM
- [ ] 4. Comparison: RMSE / QLIKE, calm vs. crisis periods
- [ ] 5. FastAPI endpoint, Docker, write-up
- [ ] Extension: anomaly detection, portfolio risk

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m volforecast.ingest AAPL MSFT   # fill data/prices.db
pytest
```

## Design decisions
(Fill in as you go: why these tickers, why this metric, what failed.)
