"""Generate blog charts for the western political instability post."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import yaml
from matplotlib.ticker import MaxNLocator
WEST_POL_ROOT = Path(__file__).resolve().parents[2] / "west_pol_stability"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "assets/images/posts/western-political-instability"

BG = "#FFF1E0"
TEXT = "#585858"
ACCENT = "#BA7781"
SECONDARY = "#5E6D8F"
GRAY_MED = "#A9978E"
GRAY_LIGHT = "#E8DDD0"
PLOT_START = pd.Timestamp("1950-01-01")
PLOT_WINDOWS = [5, 10]
WINDOW_STYLE = {
    10: {"color": ACCENT, "linewidth": 2.8, "alpha": 1.0, "label": "10-year"},
    5: {"color": GRAY_MED, "linewidth": 1.4, "alpha": 0.85, "label": "5-year"},
}


def _style_matplotlib() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": [
                "Cormorant Garamond",
                "EB Garamond",
                "Garamond",
                "Liberation Serif",
                "Times New Roman",
            ],
            "text.color": TEXT,
            "axes.labelcolor": TEXT,
            "xtick.color": TEXT,
            "ytick.color": TEXT,
        }
    )


def _swd_axes(ax: plt.Axes) -> None:
    ax.set_facecolor(BG)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRAY_MED)
    ax.spines["bottom"].set_color(GRAY_MED)
    ax.tick_params(axis="both", colors=TEXT, labelsize=10, length=0, pad=6)
    ax.yaxis.grid(True, color=GRAY_LIGHT, linewidth=0.9)
    ax.set_axisbelow(True)


def _legend_above_xaxis(ax: plt.Axes, entries: list[tuple], y: float = 0.08) -> None:
    if not entries:
        return
    width = 0.82
    start = 0.09
    step = width / len(entries)
    for i, (line, label) in enumerate(entries):
        x_text = start + step * i + step * 0.12
        x_line_end = x_text - 0.015
        x_line_start = x_line_end - 0.055
        ax.plot(
            [x_line_start, x_line_end],
            [y, y],
            transform=ax.transAxes,
            color=line.get_color(),
            linestyle=line.get_linestyle(),
            linewidth=line.get_linewidth(),
            solid_capstyle="round",
            clip_on=False,
        )
        ax.text(
            x_text,
            y,
            label,
            transform=ax.transAxes,
            va="center",
            ha="left",
            fontsize=10,
            color=TEXT,
            clip_on=False,
        )


def _load_western_either() -> pd.DataFrame:
    processed = WEST_POL_ROOT / "data" / "processed"
    leader_events = pd.read_parquet(processed / "leader_events.parquet")
    coalition_events = pd.read_parquet(processed / "coalition_events.parquet")
    leader_events["event_date"] = pd.to_datetime(leader_events["event_date"])
    coalition_events["event_date"] = pd.to_datetime(coalition_events["event_date"])

    with open(WEST_POL_ROOT / "config" / "countries.yaml") as f:
        countries = yaml.safe_load(f)["countries"]

    either_events = (
        pd.concat(
            [
                leader_events[["country_id", "event_date"]],
                coalition_events[["country_id", "event_date"]],
            ],
            ignore_index=True,
        )
        .drop_duplicates(subset=["country_id", "event_date"])
        .sort_values(["country_id", "event_date"])
    )

    end_date = pd.Timestamp.today().normalize().replace(day=1) + pd.offsets.MonthEnd(0)
    either_rows: list[dict] = []

    for country in countries:
        country_id = country["id"]
        panel_start = pd.Timestamp(f"{country['start_year']}-01-01")
        country_events = either_events[either_events["country_id"] == country_id]
        months = pd.date_range(panel_start, end_date, freq="MS")

        for month_end in months:
            for window in PLOT_WINDOWS:
                window_start = month_end - pd.DateOffset(years=window) + pd.DateOffset(days=1)
                if window_start < panel_start:
                    continue
                count = int(
                    (
                        (country_events["event_date"] > window_start)
                        & (country_events["event_date"] <= month_end)
                    ).sum()
                )
                either_rows.append(
                    {
                        "date": month_end,
                        "country_id": country_id,
                        "window_years": window,
                        "annualized_rate": count / window,
                    }
                )

    either_rolling = pd.DataFrame(either_rows)
    return either_rolling.groupby(["date", "window_years"], as_index=False).agg(
        annualized_rate=("annualized_rate", "mean")
    )


def _either_5yr_annual(western_either: pd.DataFrame) -> pd.DataFrame:
    return (
        western_either[western_either["window_years"] == 5]
        .sort_values("date")
        .assign(year=lambda df: df["date"].dt.year)
        .groupby("year", as_index=False)
        .tail(1)[["year", "annualized_rate"]]
        .rename(columns={"annualized_rate": "either_change_rate"})
    )


def plot_either_change(western_either: pd.DataFrame, output_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor(BG)
    _swd_axes(ax)

    lines: list[tuple] = []
    data_end = PLOT_START
    for window in PLOT_WINDOWS:
        style = WINDOW_STYLE[window]
        data = western_either[
            (western_either["window_years"] == window) & (western_either["date"] >= PLOT_START)
        ].sort_values("date")
        (line,) = ax.plot(
            data["date"].dt.year + (data["date"].dt.month - 1) / 12,
            data["annualized_rate"],
            color=style["color"],
            linewidth=style["linewidth"],
            alpha=style["alpha"],
            solid_capstyle="round",
        )
        lines.append((line, style["label"]))
        data_end = max(data_end, data["date"].max())

    ax.text(
        0.0,
        1.08,
        "Either-change rate: leader or coalition turnover, averaged across 20 Western democracies",
        transform=ax.transAxes,
        fontsize=10,
        color=GRAY_MED,
        va="bottom",
        ha="left",
        clip_on=False,
    )
    ax.text(
        0.0,
        1.0,
        "Political turnover troughed in the 2000s, then rose again",
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
        color=TEXT,
        va="bottom",
        ha="left",
        clip_on=False,
    )
    ax.set_ylabel("Changes per year", fontsize=10)
    ax.set_xlabel("Year", fontsize=10)
    ax.set_xlim(PLOT_START.year, data_end.year + 0.5)
    _legend_above_xaxis(ax, lines)
    fig.subplots_adjust(left=0.09, right=0.86, top=0.82, bottom=0.16)

    path = output_dir / "either-change-rate.png"
    fig.savefig(path, dpi=150, facecolor=BG)
    plt.close(fig)
    return path


def plot_instability_vs_growth(western_either: pd.DataFrame, output_dir: Path) -> Path:
    from west_pol_stability.ingest.gdp import annual_gdp_summary, fetch_gdp_per_capita

    gdp_stats = annual_gdp_summary(fetch_gdp_per_capita())
    combined = (
        _either_5yr_annual(western_either)
        .merge(gdp_stats, on="year", how="inner")
        .dropna(subset=["gdp_yoy_pct_5yr"])
        .loc[lambda df: df["year"] >= max(PLOT_START.year, 1960)]
        .sort_values("year")
    )

    fig, ax_instability = plt.subplots(figsize=(12.5, 5.8))
    fig.patch.set_facecolor(BG)
    ax_growth = ax_instability.twinx()
    ax_instability.set_facecolor(BG)
    ax_growth.set_facecolor(BG)

    (line_instability,) = ax_instability.plot(
        combined["year"],
        combined["either_change_rate"],
        color=ACCENT,
        linewidth=2.6,
        solid_capstyle="round",
    )
    (line_growth,) = ax_growth.plot(
        combined["year"],
        combined["gdp_yoy_pct_5yr"],
        color=SECONDARY,
        linewidth=1.8,
        linestyle="--",
        solid_capstyle="round",
    )

    ax_instability.text(
        0.0,
        1.16,
        "GDP growth = cross-country mean of year-on-year % changes, smoothed over 5 years",
        transform=ax_instability.transAxes,
        fontsize=10,
        color=GRAY_MED,
        va="bottom",
        ha="left",
        clip_on=False,
    )
    ax_instability.text(
        0.0,
        1.06,
        "Instability rose after the 2000s while GDP growth trended lower",
        transform=ax_instability.transAxes,
        fontsize=14,
        fontweight="bold",
        color=TEXT,
        va="bottom",
        ha="left",
        clip_on=False,
    )

    ax_instability.set_ylabel("Either-changes per year", color=ACCENT, fontsize=10)
    ax_growth.set_ylabel("GDP growth (%)", color=SECONDARY, fontsize=10)
    ax_instability.set_xlabel("Year", fontsize=10)
    ax_instability.set_xlim(combined["year"].min() - 0.5, combined["year"].max() + 0.5)
    ax_instability.set_ylim(0, combined["either_change_rate"].max() * 1.45 + 0.05)
    growth_pad = max(
        abs(combined["gdp_yoy_pct_5yr"].max() - combined["gdp_yoy_pct_5yr"].min()) * 0.25,
        0.5,
    )
    ax_growth.set_ylim(
        combined["gdp_yoy_pct_5yr"].min() - growth_pad,
        combined["gdp_yoy_pct_5yr"].max() + growth_pad,
    )
    ax_growth.yaxis.set_major_locator(MaxNLocator(4))

    for axis in (ax_instability, ax_growth):
        axis.spines["top"].set_visible(False)
    ax_instability.spines["right"].set_visible(False)
    ax_instability.spines["left"].set_color(ACCENT)
    ax_instability.spines["bottom"].set_color(GRAY_MED)
    ax_growth.spines["right"].set_color(SECONDARY)
    ax_instability.tick_params(axis="y", colors=ACCENT, labelsize=10, length=0, pad=6)
    ax_growth.tick_params(axis="y", colors=SECONDARY, labelsize=10, length=0, pad=6)
    ax_instability.tick_params(axis="x", colors=TEXT, labelsize=10, length=0, pad=6)
    ax_instability.yaxis.grid(True, color=GRAY_LIGHT, linewidth=0.9)
    ax_instability.set_axisbelow(True)

    _legend_above_xaxis(
        ax_instability,
        [
            (line_instability, "Either-change (5-year)"),
            (line_growth, "GDP growth (5-year)"),
        ],
    )
    fig.subplots_adjust(left=0.09, right=0.88, top=0.82, bottom=0.16)

    path = output_dir / "instability-vs-gdp-growth.png"
    fig.savefig(path, dpi=150, facecolor=BG)
    plt.close(fig)
    return path


def plot_instability_vs_stress(western_either: pd.DataFrame, output_dir: Path) -> Path:
    from west_pol_stability.ingest.gdp import annual_gdp_summary, fetch_gdp_per_capita

    gdp_stats = annual_gdp_summary(fetch_gdp_per_capita())
    combined = (
        _either_5yr_annual(western_either)
        .merge(gdp_stats, on="year", how="inner")
        .dropna(subset=["gdp_yoy_pct_5yr"])
        .loc[lambda df: df["year"] >= max(PLOT_START.year, 1960)]
        .sort_values("year")
    )

    growth_baseline = combined["gdp_yoy_pct_5yr"].rolling(10, min_periods=5).mean()
    combined["gdp_growth_stress"] = (growth_baseline - combined["gdp_yoy_pct_5yr"]).clip(lower=0)

    lag_years = 1
    lag_corrs = {
        lag: combined["either_change_rate"].corr(combined["gdp_growth_stress"].shift(lag))
        for lag in range(0, 6)
    }
    best_lag = max(
        lag_corrs,
        key=lambda lag: lag_corrs[lag] if lag_corrs[lag] == lag_corrs[lag] else float("-inf"),
    )
    plot_df = combined.assign(gdp_stress_lagged=combined["gdp_growth_stress"].shift(lag_years)).dropna(
        subset=["gdp_stress_lagged"]
    )

    fig, ax_instability = plt.subplots(figsize=(12.5, 5.8))
    fig.patch.set_facecolor(BG)
    ax_stress = ax_instability.twinx()
    ax_instability.set_facecolor(BG)
    ax_stress.set_facecolor(BG)

    (line_instability,) = ax_instability.plot(
        plot_df["year"],
        plot_df["either_change_rate"],
        color=ACCENT,
        linewidth=2.6,
        solid_capstyle="round",
    )
    (line_stress,) = ax_stress.plot(
        plot_df["year"],
        plot_df["gdp_stress_lagged"],
        color=SECONDARY,
        linewidth=1.8,
        linestyle="--",
        solid_capstyle="round",
    )

    corr_bits = ", ".join(f"lag {lag}: r={lag_corrs[lag]:.2f}" for lag in range(0, 4))
    ax_instability.text(
        0.0,
        1.16,
        f"Correlations (instability vs stress): {corr_bits} – strongest at lag {best_lag}",
        transform=ax_instability.transAxes,
        fontsize=10,
        color=GRAY_MED,
        va="bottom",
        ha="left",
        clip_on=False,
    )
    ax_instability.text(
        0.0,
        1.06,
        "GDP stress peaks often align with later instability",
        transform=ax_instability.transAxes,
        fontsize=14,
        fontweight="bold",
        color=TEXT,
        va="bottom",
        ha="left",
        clip_on=False,
    )

    ax_instability.set_ylabel("Either-changes per year", color=ACCENT, fontsize=10)
    ax_stress.set_ylabel("GDP growth stress (pp)", color=SECONDARY, fontsize=10)
    ax_instability.set_xlabel("Year", fontsize=10)
    ax_instability.set_xlim(plot_df["year"].min() - 0.5, plot_df["year"].max() + 0.5)
    ax_instability.set_ylim(0, plot_df["either_change_rate"].max() * 1.45 + 0.05)
    stress_pad = max(plot_df["gdp_stress_lagged"].max() * 0.25, 0.3)
    ax_stress.set_ylim(0, plot_df["gdp_stress_lagged"].max() + stress_pad)
    ax_stress.yaxis.set_major_locator(MaxNLocator(4))

    for axis in (ax_instability, ax_stress):
        axis.spines["top"].set_visible(False)
    ax_instability.spines["right"].set_visible(False)
    ax_instability.spines["left"].set_color(ACCENT)
    ax_instability.spines["bottom"].set_color(GRAY_MED)
    ax_stress.spines["right"].set_color(SECONDARY)
    ax_instability.tick_params(axis="y", colors=ACCENT, labelsize=10, length=0, pad=6)
    ax_stress.tick_params(axis="y", colors=SECONDARY, labelsize=10, length=0, pad=6)
    ax_instability.tick_params(axis="x", colors=TEXT, labelsize=10, length=0, pad=6)
    ax_instability.yaxis.grid(True, color=GRAY_LIGHT, linewidth=0.9)
    ax_instability.set_axisbelow(True)

    _legend_above_xaxis(
        ax_instability,
        [
            (line_instability, "Either-change (5-year)"),
            (line_stress, f"GDP growth stress ({lag_years}yr lead)"),
        ],
    )
    fig.subplots_adjust(left=0.09, right=0.88, top=0.82, bottom=0.16)

    path = output_dir / "instability-vs-gdp-stress.png"
    fig.savefig(path, dpi=150, facecolor=BG)
    plt.close(fig)
    return path


def main() -> None:
    _style_matplotlib()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    western_either = _load_western_either()
    paths = [
        plot_either_change(western_either, OUTPUT_DIR),
        plot_instability_vs_growth(western_either, OUTPUT_DIR),
        plot_instability_vs_stress(western_either, OUTPUT_DIR),
    ]
    for path in paths:
        print(f"Saved {path}")


if __name__ == "__main__":
    main()
