# QuantAI-OS: Institutional Research Terminal

## Project Overview

QuantAI-OS is a production-grade quantitative analysis command-line interface (CLI) designed for institutional-grade financial research and trading analysis. This tool provides comprehensive quantitative analysis of stocks using machine learning models, market regime detection, and risk management techniques.

## Purpose

The primary purpose of QuantAI-OS is to democratize access to institutional-quality quantitative analysis tools. In traditional finance, sophisticated quantitative models and risk management systems are typically only available to large financial institutions with dedicated quant teams. This project bridges that gap by providing:

- **Professional-grade analysis**: Using the same methodologies employed by hedge funds and investment banks
- **Machine learning predictions**: Ensemble models combining multiple algorithms for robust signal generation
- **Risk-aware position sizing**: Kelly Criterion-based allocation that adjusts for market conditions
- **Market regime awareness**: Hidden Markov Model detection of volatility states
- **Automated reporting**: Markdown reports for documentation and compliance
- **Database persistence**: Historical signal tracking and performance analysis

## Why We Built It

QuantAI-OS was developed to address several key challenges in modern quantitative trading:

1. **Accessibility**: Most retail traders lack access to professional quant tools
2. **Risk Management**: Many trading strategies fail due to poor position sizing and market timing
3. **Model Robustness**: Single-model approaches are prone to overfitting and regime-specific failures
4. **Documentation**: Institutional workflows require comprehensive audit trails
5. **Scalability**: Need for automated, repeatable analysis processes

The project combines cutting-edge machine learning techniques with time-tested quantitative finance principles to create a reliable, production-ready analysis platform.

## What It Does

### Core Features

#### 1. Quantitative Stock Analysis
- Fetches historical price data using Yahoo Finance API
- Engineers technical and statistical features from raw price data
- Applies multiple machine learning models for price direction prediction

#### 2. Market Regime Detection
- Uses Hidden Markov Models (HMM) to identify market volatility states
- Classifies markets as High Volatility, Medium Volatility, or Low Volatility
- Adjusts risk parameters based on current market conditions

#### 3. Ensemble Machine Learning
- Combines Gradient Boosting and Elastic Net models
- Provides confidence scores and win probability estimates
- Reduces overfitting through model averaging

#### 4. Risk-Aware Position Sizing
- Implements Kelly Criterion for optimal position sizing
- Adjusts allocations based on market regime (more conservative in high volatility)
- Provides half-Kelly recommendations for risk management

#### 5. AI-Powered Commentary
- Generates natural language analysis using Groq AI
- Explains model predictions and risk factors
- Provides investment rationale and caveats

#### 6. Professional Reporting
- Creates detailed Markdown reports with charts and tables
- Includes all analysis components in structured format
- Suitable for compliance and record-keeping

#### 7. Database Integration
- Stores all analysis signals in SQLite database
- Tracks historical predictions and performance
- Enables backtesting and strategy evaluation

### Technical Architecture

- **Language**: Python 3.10+
- **CLI Framework**: Typer for command-line interface
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn, HMMlearn
- **Visualization**: Rich library for terminal UI
- **Database**: SQLAlchemy with SQLite
- **AI Integration**: Groq API for commentary generation

### Usage Example

```bash
# Analyze Apple stock
python main.py analyze AAPL

# View historical signals
python main.py history

# List generated reports
python main.py list-reports
```

### Output Format

The tool provides Bloomberg Terminal-style output with:
- Real-time analysis results
- Regime probability distributions
- Model confidence scores
- Position sizing recommendations
- ASCII sparkline charts
- AI-generated commentary

## Target Audience

- Quantitative traders and analysts
- Portfolio managers requiring systematic analysis
- Financial researchers developing trading strategies
- Individual investors seeking professional-grade tools
- Educational institutions teaching quantitative finance

## Project Status

**Version**: 2.0.0 (Beta)  
**License**: MIT  
**Development Status**: Active development with production-ready features

This project represents a comprehensive solution for quantitative analysis in finance, combining academic rigor with practical usability.

## Disclaimer

This project is for educational and research purposes only. It is not intended to be used as financial advice or for making actual investment decisions. Trading stocks and financial instruments involves significant risk.
