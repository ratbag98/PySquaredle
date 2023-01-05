"""
Canvas class, provides surface for drawing solution lines

Inspired by https://gist.github.com/zhanglongqi/78d7b5cd24f7d0c42f5d116d967923e7
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPaintEvent, QPalette, QPen
from PyQt6.QtWidgets import QWidget


class Overlay(QWidget):
    """
    Provide a surface for drawing lines over the Puzzle.

    We're a transparent widget, created by the LetterGridWidget.
    """

    LINE_WIDTH = 12

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

    def __init__(self, parent=None) -> None:
        super(Overlay, self).__init__(parent)

        palette = QPalette(self.palette())
        palette.setColor(palette.ColorRole.Base, Qt.GlobalColor.transparent)

        self._paths: list[list[tuple[int, int]]] = []
        self.colours: list[QColor] = []

        for col in self.COLOUR_PALETTE:
            colour = QColor(*[int(c * 255) for c in col])
            colour.setAlpha(96)
            self.colours.append(colour)

    def set_paths(self, paths: list[list[tuple[int, int]]]):
        """
        Set the drawing paths, one or more lists of coordinates.

        We'll loop through the lists, selecting a new colour and drawing the
        relevant lines.
        """
        self._paths = paths
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Paint the lines
        """
        qp = QPainter(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)

        for index, path in enumerate(self._paths):
            pen = QPen(self.colours[index % len(self.colours)])
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen.setWidth(self.LINE_WIDTH)
            qp.setPen(pen)

            # TODO draw a circle at start of line
            # make lines more visible by offsetting successive lines by half
            offset = index * self.LINE_WIDTH // 2
            for i in range(len(path) - 1):
                qp.drawLine(
                    path[i][0] + offset,
                    path[i][1] + offset,
                    path[i + 1][0] + offset,
                    path[i + 1][1] + offset,
                )
            # TODO draw a line across the end of the line
