"""
Canvas class, provides surface for drawing solution lines

Inspired by https://gist.github.com/zhanglongqi/78d7b5cd24f7d0c42f5d116d967923e7
"""

from PyQt6.QtCore import QLine, Qt
from PyQt6.QtGui import QBrush, QColor, QPainter, QPaintEvent, QPalette, QPen
from PyQt6.QtWidgets import QWidget


class Overlay(QWidget):
    """
    Provide a surface for drawing lines over the Puzzle.

    We're a transparent widget, created by the LetterGridWidget.
    """

    LINE_WIDTH = 12
    CIRCLE_RADIUS = LINE_WIDTH + 4
    ALPHA = 0.5

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

    def __init__(self, parent: QWidget) -> None:
        super(Overlay, self).__init__(parent)

        palette = QPalette(self.palette())
        palette.setColor(palette.ColorRole.Base, Qt.GlobalColor.transparent)

        self._paths: list[list[tuple[int, int]]] = []
        self.colours: list[QColor] = []

        for col in self.COLOUR_PALETTE:
            colour = QColor(*[int(c * 255) for c in col])
            colour.setAlpha(int(self.ALPHA * 255))
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
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for index, path in enumerate(self._paths):
            pen = QPen(self.colours[index % len(self.colours)])
            pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen.setWidth(self.LINE_WIDTH)
            painter.setPen(pen)

            # make lines more visible by offsetting successive lines by half
            offset = 4 * self.LINE_WIDTH // 2

            # TODO look at using QDrawLines instead - this might join more neatly

            for i in range(len(path) - 1):
                painter.drawLine(
                    path[i][0] + offset,
                    path[i][1] + offset,
                    path[i + 1][0] + offset,
                    path[i + 1][1] + offset,
                )

            # draw a line across the end of the last line segment
            scaled_end_bar: tuple[int, int] = self._calculate_end_bar_vector(
                path[-1][0] - path[-2][0], path[-1][1] - path[-2][1]
            )

            pen.setCapStyle(Qt.PenCapStyle.SquareCap)
            painter.setPen(pen)

            painter.drawLine(
                path[-1][0] + offset - scaled_end_bar[0],
                path[-1][1] + offset - scaled_end_bar[1],
                path[-1][0] + offset + scaled_end_bar[0],
                path[-1][1] + offset + scaled_end_bar[1],
            )

            brush = QBrush(self.colours[index % len(self.colours)])
            brush.setStyle(Qt.BrushStyle.SolidPattern)
            painter.setBrush(brush)
            pen.setStyle(Qt.PenStyle.NoPen)
            painter.setPen(pen)

            # draw a filled circle centered on the first point
            painter.drawEllipse(
                path[0][0] + offset - self.CIRCLE_RADIUS,
                path[0][1] + offset - self.CIRCLE_RADIUS,
                self.CIRCLE_RADIUS * 2,
                self.CIRCLE_RADIUS * 2,
            )

    def _calculate_end_bar_vector(self, x: int, y: int) -> tuple[int, int]:
        """
        Calculate a vector to draw a line across the end of a line.
        x and y are the vector components for the last two points in the path.
        """

        end_bar_vector = self._rotate(x, y)
        normalized = self._normalize(*end_bar_vector)
        scaled = self._scale(*normalized, self.LINE_WIDTH * 2)
        return scaled

    # rotate a vector by 90 degrees
    def _rotate(self, x: int, y: int) -> tuple[int, int]:
        return y, -x

    # normalize a vector
    def _normalize(self, x: int, y: int) -> tuple[float, float]:
        length = (x**2 + y**2) ** 0.5
        return x / length, y / length

    # multiply vector by a scalar
    def _scale(self, x: float, y: float, scale: float) -> tuple[int, int]:
        return int(x * scale), int(y * scale)
