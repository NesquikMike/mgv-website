"""Trade-off between speed of adoption and speed of active use."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects as pe

from mgv_style import COLOURS, apply

OUT_DIR = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "images"
    / "posts"
    / "thinking-is-slow-copying-is-fast"
)


def _halo():
    return [pe.withStroke(linewidth=4.5, foreground=COLOURS["paper"])]


def main():
    apply()
    c = COLOURS

    # Essay positions, not measured data.
    kinds = [
        dict(
            x=0.10,
            y=0.93,
            label="Genes",
            note="slowest to evolve,\nfastest to use",
            color=c["accent_light"],
            dx=11,
            dy=12,
            ha="left",
            emphasis=False,
        ),
        dict(
            x=0.34,
            y=0.81,
            label="Pavlovian",
            note="learnt in a lifetime,\nstill fast to use",
            color=c["dark"],
            dx=11,
            dy=14,
            ha="left",
            emphasis=False,
        ),
        dict(
            x=0.58,
            y=0.74,
            label="Copying",
            note="fairly quick to learn,\nstill quick to use",
            color=c["accent"],
            dx=10,
            dy=16,
            ha="left",
            emphasis=True,
        ),
        dict(
            x=0.90,
            y=0.18,
            label="Thinking",
            note="invented on first meeting,\nslow to perform",
            color=c["dark"],
            dx=-14,
            dy=20,
            ha="right",
            emphasis=False,
        ),
    ]

    xs = np.array([k["x"] for k in kinds])
    ys = np.array([k["y"] for k in kinds])
    coef = np.polyfit(xs, ys, 3)
    curve_x = np.linspace(xs.min(), xs.max(), 400)
    curve_y = np.clip(np.polyval(coef, curve_x), 0, 1)

    fig, ax = plt.subplots(figsize=(7.2, 4.9))
    fig.subplots_adjust(top=0.80, left=0.14, right=0.98, bottom=0.16)

    ax.plot(
        curve_x,
        curve_y,
        color=c["accent_light"],
        linewidth=1.7,
        solid_capstyle="round",
        zorder=1,
    )

    for k in kinds:
        ax.scatter(
            [k["x"]],
            [k["y"]],
            s=96 if k["emphasis"] else 58,
            color=k["color"],
            zorder=3,
            linewidths=0,
        )
        ax.annotate(
            k["label"],
            xy=(k["x"], k["y"]),
            xytext=(k["dx"], k["dy"]),
            textcoords="offset points",
            ha=k["ha"],
            va="bottom",
            color=k["color"],
            fontsize=14 if k["emphasis"] else 12.5,
            path_effects=_halo(),
        )
        ax.annotate(
            k["note"],
            xy=(k["x"], k["y"]),
            xytext=(k["dx"], k["dy"] - 15),
            textcoords="offset points",
            ha=k["ha"],
            va="top",
            color=c["ink"],
            fontsize=9.5,
            linespacing=1.25,
            path_effects=_halo(),
        )

    ax.set_xlim(-0.02, 1.04)
    ax.set_ylim(-0.04, 1.08)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("Speed of adoption")
    ax.set_ylabel("Speed of active use")

    ax.text(0.02, -0.07, "Slow", ha="left", va="top", color=c["ink"], fontsize=10)
    ax.text(0.98, -0.07, "Fast", ha="right", va="top", color=c["ink"], fontsize=10)
    ax.text(
        -0.07,
        0.02,
        "Slow",
        ha="right",
        va="bottom",
        color=c["ink"],
        fontsize=10,
        rotation=90,
    )
    ax.text(
        -0.07,
        0.98,
        "Fast",
        ha="right",
        va="top",
        color=c["ink"],
        fontsize=10,
        rotation=90,
    )

    # Takeaway title, left-aligned, with the exception in the accent colour.
    title_y = 1.10
    ax.text(
        0.0,
        title_y,
        "Fast to use usually means slow to learn — ",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        color=c["ink"],
        fontsize=15,
        clip_on=False,
    )
    # Width of the first run, then the punchline.
    first = ax.text(
        0.0,
        title_y,
        "Fast to use usually means slow to learn — ",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        color=c["ink"],
        fontsize=15,
        alpha=0,
        clip_on=False,
    )
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bbox = first.get_window_extent(renderer=renderer)
    inv = ax.transAxes.inverted()
    punch_x = inv.transform((bbox.x1, bbox.y0))[0]
    ax.text(
        punch_x,
        title_y,
        "except when we copy.",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        color=c["accent"],
        fontsize=15,
        clip_on=False,
    )

    ax.spines["left"].set_position(("data", 0))
    ax.spines["bottom"].set_position(("data", 0))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    png = OUT_DIR / "learning-tradeoff.png"
    svg = OUT_DIR / "learning-tradeoff.svg"
    fig.savefig(png)
    fig.savefig(svg)
    print(png)


if __name__ == "__main__":
    main()
