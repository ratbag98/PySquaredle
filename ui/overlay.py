"""
Canvas class, provides surface for drawing solution lines

Inspired by https://gist.github.com/zhanglongqi/78d7b5cd24f7d0c42f5d116d967923e7
"""

from PyQt6.QtCore import QLine, Qt
from PyQt6.QtGui import QBrush, QPainter, QPaintEvent, QPalette, QPen
from PyQt6.QtWidgets import QWidget

from ui.line_palette import LinePalette


class Overlay(QWidget):
    """
    Provide a surface for drawing lines over the Puzzle.

    We're a transparent widget, created by the LetterGridWidget.
    """

    LINE_WIDTH = 12
    CIRCLE_RADIUS = LINE_WIDTH + 4

    def __init__(self, parent: QWidget, rainbow: bool = False) -> None:
        super().__init__(parent)

        # we're transparent
        palette = QPalette(self.palette())
        palette.setColor(palette.ColorRole.Base, Qt.GlobalColor.transparent)

        # we're used to draw one or more "paths" representing the solution(s) for
        # a given word.
        self._paths: list[list[tuple[int, int]]] = []

        # for multiple lines we use a palette to cycle through colours
        self.line_palette: LinePalette = LinePalette()

        # if this is true, don't reset the LinePalette when the word changes
        self.rainbow = rainbow

    def set_paths(self, paths: list[list[tuple[int, int]]]):
        """
        Set the drawing paths, one or more lists of coordinates.

        We'll loop through the lists, selecting a new colour and drawing the
        relevant lines.
        """
        self._paths = paths
        if not self.rainbow:
            self.line_palette.reset()
        self.update()

    def paintEvent(self, _event: QPaintEvent) -> None:
        """
        Paint the lines
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for index, path in enumerate(self._paths):
            color = self.line_palette.next()
            pen = QPen(color)
            pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen.setWidth(self.LINE_WIDTH)
            painter.setPen(pen)

            # make lines more visible by offsetting successive lines by half
            offset = index * self.LINE_WIDTH

            line_segments: list[QLine] = [
                QLine(
                    path[i][0] + offset,
                    path[i][1] + offset,
                    path[i + 1][0] + offset,
                    path[i + 1][1] + offset,
                )
                for i in range(len(path) - 1)
            ]

            painter.drawLines(line_segments)

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

            brush = QBrush(color)
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
