"""Generate Reddit funnel charts for the twapp build/distribution post."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUTPUT_DIR = (
    Path(__file__).resolve().parents[1]
    / "assets/images/posts/building-twapp-was-easy"
)

BG = "#FFF1E0"
TEXT = "#585858"
ACCENT = "#BA7781"
SECONDARY = "#5E6D8F"
GRAY_MED = "#A9978E"
GRAY_LIGHT = "#E8DDD0"

FIG_W = 6.8
DPI = 200
TITLE_SIZE = 22
SUBTITLE_SIZE = 15
LABEL_SIZE = 14
TICK_SIZE = 13
ANNOT_SIZE = 12


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
    ax.tick_params(axis="both", colors=TEXT, labelsize=TICK_SIZE, length=0, pad=4)
    ax.xaxis.grid(True, color=GRAY_LIGHT, linewidth=0.9)
    ax.set_axisbelow(True)


def _blog_headlines(fig: plt.Figure, title: str, subtitle: str) -> None:
    fig.text(
        0.0,
        1.0,
        title,
        fontsize=TITLE_SIZE,
        fontweight="bold",
        color=TEXT,
        ha="left",
        va="top",
        transform=fig.transFigure,
    )
    fig.text(
        0.0,
        0.90,
        subtitle,
        fontsize=SUBTITLE_SIZE,
        color=GRAY_MED,
        ha="left",
        va="top",
        transform=fig.transFigure,
    )


def funnel_chart() -> Path:
    labels = [
        "Impressions",
        "Clicks",
        "Sessions",
        "Puzzle starts",
        "Completes",
        "Signups",
        "League joins",
    ]
    values = [206722, 1166, 1020, 60, 27, 5, 4]
    # Highlight the cliff after landing
    colors = [
        GRAY_MED,
        GRAY_MED,
        SECONDARY,
        ACCENT,
        ACCENT,
        ACCENT,
        ACCENT,
    ]

    fig, ax = plt.subplots(figsize=(FIG_W, 4.2), dpi=DPI, facecolor=BG)
    _blog_headlines(
        fig,
        "Reddit ads funnel",
        "Visitor-only, 25–29 Oct 2026, before Popbitch",
    )
    fig.subplots_adjust(left=0.22, right=0.86, top=0.82, bottom=0.12)
    _swd_axes(ax)

    y = np.arange(len(labels))[::-1]
    ax.barh(y, values, color=colors, height=0.62)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=LABEL_SIZE)
    ax.set_xscale("log")
    ax.set_xlim(1, 400000)
    ax.set_xlabel("")
    ax.spines["left"].set_visible(False)

    for yi, v in zip(y, values):
        ax.text(
            v * 1.12,
            yi,
            f"{v:,}",
            va="center",
            ha="left",
            fontsize=ANNOT_SIZE,
            color=TEXT,
        )

    out = OUTPUT_DIR / "reddit-funnel.png"
    fig.savefig(out, dpi=DPI, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return out


def cost_chart() -> Path:
    labels = [
        "Click",
        "Landed session",
        "Puzzle start",
        "Completed puzzle",
        "Verified signup",
        "League join",
    ]
    values = [0.86, 0.98, 16.68, 37.06, 200.11, 250.13]

    fig, ax = plt.subplots(figsize=(FIG_W, 4.0), dpi=DPI, facecolor=BG)
    _blog_headlines(
        fig,
        "Cost per outcome",
        "£1,000.53 spent · visitor-only funnel",
    )
    fig.subplots_adjust(left=0.24, right=0.88, top=0.82, bottom=0.12)
    _swd_axes(ax)

    y = np.arange(len(labels))[::-1]
    colors = [GRAY_MED, SECONDARY, ACCENT, ACCENT, ACCENT, ACCENT]
    ax.barh(y, values, color=colors, height=0.62)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=LABEL_SIZE)
    ax.set_xlim(0, 280)
    ax.spines["left"].set_visible(False)

    for yi, v in zip(y, values):
        label = f"£{v:.2f}" if v < 10 else f"£{v:.0f}"
        ax.text(
            v + 4,
            yi,
            label,
            va="center",
            ha="left",
            fontsize=ANNOT_SIZE,
            color=TEXT,
        )

    out = OUTPUT_DIR / "reddit-cost-per-outcome.png"
    fig.savefig(out, dpi=DPI, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return out


def main() -> None:
    _style_matplotlib()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(funnel_chart())
    print(cost_chart())


if __name__ == "__main__":
    main()
