"""OptiSplit project thumb: A/B uptick chart in the OptiSplit brand."""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm
from matplotlib import patheffects as pe
from matplotlib.patches import FancyBboxPatch

OUT = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "images"
    / "projects"
    / "optisplit.jpg"
)

# From optisplit/web/assets/css/styles.css
C = {
    "ink": "#17211c",
    "ink_soft": "#3f4d46",
    "paper": "#f3eee4",
    "white": "#fcfaf6",
    "green": "#1d6a48",
    "coral": "#c24d34",
    "line": "#d6ccba",
}

FRAUNCES = str(
    next(
        p
        for p in Path("/usr/share/fonts/fraunces").iterdir()
        if p.suffix.lower() == ".ttf" and "Italic" not in p.name
    )
)
SANS = {
    "regular": "/usr/share/fonts/adobe-source-sans/SourceSans3-Regular.otf",
    "semibold": "/usr/share/fonts/adobe-source-sans/SourceSans3-Semibold.otf",
    "bold": "/usr/share/fonts/adobe-source-sans/SourceSans3-Bold.otf",
}


def serif(size, weight=600):
    return fm.FontProperties(fname=FRAUNCES, size=size, weight=weight)


def sans(size, weight="regular"):
    return fm.FontProperties(fname=SANS[weight], size=size)


def _brand():
    mpl.rcdefaults()
    for path in (FRAUNCES, *SANS.values()):
        if Path(path).exists():
            fm.fontManager.addfont(path)
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Source Sans 3", "Source Sans Pro", "sans-serif"],
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.8,
            "axes.grid": False,
            "xtick.major.size": 0,
            "ytick.major.size": 0,
            "text.color": C["ink"],
            "axes.labelcolor": C["ink_soft"],
            "xtick.color": C["ink_soft"],
            "ytick.color": C["ink_soft"],
        }
    )


def main():
    _brand()
    days = np.arange(1, 15)
    # Land on the live-example numbers from the OptiSplit homepage.
    control = 16.2 + np.linspace(0, 1.8, len(days))
    variant = 16.2 + np.array(
        [0, 0.4, 1.1, 2.2, 3.6, 5.2, 6.6, 8.0, 9.3, 10.5, 11.6, 12.6, 13.6, 14.8]
    )

    fig, ax = plt.subplots(figsize=(4.5, 8.0))
    fig.patch.set_facecolor(C["paper"])
    ax.set_facecolor(C["white"])
    fig.subplots_adjust(top=0.74, left=0.22, right=0.90, bottom=0.18)

    card = FancyBboxPatch(
        (0.07, 0.05),
        0.86,
        0.90,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        transform=fig.transFigure,
        facecolor=C["white"],
        edgecolor=C["line"],
        linewidth=1.2,
        zorder=-1,
        clip_on=False,
    )
    fig.add_artist(card)

    ax.plot(days, control, color=C["coral"], linewidth=2.4, solid_capstyle="round")
    ax.plot(days, variant, color=C["green"], linewidth=2.8, solid_capstyle="round")
    ax.scatter([days[-1]], [control[-1]], color=C["coral"], s=36, zorder=3)
    ax.scatter([days[-1]], [variant[-1]], color=C["green"], s=48, zorder=3)

    halo = [pe.withStroke(linewidth=4, foreground=C["white"])]
    ax.annotate(
        "15% off",
        xy=(days[-1], variant[-1]),
        xytext=(-6, 10),
        textcoords="offset points",
        ha="right",
        color=C["green"],
        fontproperties=sans(12, "semibold"),
        path_effects=halo,
    )
    ax.annotate(
        "31% redeemed",
        xy=(days[-1], variant[-1]),
        xytext=(-6, -4),
        textcoords="offset points",
        ha="right",
        va="top",
        color=C["ink"],
        fontproperties=sans(9),
        path_effects=halo,
    )
    ax.annotate(
        "10% off",
        xy=(days[-1], control[-1]),
        xytext=(-6, -12),
        textcoords="offset points",
        ha="right",
        color=C["coral"],
        fontproperties=sans(12, "semibold"),
        path_effects=halo,
    )

    ax.set_xlim(0.5, 14.8)
    ax.set_ylim(14, 36)
    ax.set_xticks([1, 7, 14])
    ax.set_xticklabels(["Day 1", "Week 1", "Week 2"], fontproperties=sans(9.5))
    ax.set_yticks([18, 24, 31])
    ax.set_yticklabels(["18%", "24%", "31%"], fontproperties=sans(9.5))
    ax.set_ylabel("Redemption rate", fontproperties=sans(10), color=C["ink_soft"])
    ax.yaxis.set_label_coords(-0.16, 0.5)
    ax.spines["left"].set_color(C["line"])
    ax.spines["bottom"].set_color(C["line"])

    fig.text(
        0.14,
        0.905,
        "LIVE EXAMPLE",
        fontproperties=sans(8, "bold"),
        color=C["green"],
        ha="left",
        va="bottom",
    )
    fig.text(
        0.14,
        0.795,
        "The 15% pastry offer\npulled away.",
        fontproperties=serif(15.5),
        color=C["ink"],
        ha="left",
        va="bottom",
        linespacing=1.12,
    )

    logo = serif(13)
    t_opti = fig.text(
        0.14,
        0.105,
        "Opti",
        fontproperties=logo,
        color=C["ink"],
        ha="left",
        va="center",
    )
    fig.canvas.draw()
    opti_w = t_opti.get_window_extent().transformed(fig.transFigure.inverted()).width
    fig.text(
        0.14 + opti_w,
        0.105,
        "Split",
        fontproperties=logo,
        color=C["green"],
        ha="left",
        va="center",
    )
    fig.text(
        0.14,
        0.068,
        "Bloom & Co Café · two weekends",
        fontproperties=sans(8.5),
        color=C["ink_soft"],
        ha="left",
        va="center",
    )

    fig.savefig(OUT, dpi=160, format="jpeg", pil_kwargs={"quality": 88})
    print(OUT)


if __name__ == "__main__":
    main()
