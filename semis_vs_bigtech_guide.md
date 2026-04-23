# Semis vs Big Tech Notebook Guide

## Purpose

This guide tracks the new `SOXX` versus `QQQ` notebook and keeps the deliverable notes synced with the implementation in [semis_vs_bigtech_analysis.ipynb](/Users/akshit/Code/IC%20Quant%20Project/semis_vs_bigtech_analysis.ipynb:1).

## Current Notebook Structure

1. Project framing
2. Environment bootstrap
3. Imports and config
4. Data choices
5. Data loading and preprocessing
6. Concepts: GARCH, RSS, TSS, Ridge, Lasso
7. Statistics and modeling
8. Section 1: core pair analysis
9. Section 2: regression diagnostics
10. Section 3: semis amplification strategy
11. Section 4: mean-reversion pairs trade
12. Section 5: mean reversion with QQQ trend filter and asymmetric SOXX short
13. Quick interpretation prompts

## Current High-Level Decisions

- The main pair is `SOXX` versus `QQQ`.
- The notebook uses the last five years of data dynamically at runtime.
- Returns and risk metrics use `Adj Close`.
- Missing values are audited first and then forward-filled conservatively.
- The graph set is intentionally compact:
  - normalized price performance
  - rolling annualized volatility
  - rolling correlation
  - return distributions
  - GARCH conditional volatility
  - strategy comparison
- GARCH is included to show time-varying volatility more formally than the rolling-vol chart.
- RSS and TSS are included through the pair regression diagnostics.
- Regularization is included through a simple OLS/Ridge/Lasso next-day return comparison.
- The notebook now contains three strategy variants:
  - semis amplification
  - raw stat-arb mean reversion
  - stat-arb mean reversion with a `QQQ` trend filter and asymmetric `SOXX` short

## What the Notebook Covers

### Data Collection & Cleaning

- Yahoo Finance via `yfinance`
- `SOXX` and `QQQ`
- last five years of daily data
- missing-value audit
- forward fill
- adjusted-close returns

### EDA & Visualizations

- normalized performance chart
- rolling annualized volatility chart
- rolling correlation chart
- return distributions
- GARCH volatility chart
- strategy comparison chart

### Modeling / Statistical Analysis

- pair regression of `SOXX` returns on `QQQ` returns
- beta and alpha
- correlation and `R^2`
- RSS and TSS
- OLS, Ridge, and Lasso comparison on a small predictive feature set

### Insights & Interpretation

- whether semis acted like a leveraged expression of big tech
- whether volatility clustered materially during AI-driven periods
- whether the selective semis-tilt strategy improved on `QQQ`
- whether spread dislocations were more useful than outright sector rotation
- whether a broad-tech trend filter reduced stat-arb drawdowns
- whether adding a selective SOXX short improved weak-regime performance

## Strategy Logic

### 1. Semis Amplification

- hold `QQQ` by default
- switch into `SOXX` only when:
  - `QQQ` 30-day momentum is positive
  - `SOXX / QQQ` relative strength is above its 50-day moving average
  - `SOXX` rolling volatility is not too far above `QQQ`

### 2. Raw Stat-Arb Mean Reversion

- compute a rolling Z-score on the `SOXX / QQQ` ratio
- buy `SOXX` when the ratio is unusually cheap
- otherwise default back to `QQQ`

### 3. Filtered Stat-Arb Mean Reversion With Short Side

- keep the same spread Z-score signal
- buy the `SOXX` dip when `QQQ` is still above its 50-day moving average
- short `SOXX` when it is rich versus `QQQ` and `QQQ` is below its 50-day moving average
- otherwise remain in `QQQ`

This filtered version is designed to avoid fading semiconductors during larger big-tech downtrends while still capturing some downside when the spread is stretched in a weak regime.

## PDF Summary Structure

Recommended structure:

1. Project question
2. Dataset and source
3. Methods
4. Key findings
5. Strategy takeaway
6. Reflection and limitations

## Slide Guidance

Best options for the one-slide deck:

- normalized performance plus one takeaway sentence
- rolling correlation plus one sentence on supply-chain linkage
- strategy comparison if one of the three variants is strong enough to discuss

## What To Update If the Notebook Changes

- ticker set
- sample period
- cleaning method
- rolling windows
- GARCH usage
- regression feature set
- strategy rule
- trend filter definition
- short-side rule
- report / slide recommendations
