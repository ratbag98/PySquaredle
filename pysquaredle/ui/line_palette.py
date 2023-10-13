"""Manage color palettes for the lines drawn over the grid."""

from collections.abc import Iterator

from PyQt6.QtGui import QColor


class LinePalette:
    """Manage color palettes for the lines drawn over the grid."""

    # palette of pleasant colours from seaborn
    # https://seaborn.pydata.org/tutorial/color_palettes.html
    COLOUR_PALETTE = [
        (0.12156862745098039, 0.4666666666666667, 0.7058823529411765),
        (1.0, 0.4980392156862745, 0.054901960784313725),
        (0.17254901960784313, 0.6274509803921569, 0.17254901960784313),
        (0.8392156862745098, 0.15294117647058825, 0.1568627450980392),
        (0.5803921568627451, 0.403921568627451, 0.7411764705882353),
        (0.5490196078431373, 0.33725490196078434, 0.29411764705882354),
        (0.8901960784313725, 0.4666666666666667, 0.7607843137254902),
        (0.4980392156862745, 0.4980392156862745, 0.4980392156862745),
        (0.7372549019607844, 0.7411764705882353, 0.13333333333333333),
        (0.09019607843137255, 0.7450980392156863, 0.8117647058823529),
    ]
    ALPHA = 0.5

    def __init__(self) -> None:
        self._palette: list[QColor] = []

        for col in self.COLOUR_PALETTE:
            colour = QColor(*[int(c * 255) for c in col])
            colour.setAlpha(int(self.ALPHA * 255))
            self._palette.append(colour)

        self._index = 0

    def next(self) -> QColor:
        """Return the next color in the palette."""
        color = self._palette[self._index]
        self._index = (self._index + 1) % len(self)
        return color

    def reset(self) -> None:
        """Reset the palette index to the beginning."""
        self._index = 0

    def __len__(self) -> int:
        """Return the number of colors in the palette."""
        return len(self._palette)

    def __getitem__(self, index: int) -> QColor:
        """Return the color at the given index."""
        return self._palette[index]

    def __setitem__(self, index: int, color: QColor) -> None:
        """Set the color at the given index."""
        self._palette[index] = color

    def __iter__(self) -> Iterator[QColor]:
        """Iterate over the colors in the palette."""
        return iter(self._palette)

    def __contains__(self, color: QColor) -> bool:
        """Return True if the palette contains the given color."""
        return color in self._palette

    def __repr__(self) -> str:
        """Return a string representation of the palette."""
        return f"LinePalette({self._palette})"
