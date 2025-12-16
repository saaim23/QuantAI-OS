# QuantAI-OS - Institutional Research Terminal

## Overview
QuantAI-OS is a production-grade quantitative analysis CLI tool for stock market analysis. It uses machine learning models (HistGradientBoosting, ElasticNet), Hidden Markov Models for regime detection, and Kelly Criterion for position sizing.

## Project Structure
```
├── src/
│   └── quantai/
│       ├── __init__.py          # Package initialization
│       ├── cli.py               # Main CLI entry point
│       ├── config.py            # Configuration via .env
│       ├── database.py          # SQLite database handler
│       ├── logger.py            # Logging system
│       ├── visualization.py     # ASCII charts
│       ├── data/                # Data layer
│       │   ├── loader.py        # Yahoo Finance data fetcher
│       │   └── features.py      # Feature engineering
│       ├── models/              # ML models
│       │   ├── trees.py         # Gradient boosting
│       │   ├── linear.py        # ElasticNet
│       │   └── ensemble.py      # Model ensemble
│       ├── risk/                # Risk management
│       │   ├── regimes.py       # HMM regime detection
│       │   └── sizing.py        # Kelly criterion
│       └── ai/                  # AI commentary
│           └── commentary.py    # Groq LLM integration
├── main.py                      # Entry point
├── requirements.txt             # Dependencies
├── pyproject.toml               # Project configuration
├── .env.example                 # Example environment file
└── .gitignore                   # Git ignore rules
```

## Usage
```bash
# Analyze a stock
python main.py analyze AAPL

# View signal history
python main.py history

# List generated reports
python main.py list-reports

# Show version
python main.py version
```

## Configuration
Copy `.env.example` to `.env` and configure:
- `GROQ_API_KEY`: Optional, for AI commentary

## Dependencies
Uses standard Python libraries only:
- yfinance: Market data
- pandas/numpy: Data processing
- scikit-learn: ML models
- hmmlearn: Regime detection
- typer/rich: CLI interface
- sqlalchemy: Database
- pydantic: Configuration
- python-dotenv: Environment loading
- groq: AI commentary (optional)

## Portability
This codebase is fully portable and can run on any machine with Python 3.10+.
All Replit-specific configuration is in separate files (.replit, replit.nix).
