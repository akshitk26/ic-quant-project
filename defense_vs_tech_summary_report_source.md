# Defense vs Tech Summary Analysis Report

## Dataset and source
This project uses daily adjusted closing prices for Lockheed Martin `LMT`, Northrop Grumman `NOC`, General Dynamics `GD`, and the Technology Select Sector SPDR Fund `XLK` from Jan 2020 - Dec 2025 (yfinance).

## Analysis methods
- normalized price performance comparisons
- 30-day rolling volatility to show how risk changed through time
- GARCH conditional volatility to estimate how volatility clustered after market shocks
- daily return distributions to compare tail behavior and kurtosis
- rolling correlations versus `XLK`
- pair regressions versus `XLK` with `R^2`, `RSS`, and `TSS`

## Key findings
- `XLK` had the strongest long-run performance in the sample, while `{lowest_vol}` had the lowest annualized volatility.
- `{weakest_corr}` had the weakest full-period correlation to `XLK`, so it was the best candidate for conditional diversification.
- `{strongest_fit}` had the strongest regression fit to `XLK`, which means it behaved most like a tech-sensitive equity among the defense names.
- `{highest_kurt}` had the highest kurtosis, meaning its return distribution had the fattest tails and the greatest tendency toward unusually large daily moves.

## Visual 1: GARCH conditional volatility
[[IMAGE:garch|A GARCH(1,1) model mathematically captures "volatility clustering", which is that large price swings tend to be followed by larger price swings. It provides a dynamic estimate of how unstable each asset is immediately after absorbing recent market shocks. The main takeaway is that risk is not static and volatility clearly came in distinct clusters across the sample. `XLK` generally experienced the most persistent high volatility bursts, while the defense names were usually calmer but still reacted sharply during market stress.]]

## Visual 2: daily return distributions
[[IMAGE:dist|Figure 2. Daily return distributions with kurtosis labels. Kurtosis helps explain tail risk: higher kurtosis means more weight in the tails and therefore a greater chance of unusually large daily moves. This matters because two assets can have similar average returns but very different downside and tail behavior.]]

## Visual 3/4: biased regime strategy vs lagged regime strategy
I built a regime-switching strategy based strictly on `XLK`'s rolling volatility percentiles. When tech volatility was low (bottom 33%), the strategy stayed completely invested in `XLK` to capture its upside trend. When tech volatility shifted to a medium range (33%-67%), it rotated into whichever defense stock had the strongest recent momentum to secure stability. Finally, during high volatility (top 33%), it moved into the defensive stock showing the lowest absolute trailing volatility. 

[[IMAGE:biased|Figure 3. The biased version of this regime rotation model ended near `{biased_end}` while `XLK` ended near `{xlk_biased_end}` over the same aligned time window. At first, this looks like compelling evidence that defensively rotating out of tech during market shocks consistently increased long-term gains. However, this test used the day's closing volatility calculation to trade the exact same day's return. That immediately made a lookahead bias, meaning the strategy was unintentionally allowed to react to future information that the trader could not have possibly known in real time.]]

[[IMAGE:lagged|Figure 4. To correct this, we shifted the execution logic back to reality: we compute the volatility signal based on today's close, but apply the portfolio change to tomorrow's daily returns. Once the execution was properly delayed by one trading day, the entire strategy collapsed, driving the terminal value down to `{lagged_end}` compared to `XLK`'s `{xlk_lagged_end}`. This properly lagged version exposes the earlier outperformance as almost entirely a false positive driven purely by lookahead bias rather than genuine timing skill.]]

## Reflection
The clearest conclusion is not that a defense rotation strategy consistently beat tech. Instead, the evidence indicates that defense stocks served only as partial and unstable diversifiers against `XLK`. While these assets exhibited lower overall volatility, their correlations with the broader tech sector often spiked during periods of acute market stress, which is precisely when a hedge is needed most. This structural instability means that defense equities cannot be treated as a static or guaranteed safe haven. The strongest final takeaway is that diversification and market timing claims require rigorous statistical analysis. Strategies that seem intuitive on a surface level can easily disappear once they are subjected to realistic constraints like delayed execution and imperfect knowledge.
