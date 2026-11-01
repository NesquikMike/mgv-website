"""Generate image-pipeline charts for the twapp post."""

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
POS = "#5E6D8F"
NEG = "#BA7781"

FIG_W = 6.8
DPI = 200
TITLE_SIZE = 22
SUBTITLE_SIZE = 15
LABEL_SIZE = 14
TICK_SIZE = 13
ANNOT_SIZE = 12


def _style() -> None:
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


def _headlines(fig: plt.Figure, title: str, subtitle: str) -> None:
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


def taste_chart() -> Path:
    # Hand-reviewed first drafts only (owner taste labels on originals)
    labels = [
        "Funny",
        "Funny-ish",
        "Meh",
        "Kill\n(not funny)",
        "Flux miss\n(wrong render)",
        "Desc miss",
    ]
    values = [13, 7, 5, 26, 7, 2]
    colors = [POS, POS, GRAY_MED, NEG, NEG, GRAY_MED]

    fig, ax = plt.subplots(figsize=(FIG_W, 3.8), dpi=DPI, facecolor=BG)
    _headlines(
        fig,
        "First-draft taste labels",
        "60 hand-reviewed originals · owner only · selective sample",
    )
    fig.subplots_adjust(left=0.08, right=0.98, top=0.78, bottom=0.18)
    _swd_axes(ax)
    ax.spines["left"].set_visible(False)

    x = np.arange(len(labels))
    ax.bar(x, values, color=colors, width=0.72)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylim(0, 30)
    ax.yaxis.grid(True, color=GRAY_LIGHT, linewidth=0.9)
    ax.xaxis.grid(False)

    for xi, v in zip(x, values):
        ax.text(xi, v + 0.6, str(v), ha="center", va="bottom", fontsize=ANNOT_SIZE, color=TEXT)

    out = OUTPUT_DIR / "image-taste-originals.png"
    fig.savefig(out, dpi=DPI, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return out


def refine_decision_chart() -> Path:
    labels = ["Keep new", "Keep refining", "Keep original"]
    values = [53, 64, 3]
    colors = [POS, ACCENT, GRAY_MED]

    fig, ax = plt.subplots(figsize=(FIG_W, 3.4), dpi=DPI, facecolor=BG)
    _headlines(
        fig,
        "What happened after a tweak",
        "120 decided refine results · 53% still needed another pass",
    )
    fig.subplots_adjust(left=0.22, right=0.88, top=0.78, bottom=0.14)
    _swd_axes(ax)
    ax.spines["left"].set_visible(False)

    y = np.arange(len(labels))[::-1]
    ax.barh(y, values, color=colors, height=0.55)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=LABEL_SIZE)
    ax.set_xlim(0, 75)

    for yi, v in zip(y, values):
        ax.text(v + 1.5, yi, str(v), va="center", fontsize=ANNOT_SIZE, color=TEXT)

    out = OUTPUT_DIR / "image-refine-decisions.png"
    fig.savefig(out, dpi=DPI, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return out


def tweak_bucket_chart() -> Path:
    labels = [
        "Keep everything else the same",
        "Facial expression / emotion",
        "Physics / anatomy / spatial",
        "Character / outfit / casting",
        "Remove an unwanted element",
        "Make it sexier",
        "Make the gag clearer",
        "Add crowd / witnesses",
        "Wrong setting",
        "Make it funnier (explicit)",
    ]
    values = [45, 44, 44, 42, 40, 36, 28, 20, 17, 3]
    n = 196
    pcts = [100 * v / n for v in values]

    fig, ax = plt.subplots(figsize=(FIG_W, 5.0), dpi=DPI, facecolor=BG)
    _headlines(
        fig,
        "What the tweak instructions asked for",
        f"Keyword buckets over {n} refine jobs · multi-label, so bars overlap",
    )
    fig.subplots_adjust(left=0.42, right=0.88, top=0.82, bottom=0.08)
    _swd_axes(ax)
    ax.spines["left"].set_visible(False)

    y = np.arange(len(labels))[::-1]
    colors = [ACCENT] + [SECONDARY] * 8 + [GRAY_MED]
    ax.barh(y, values, color=colors, height=0.62)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=11)
    ax.set_xlim(0, 55)

    for yi, v, p in zip(y, values, pcts):
        ax.text(v + 0.8, yi, f"{v} ({p:.0f}%)", va="center", fontsize=10, color=TEXT)

    out = OUTPUT_DIR / "image-tweak-buckets.png"
    fig.savefig(out, dpi=DPI, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return out


def keep_else_chart() -> Path:
    # Among 45 keep-else jobs: 16 got a further refine (failure of one-pass)
    labels = [
        "Accepted\n(keep new)",
        "Needed another\ntweak",
        "Reverted to\noriginal",
        "No decision\nrecorded",
    ]
    values = [18, 10, 2, 15]
    colors = [POS, ACCENT, GRAY_MED, GRAY_LIGHT]

    fig, ax = plt.subplots(figsize=(FIG_W, 3.6), dpi=DPI, facecolor=BG)
    _headlines(
        fig,
        "“Don’t change anything else” outcomes",
        "45 refine jobs that asked to freeze the rest of the image",
    )
    fig.subplots_adjust(left=0.08, right=0.98, top=0.78, bottom=0.16)
    _swd_axes(ax)
    ax.spines["left"].set_visible(False)

    x = np.arange(len(labels))
    ax.bar(x, values, color=colors, width=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylim(0, 22)
    ax.yaxis.grid(True, color=GRAY_LIGHT, linewidth=0.9)
    ax.xaxis.grid(False)

    for xi, v in zip(x, values):
        ax.text(xi, v + 0.4, str(v), ha="center", va="bottom", fontsize=ANNOT_SIZE, color=TEXT)

    out = OUTPUT_DIR / "image-keep-else-outcomes.png"
    fig.savefig(out, dpi=DPI, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return out


def main() -> None:
    _style()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for fn in (taste_chart, refine_decision_chart, tweak_bucket_chart, keep_else_chart):
        print(fn())


if __name__ == "__main__":
    main()
