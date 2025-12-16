# What is the Terminal Showing?

When you run `python main.py analyze AAPL`, the terminal displays a professional quantitative analysis report. Here's what each section means:

---

## Header Section

```
+---------------------------------+
| TERMINAL  | QuantAI-OS v2.0.0   |
| TIMESTAMP | 2025-12-15 12:25:03 |
+---------------------------------+
```

This simply shows the tool name and when the analysis was run.

---

## Main Analysis Summary

```
| Ticker    | SPY                    |
| Company   | SPDR S&P 500 ETF       |
| Price     | $681.76                |
| Regime    | LOW VOL (2)            |
| Signal    | 0.79 (LONG)            |
| Kelly Size| 14.03%                 |
| Price(30D)| ~~--.-~~~--._.__.--~~  |
```

**What this tells you:**

- **Ticker/Company/Price**: Basic stock info and current market price
- **Regime**: The current market volatility state (explained below)
- **Signal**: A number from 0-1 showing confidence. Higher = stronger buy signal. "LONG" means the models predict the price will go UP. "SHORT" would mean they predict it will go DOWN.
- **Kelly Size**: How much of your portfolio you should theoretically invest (explained below)
- **Price (30D)**: A mini-chart showing the last 30 days of price movement. The `^` symbols mean higher prices, `_` means lower.

---

## Regime Probabilities

```
| HIGH VOL  |   0.0% | [................] |
| MED VOL   |   0.0% | [................] |
| LOW VOL   | 100.0% | [################] |
```

**What is a "Regime"?**

The system uses a Hidden Markov Model (HMM) to detect what "mode" the market is currently in:

- **HIGH VOL (High Volatility)**: The market is unstable and swinging wildly. This is risky - prices can jump up or crash down quickly. Think 2008 financial crisis or COVID crash.

- **MED VOL (Medium Volatility)**: The market is somewhat uncertain. Normal trading conditions with moderate ups and downs.

- **LOW VOL (Low Volatility)**: The market is calm and stable. Prices are moving smoothly without big surprises. This is generally considered safer for trend-following strategies.

**Why does this matter?** The system reduces your recommended position size during high volatility to protect you from big swings.

---

## Model Predictions

```
| GradientBoosting | LONG |  72.2% |  56.1% |
| ElasticNet       | LONG |  90.1% |  63.4% |
```

**What are these models?**

The system uses two machine learning models that learned from historical price patterns:

1. **GradientBoosting**: A decision-tree based algorithm that's good at finding complex patterns
2. **ElasticNet**: A linear model that finds simpler, more robust trends

**The columns mean:**

- **Direction**: LONG (buy/bullish) or SHORT (sell/bearish) - which way the model thinks the price will move
- **Confidence**: How sure the model is about its prediction (higher = more confident)
- **Accuracy**: How often this model was correct on test data (this is NOT a guarantee of future performance)

---

## Ensemble Result

```
| Direction       | LONG   |
| Confidence      | 79.4%  |
| Win Probability | 56.8%  |
```

**What is an Ensemble?**

Instead of trusting just one model, the system combines both models' predictions (weighted average). This is like getting a second opinion - it's often more reliable than any single model alone.

- **Direction**: The combined prediction (LONG = expect price to rise)
- **Confidence**: How confident the combined models are
- **Win Probability**: Estimated chance this trade would be profitable

---

## Position Sizing

```
| Full Kelly       | 28.07% |
| Recommended Size | 14.03% |
| Max Allowed      | 25.00% |
```

**What is Kelly Criterion?**

The Kelly Criterion is a mathematical formula used by professional traders and gamblers to determine the optimal bet size. It calculates: "Given my win probability and potential gains/losses, how much should I risk to maximize long-term growth?"

- **Full Kelly**: The mathematically "optimal" position (often too aggressive for real trading)
- **Recommended Size**: Half-Kelly adjusted for market regime (safer, what you should actually consider)
- **Max Allowed**: A hard cap to prevent over-betting (default 25%)

**Example**: If Recommended Size is 14.03%, this means the system suggests allocating about 14% of your portfolio to this trade.

---

## The Sparkline (Mini Price Chart)

```
Price (30D) | ~~--.-~~~--._.__.--~~~~~~~~~^~
```

This is a tiny ASCII chart showing recent price movement:
- `_` = Price at the low end of the range
- `.` = Price slightly below middle
- `-` = Price near middle
- `~` = Price slightly above middle  
- `^` = Price at the high end of the range

Reading left to right shows you how the price moved over the last 30 days.

---

## Important Disclaimer

This is a quantitative analysis tool for educational and research purposes. The predictions are based on historical patterns and machine learning models, which:

- Cannot predict the future with certainty
- May fail during unusual market conditions
- Should never be used as your sole basis for trading decisions

Always do your own research and consider consulting a financial advisor before making investment decisions.
