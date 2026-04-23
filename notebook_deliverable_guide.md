# Defense vs Tech Notebook Companion Guide

This guide stays in sync with [defense_vs_tech_analysis.ipynb](/Users/akshit/Code/IC%20Quant%20Project/defense_vs_tech_analysis.ipynb:1) and explains the notebook's final scope, structure, and presentation angle.

## Purpose

The notebook answers a focused question:

How well do major defense names (`LMT`, `NOC`, `GD`) diversify or track the technology sector proxy `XLK` over the last five years?

The final version is cleaner than the earlier drafts, but it still keeps the two strategy sections you wanted:

- the regime strategy
- the momentum-with-defense-filter strategy

The notebook now balances four things:

- clean descriptive analysis
- GARCH-based volatility modeling
- light regression / regularization modeling
- a compact strategy section that illustrates what did and did not work

## Final Notebook Structure

1. Title and framing
2. Environment bootstrap
3. Imports and config
4. Data choices and cleaning notes
5. Data loading / preprocessing
6. Concepts for GARCH, `R^2`, `TSS`, `RSS`, Ridge, and Lasso
7. Core statistics, GARCH volatility, regression diagnostics, regularization, and strategy tables
8. Core visualizations
9. Chart interpretation notes
10. Strategy Section 1: regime strategy
11. Strategy Section 2: momentum with defense filter
12. Insight generation
13. Reflection prompts

## What Was Removed

To keep the notebook cleaner and easier to present, the final version removes:

- rolling beta plots
- rolling drawdown path plots
- drawdown-triggered lowest-beta strategy
- extra strategy clutter beyond the two strategy sections above
- hedged spread visuals

Those sections made the notebook longer without improving the main story enough.

## Current High-Level Decisions

- The deliverable is a real `.ipynb` notebook.
- Data source is Yahoo Finance through `yfinance`.
- The main price field is `Adj Close`.
- Missing values are audited first, then forward-filled conservatively.
- Analysis uses daily data from `2020-01-01` through `2025-12-31`.
- The main rolling window is `30` trading days.
- The notebook is analytical first, but still includes two compact strategy diagnostics.

## What the Notebook Covers

### Data Cleaning and Preprocessing

- downloads Yahoo Finance history for `LMT`, `NOC`, `GD`, and `XLK`
- checks missing values before cleaning
- aligns the price series into one table
- forward-fills small gaps
- computes daily returns
- normalizes price performance to a common base of `100`

### Exploratory Data Analysis

- normalized price performance chart
- 30-day rolling annualized volatility chart
- GARCH conditional volatility chart
- full-period correlation heatmap
- 30-day rolling correlation versus `XLK`
- return distribution comparison
- regime summary table based on 30-day `XLK` volatility buckets

### Statistical Modeling

- pair regressions of each defense stock on `XLK`
- reported diagnostics:
  - correlation
  - beta
  - alpha
  - `R^2`
  - `RMSE`
  - `MAE`
  - `RSS`
  - `TSS`
  - `RSS / TSS`
- simple predictive comparison using:
  - OLS
  - Ridge
  - Lasso

### Strategy Diagnostics

- biased regime strategy chart to show a false positive created by same-day information leakage
- corrected lagged regime strategy chart
- momentum-with-defense-filter strategy chart
- summary tables for both strategies

These sections help show that strategy intuition needed to be tested carefully rather than assumed.

## Rubric Mapping

### 1. Data Cleaning / Preprocessing

Rubric item:
Handle missing values, inconsistent formats, and structural issues.

Notebook match:
- missing-value audit table
- unified adjusted-close extraction
- aligned date index across tickers
- conservative forward fill

Rubric item:
Perform any necessary normalization, resampling, or smoothing.

Notebook match:
- normalized price chart with base `100`
- rolling 30-day volatility and correlation windows for smoothing
- GARCH conditional volatility as a model-based volatility estimate

### 2. Exploratory Data Analysis

Rubric item:
Generate time-series visualizations to highlight key patterns or anomalies.

Notebook match:
- normalized performance
- rolling volatility
- GARCH conditional volatility
- rolling correlation
- return distributions
- strategy comparison charts

Rubric item:
Compute and visualize moving averages, rolling volatility, correlations, or autocorrelation structures.

Notebook match:
- rolling volatility
- GARCH volatility modeling
- rolling correlation
- momentum filter logic indirectly uses rolling trend information

Rubric item:
Segment data into regimes or patterns.

Notebook match:
- volatility regime table using 30-day `XLK` volatility terciles
- regime strategy section based on low / medium / high volatility states

### 3. Statistical Modeling or Forecasting

Rubric item:
Choose and apply a suitable time-series model.

Notebook match:
- GARCH volatility model
- pair regression framework
- next-day predictive comparison using lagged-return features with OLS, Ridge, and Lasso

Rubric item:
Evaluate model performance using appropriate metrics.

Notebook match:
- `R^2`
- `RMSE`
- `MAE`
- `RSS`
- `TSS`

### 4. Insight Generation

Rubric item:
Summarize meaningful observations or anomalies from the data.

Notebook match:
- final printed takeaways
- chart notes section
- biased vs corrected regime strategy comparison

Rubric item:
Provide commentary on temporal trends, relationships, or predictive dynamics.

Notebook match:
- normalized performance interpretation
- changing rolling correlations
- regression fit comparisons
- regularization comparison results
- strategy results showing how difficult it was to beat `XLK`

Rubric item:
Propose basic high-level strategy implications based on findings.

Notebook match:
- regime strategy section
- momentum filter section
- final reflection questions

## What to Emphasize in the PDF Summary

Keep the PDF concise. A good structure is:

1. Question
   Compare major defense stocks with `XLK` to test whether defense behaves as a useful diversifier or partial hedge to tech.

2. Data and method
   Explain Yahoo Finance source, `Adj Close`, missing-value audit, forward fill, daily returns, 30-day rolling windows, pair regressions, and the two compact strategy tests.

3. Main findings
   Focus on:
   - long-run relative performance
   - volatility differences
   - unstable rolling correlation
   - which stock was least tied to `XLK`
   - whether predictive models added much value
   - why the biased regime strategy overstated performance

4. Conclusion
   State whether the evidence supports a simple “defense hedges tech” story and whether simple overlay strategies added value over holding `XLK`.

## What to Put on the One-Slide Deck

A clean one-slide structure:

- Title at the top:
  `Defense vs Tech: Do Defense Stocks Really Diversify XLK?`

- Left side:
  one chart, preferably rolling correlation or normalized performance

- Right side:
  3 short bullets
  - defense generally lagged `XLK` in cumulative performance
  - correlation with `XLK` changed materially over time
  - simple defense-overlay strategies were not enough to reliably beat `XLK`

- Bottom:
  one-sentence conclusion

## Best Talking Points

- `Adj Close` is the right field for return analysis because it reflects investor-relevant adjustments.
- A single full-period correlation is not enough; rolling correlations show the relationship changes over time.
- Some defense names are less tied to `XLK` than others, but none provide a perfect hedge.
- The regularization section adds a modest predictive extension without making the notebook feel overbuilt.
- The biased regime chart is useful because it shows how easy it is to create a false positive in backtesting.
- The strongest final takeaway is about the limits of simple sector-hedging assumptions.


## Notebook Maintenance

- Comments were added directly in the code cells to make the notebook easier to read during presentation and editing.
- Comments stay short and functional so the notebook does not become visually noisy.
