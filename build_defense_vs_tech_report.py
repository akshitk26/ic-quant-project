from __future__ import annotations

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import yfinance as yf
from arch import arch_model
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

PDF_PATH = BASE_DIR / "defense_vs_tech_summary_report.pdf"
SOURCE_PATH = BASE_DIR / "defense_vs_tech_summary_report_source.md"

TICKERS = ["LMT", "NOC", "GD", "XLK"]
DEFENSE_TICKERS = ["LMT", "NOC", "GD"]
TECH_TICKER = "XLK"
START_DATE = "2020-01-01"
END_DATE = "2025-12-31"
ROLLING_WINDOW = 30
MOMENTUM_WINDOW = 30
TRADING_DAYS_PER_YEAR = 252


def annualize_return(series: pd.Series) -> float:
    compounded = (1 + series).prod()
    return compounded ** (TRADING_DAYS_PER_YEAR / len(series)) - 1


def annualize_volatility(series: pd.Series) -> float:
    return series.std() * np.sqrt(TRADING_DAYS_PER_YEAR)


def max_drawdown(series: pd.Series) -> float:
    curve = (1 + series).cumprod()
    return (curve / curve.cummax() - 1).min()


def pair_regression(target: pd.Series, benchmark: pd.Series) -> dict[str, float]:
    aligned = pd.concat([target, benchmark], axis=1).dropna()
    aligned.columns = ["target", "benchmark"]
    x = sm.add_constant(aligned["benchmark"])
    model = sm.OLS(aligned["target"], x).fit()
    fitted = model.predict(x)
    resid = aligned["target"] - fitted
    rss = float((resid**2).sum())
    tss = float(((aligned["target"] - aligned["target"].mean()) ** 2).sum())
    return {
        "r_squared": float(model.rsquared),
        "beta": float(model.params["benchmark"]),
        "rss": rss,
        "tss": tss,
    }


def get_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = yf.download(
        TICKERS,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=False,
        progress=False,
        group_by="column",
    )
    adj_close = raw["Adj Close"].sort_index().ffill().dropna(how="all")
    returns = adj_close.pct_change().dropna()
    return adj_close, returns


def rolling_volatility(returns: pd.DataFrame) -> pd.DataFrame:
    return returns.rolling(ROLLING_WINDOW).std() * np.sqrt(TRADING_DAYS_PER_YEAR)


def garch_volatility(returns: pd.DataFrame) -> pd.DataFrame:
    data: dict[str, pd.Series] = {}
    for ticker in returns.columns:
        series = returns[ticker].dropna() * 100
        fit = arch_model(series, vol="Garch", p=1, q=1, mean="Zero", dist="normal").fit(disp="off")
        data[ticker] = fit.conditional_volatility / 100 * np.sqrt(TRADING_DAYS_PER_YEAR)
    return pd.DataFrame(data)


def backtest_biased_regime_strategy(
    returns: pd.DataFrame,
    prices: pd.DataFrame,
    rolling_vol: pd.DataFrame,
) -> pd.Series:
    signal = rolling_vol[TECH_TICKER].dropna()
    low_cutoff = signal.quantile(0.33)
    high_cutoff = signal.quantile(0.67)
    trailing_return = prices[DEFENSE_TICKERS + [TECH_TICKER]].pct_change(MOMENTUM_WINDOW)
    trailing_vol = rolling_vol[DEFENSE_TICKERS]
    vals = []
    idx = []
    for date in signal.index.intersection(returns.index):
        vol_value = signal.loc[date]
        if vol_value <= low_cutoff:
            chosen = TECH_TICKER
        elif vol_value <= high_cutoff:
            chosen = trailing_return.loc[date, DEFENSE_TICKERS].idxmax()
        else:
            chosen = trailing_vol.loc[date, DEFENSE_TICKERS].idxmin()
        idx.append(date)
        vals.append(returns.loc[date, chosen])
    return pd.Series(vals, index=idx)


def backtest_lagged_regime_strategy(
    returns: pd.DataFrame,
    prices: pd.DataFrame,
    rolling_vol: pd.DataFrame,
) -> pd.Series:
    signal = rolling_vol[TECH_TICKER].dropna()
    low_cutoff = signal.quantile(0.33)
    high_cutoff = signal.quantile(0.67)
    trailing_return = prices[DEFENSE_TICKERS + [TECH_TICKER]].pct_change(MOMENTUM_WINDOW)
    trailing_vol = rolling_vol[DEFENSE_TICKERS]
    vals = []
    idx = []
    eligible_dates = signal.index.intersection(returns.index)
    for signal_date in eligible_dates[:-1]:
        trade_date = returns.index[returns.index.get_loc(signal_date) + 1]
        vol_value = signal.loc[signal_date]
        if vol_value <= low_cutoff:
            chosen = TECH_TICKER
        elif vol_value <= high_cutoff:
            chosen = trailing_return.loc[signal_date, DEFENSE_TICKERS].idxmax()
        else:
            chosen = trailing_vol.loc[signal_date, DEFENSE_TICKERS].idxmin()
        idx.append(trade_date)
        vals.append(returns.loc[trade_date, chosen])
    return pd.Series(vals, index=idx)


def indexed_curve(series: pd.Series) -> pd.Series:
    return (1 + series.fillna(0)).cumprod() * 100


def build_charts(prices: pd.DataFrame, returns: pd.DataFrame) -> dict[str, Path]:
    sns.set_theme(style="whitegrid")
    plt.rcParams["figure.figsize"] = (11, 5.8)

    rolling_vol = rolling_volatility(returns)
    garch_vol = garch_volatility(returns)
    biased = backtest_biased_regime_strategy(returns, prices, rolling_vol)
    lagged = backtest_lagged_regime_strategy(returns, prices, rolling_vol)

    biased_curve = indexed_curve(biased)
    lagged_curve = indexed_curve(lagged)
    xlk_biased_curve = indexed_curve(returns.loc[biased.index, TECH_TICKER])
    xlk_lagged_curve = indexed_curve(returns.loc[lagged.index, TECH_TICKER])

    chart_paths = {
        "garch": OUTPUT_DIR / "defense_garch_volatility.png",
        "dist": OUTPUT_DIR / "defense_return_distributions.png",
        "biased": OUTPUT_DIR / "defense_biased_regime_strategy.png",
        "lagged": OUTPUT_DIR / "defense_lagged_regime_strategy.png",
    }

    plt.figure()
    for ticker in TICKERS:
        plt.plot(garch_vol.index, garch_vol[ticker], linewidth=2, label=ticker)
    plt.title("GARCH Conditional Volatility")
    plt.xlabel("Date")
    plt.ylabel("Annualized Conditional Volatility")
    plt.legend(title="Ticker")
    plt.tight_layout()
    plt.savefig(chart_paths["garch"], dpi=180)
    plt.close()

    plt.figure()
    for ticker in TICKERS:
        kurt = returns[ticker].kurtosis()
        sns.kdeplot(returns[ticker], fill=False, linewidth=2, label=f"{ticker}  kurtosis={kurt:.2f}")
    plt.title("Daily Return Distributions")
    plt.xlabel("Daily Return")
    plt.ylabel("Density")
    plt.legend(title="Ticker")
    plt.tight_layout()
    plt.savefig(chart_paths["dist"], dpi=180)
    plt.close()

    plt.figure()
    plt.plot(biased_curve.index, biased_curve.values, linewidth=2, label="Biased Regime Strategy")
    plt.plot(xlk_biased_curve.index, xlk_biased_curve.values, linewidth=2, label="XLK")
    plt.title("Biased Regime Strategy vs XLK")
    plt.xlabel("Date")
    plt.ylabel("Indexed Value")
    plt.legend(title="Series")
    plt.tight_layout()
    plt.savefig(chart_paths["biased"], dpi=180)
    plt.close()

    plt.figure()
    plt.plot(lagged_curve.index, lagged_curve.values, linewidth=2, label="Lagged Regime Strategy")
    plt.plot(xlk_lagged_curve.index, xlk_lagged_curve.values, linewidth=2, label="XLK")
    plt.title("Lagged Regime Strategy vs XLK")
    plt.xlabel("Date")
    plt.ylabel("Indexed Value")
    plt.legend(title="Series")
    plt.tight_layout()
    plt.savefig(chart_paths["lagged"], dpi=180)
    plt.close()

    return chart_paths


def build_context(prices: pd.DataFrame, returns: pd.DataFrame) -> dict[str, str]:
    summary = pd.DataFrame(
        {
            ticker: {
                "annual_return": annualize_return(returns[ticker]),
                "annual_volatility": annualize_volatility(returns[ticker]),
                "max_drawdown": max_drawdown(returns[ticker]),
                "kurtosis": returns[ticker].kurtosis(),
            }
            for ticker in TICKERS
        }
    ).T

    rolling_vol = rolling_volatility(returns)
    biased = backtest_biased_regime_strategy(returns, prices, rolling_vol)
    lagged = backtest_lagged_regime_strategy(returns, prices, rolling_vol)
    biased_curve = indexed_curve(biased)
    lagged_curve = indexed_curve(lagged)
    xlk_biased_curve = indexed_curve(returns.loc[biased.index, TECH_TICKER])
    xlk_lagged_curve = indexed_curve(returns.loc[lagged.index, TECH_TICKER])

    regressions = pd.DataFrame({ticker: pair_regression(returns[ticker], returns[TECH_TICKER]) for ticker in DEFENSE_TICKERS}).T

    return {
        "best_return": summary["annual_return"].idxmax(),
        "lowest_vol": summary["annual_volatility"].idxmin(),
        "weakest_corr": returns[DEFENSE_TICKERS + [TECH_TICKER]].corr().loc[DEFENSE_TICKERS, TECH_TICKER].idxmin(),
        "strongest_fit": regressions["r_squared"].idxmax(),
        "highest_kurt": summary["kurtosis"].idxmax(),
        "biased_end": f"{float(biased_curve.iloc[-1]):.1f}",
        "lagged_end": f"{float(lagged_curve.iloc[-1]):.1f}",
        "xlk_biased_end": f"{float(xlk_biased_curve.iloc[-1]):.1f}",
        "xlk_lagged_end": f"{float(xlk_lagged_curve.iloc[-1]):.1f}",
        "lmt_kurtosis": f"{summary.loc['LMT', 'kurtosis']:.2f}",
        "noc_kurtosis": f"{summary.loc['NOC', 'kurtosis']:.2f}",
        "gd_kurtosis": f"{summary.loc['GD', 'kurtosis']:.2f}",
        "xlk_kurtosis": f"{summary.loc['XLK', 'kurtosis']:.2f}",
    }


def load_source_text(context: dict[str, str]) -> list[str]:
    text = SOURCE_PATH.read_text()
    return text.format(**context).splitlines()


def build_pdf(chart_paths: dict[str, Path], context: dict[str, str]) -> None:
    pdfmetrics.registerFont(TTFont("Arial", "/System/Library/Fonts/Supplemental/Arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="BodyArial", fontName="Arial", fontSize=12, leading=18, spaceAfter=10))
    styles.add(ParagraphStyle(name="TitleArial", fontName="Arial-Bold", fontSize=16, leading=20, alignment=TA_CENTER, spaceAfter=12))
    styles.add(ParagraphStyle(name="HeadingArial", fontName="Arial-Bold", fontSize=12, leading=18, spaceAfter=8))
    styles.add(ParagraphStyle(name="CaptionArial", fontName="Arial", fontSize=11, leading=16.5, spaceAfter=10))

    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    )

    image_map = {
        "garch": chart_paths["garch"],
        "dist": chart_paths["dist"],
        "biased": chart_paths["biased"],
        "lagged": chart_paths["lagged"],
    }

    story = []
    for raw_line in load_source_text(context):
        line = raw_line.strip()
        if not line:
            story.append(Spacer(1, 0.04 * inch))
            continue
        if line.startswith("# "):
            story.append(Paragraph(line[2:], styles["TitleArial"]))
            continue
        if line.startswith("## "):
            story.append(Paragraph(line[3:], styles["HeadingArial"]))
            continue
        if line.startswith("[[IMAGE:"):
            payload = line.removeprefix("[[IMAGE:").removesuffix("]]")
            key, caption = payload.split("|", 1)
            story.append(Image(str(image_map[key]), width=6.5 * inch, height=3.35 * inch))
            story.append(Spacer(1, 0.06 * inch))
            story.append(Paragraph(caption, styles["CaptionArial"]))
            continue
        if line.startswith("- "):
            story.append(Paragraph(f"• {line[2:]}", styles["BodyArial"]))
            continue
        story.append(Paragraph(line, styles["BodyArial"]))

    doc.build(story)


def main() -> None:
    prices, returns = get_data()
    chart_paths = build_charts(prices, returns)
    context = build_context(prices, returns)
    build_pdf(chart_paths, context)
    print(f"wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
