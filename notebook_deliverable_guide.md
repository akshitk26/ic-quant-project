# Defense vs Tech Notebook Companion Guide

## Purpose

This file tracks the notebook structure, documents major implementation choices, and gives writing guidance for the required PDF summary and 1-slide presentation. It should stay in sync with the notebook at [defense_vs_tech_analysis.ipynb](/Users/akshit/Code/IC%20Quant%20Project/defense_vs_tech_analysis.ipynb:1).

## Current Notebook Structure

1. Title and project framing
2. Environment bootstrap and dependency installation
3. Imports and config
4. Data-choice explanation
5. Data loading and preprocessing
6. Statistical helper functions
7. Visualization helper functions
8. Regime concepts and interpretation notes
9. Section 1: core correlation and risk analysis
10. Section 2: regime strategy, including the original biased false-positive chart and the corrected lagged version
11. Section 3: drawdown-triggered lowest-beta strategy
12. Insight generation
13. Optional exports
14. Reflection prompts

## Current High-Level Decisions

- Notebook deliverable is a real `.ipynb`, matching the assignment PDF.
- Notebook now includes a bootstrap cell that installs missing packages into the active kernel before the main imports run.
- Returns, volatility, correlation, and hedge analysis use `Adj Close`.
- OHLCV is still downloaded so the dataset remains faithful to the stock-data requirement.
- Missing values are audited before cleaning.
- Forward fill is used conservatively after the audit so small data gaps do not break rolling calculations.
- Main rolling window is `30` trading days.
- Main analytical emphasis is:
  - correlation matrix
  - rolling volatility
  - rolling correlation versus XLK
  - rolling beta versus XLK
  - drawdown analysis
  - volatility-regime analysis
  - OLS hedge ratio and hedged spread interpretation
- A simple regime-switching strategy benchmark is now included:
  - low-vol regime: hold `XLK`
  - medium-vol regime: hold the defense stock with the strongest recent trailing return
  - high-vol regime: hold the defense stock with the lowest recent rolling volatility
- Strategy signals are now applied with a one-trading-day delay to avoid obvious lookahead bias in the backtest.
- A second strategy test is now included:
  - if `XLK` drawdown breaches `-10%`, switch the next day into the defense stock with the lowest rolling beta to `XLK`
  - otherwise remain in `XLK`
- The notebook now explicitly preserves the original biased regime chart as a cautionary example of a false positive.
- Strategy discussion remains high level. The notebook is analytical first, not a full trading-system build.

## Why These Choices Make Sense

- `Adj Close` is the best field for return analysis because it reflects investor-relevant price adjustments.
- A 30-day rolling window is short enough to reveal regime shifts but long enough to smooth daily noise.
- Rolling beta adds a stronger explanation of sensitivity than correlation alone because it measures magnitude, not just direction.
- OLS hedge analysis gives a simple and explainable modeling section that fits the assignment's statistical-analysis requirement without overengineering the project.
- Rolling metrics support a more credible conclusion than one full-period average because relationships between sectors change over time.

## What the Notebook Already Covers for the Rubric

### Data Collection & Cleaning

- Uses Yahoo Finance via `yfinance`
- Includes a kernel-local dependency bootstrap step to reduce environment issues
- Downloads market data for `LMT`, `NOC`, `GD`, and `XLK`
- Audits missing values
- Cleans and forward-fills price data
- Computes daily returns

### EDA & Visualizations

- Normalized performance line chart
- Rolling volatility chart
- Correlation matrix heatmap
- Rolling correlation chart
- Rolling beta chart
- Return distributions
- Cumulative hedged spread chart
- Drawdown chart
- Regime-strategy versus `XLK` comparison chart
- Biased regime-strategy versus `XLK` cautionary chart
- Drawdown-triggered lowest-beta strategy versus `XLK` comparison chart

### Modeling / Statistical Analysis

- OLS regressions of each defense stock against `XLK`
- Hedge ratio estimation
- Rolling beta versus `XLK`
- Regime table based on `XLK` rolling volatility
- Simple regime-switching backtest compared with `XLK`
- Backtest now uses one-day-lagged signals rather than same-day execution
- Drawdown-triggered lowest-beta strategy compared with `XLK`
- Regression diagnostics:
  - `R^2`
  - adjusted `R^2`
  - RMSE
  - MAE
  - AIC
  - BIC
- Volatility-regime summary table with a safe fallback if the sample does not produce three clean volatility buckets

### Insights & Interpretation

- Auto-generated key insights
- High-level strategy framing
- Regime definitions explained directly in the notebook
- Explicit comparison between biased and unbiased backtests
- Reflection questions for the written report

## How to Structure the PDF Summary

Target length: roughly 1-3 pages, but quality matters more than exact page count.

Recommended structure:

### 1. Project Overview

- State the question clearly:
  - How did defense contractors behave relative to the technology sector from 2020 to 2025?
- Explain why this is interesting:
  - sector diversification
  - risk behavior
  - regime changes

### 2. Dataset and Source

- Mention Yahoo Finance and `yfinance`
- List tickers:
  - `LMT`
  - `NOC`
  - `GD`
  - `XLK`
- State time period:
  - `2020-01-01` to `2025-12-31`
- Mention fields downloaded:
  - OHLCV plus `Adj Close`
- Explain that `Adj Close` was used for return analysis

### 3. Methods

- Briefly explain:
  - data cleaning and missing-value handling
  - daily return calculation
  - 30-day rolling volatility
- return correlation matrix
- rolling correlation versus `XLK`
- rolling beta versus `XLK`
- drawdown comparison
- volatility-regime classification
- regime-switching benchmark logic
- drawdown-triggered lowest-beta logic
- OLS hedge ratio estimation
- Keep this section concise and readable for a non-technical audience

### 4. Key Findings

- Use at least 2 visuals from the notebook
- Focus on 3-4 concrete findings, such as:
  - which stock had the highest return
  - which had the lowest volatility
- which defense name was least correlated with tech
- which defense name had the lowest beta to tech during stress periods
- which defense name had the shallowest drawdowns
- whether correlations changed materially over time
- whether the simple regime strategy improved risk-adjusted behavior against `XLK`
- whether the strategy still holds up after removing lookahead bias
- whether the drawdown-triggered lowest-beta rule improves drawdown control or just sacrifices upside
- which stock had the cleanest hedge relationship with `XLK`

### 5. Interpretation / Strategy Implication

- Keep this high level, not overly prescriptive
- Good framing examples:
  - diversification benefit was unstable over time
  - some defense names behaved more like market-sensitive cyclicals than expected
  - rolling analysis suggests static assumptions are weaker than dynamic monitoring

### 6. Reflection

- Briefly mention:
  - limitations of the analysis
  - what you would extend next
  - why rolling metrics improved the analysis over simple averages

## How to Structure the Single Slide

Goal: one polished takeaway, not a mini-report.

Recommended layout:

- Title:
  - `Defense vs Tech: Diversifier or Just Another Risk Asset?`
- Main visual:
  - rolling correlation versus `XLK`
  - or rolling volatility if that tells the cleaner story
- 2-3 short takeaway bullets
- One bottom-line sentence:
  - example: `Defense names were not consistently low-correlation hedges; the relationship with tech changed materially across market regimes.`

## Best Candidate Visuals for the Report and Slide

- Best for explaining relative performance:
  - normalized price performance
- Best for risk story:
  - 30-day rolling volatility
- Best for diversification story:
  - correlation matrix
  - rolling correlation versus `XLK`
- Best for a more advanced angle:
  - cumulative hedged spread chart
  - rolling beta versus `XLK`
  - regime strategy versus `XLK`

## What To Update Here Whenever the Notebook Changes

Each time the notebook is edited, update this file if any of the following changes:

- tickers
- sample period
- cleaning method
- rolling window
- model choice
- chart set
- export behavior
- written-report recommendations

## Next Likely Improvements

- Add a rolling beta chart versus `XLK`
- Add drawdown plots
- Add sector-event annotations for major macro or geopolitical periods
- Add a polished export workflow for report-ready PNG files
