"""Website-matched matplotlib defaults for michaelgv.uk.

    from plots.mgv_style import apply, COLOURS
    apply()
"""

from pathlib import Path

import matplotlib as mpl
from matplotlib import font_manager

COLOURS = {
    "paper": "#FFF1E0",
    "ink": "#585858",
    "dark": "#5E6D8F",
    "accent_light": "#A9978E",
    "accent": "#BA7781",
    "light": "#F0F1F3",
}

_FONT_FILES = (
    "/usr/share/fonts/cormorant-garamond/CormorantGaramond-Regular.ttf",
    "/usr/share/fonts/cormorant-garamond/CormorantGaramond-Medium.ttf",
    "/usr/share/fonts/cormorant-garamond/CormorantGaramond-SemiBold.ttf",
    "/usr/share/fonts/cormorant-garamond/CormorantGaramond-Italic.ttf",
    "/usr/share/fonts/eb-garamond/EBGaramond[wght].ttf",
    "/usr/share/fonts/eb-garamond/EBGaramond-Italic[wght].ttf",
)

_APPLIED = False


def apply():
    """Register site fonts and load plots/mgv.mplstyle."""
    global _APPLIED
    for path in _FONT_FILES:
        if Path(path).exists():
            font_manager.fontManager.addfont(path)

    style = Path(__file__).with_name("mgv.mplstyle")
    mpl.style.use(style)

    families = [
        "Cormorant Garamond",
        "EB Garamond",
        "Garamond",
        "Liberation Serif",
        "serif",
    ]
    mpl.rcParams["font.family"] = "serif"
    mpl.rcParams["font.serif"] = families
    _APPLIED = True
    return COLOURS
