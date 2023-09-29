""" Canvas class, provides surface for drawing solution lines

Inspired by https://gist.github.com/zhanglongqi/78d7b5cd24f7d0c42f5d116d967923e7
"""

from PyQt6.QtCore import QLine, QPoint, Qt
from PyQt6.QtGui import QBrush, QColor, QPainter, QPaintEvent, QPalette, QPen
from PyQt6.QtWidgets import QWidget

from pysquaredle.ui.line_palette import LinePalette
from pysquaredle.vector import Vector


def _build_line_segments(path: list[tuple[int, int]], offset: int) -> list[QLine]:
    return [
        QLine(
            path[i][0] + offset,
            path[i][1] + offset,
            path[i + 1][0] + offset,
            path[i + 1][1] + offset,
        )
        for i in range(len(path) - 1)
    ]


class Overlay(QWidget):
    """Provide a surface for drawing lines over the Puzzle.

    We're a transparent widget, created by the LetterGridWidget.
    """

    LINE_WIDTH = 12
    CIRCLE_RADIUS = LINE_WIDTH + 4

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        # we're transparent
        palette = QPalette(self.palette())
        palette.setColor(palette.ColorRole.Base, Qt.GlobalColor.transparent)

        # we're used to draw one or more "paths" representing the solution(s) for
        # a given word.
        self._selected_paths: list[list[tuple[int, int]]] = []

        # for multiple lines we use a palette to cycle through colours
        self.line_palette: LinePalette = LinePalette()

    def set_paths(self, paths: list[list[tuple[int, int]]]) -> None:
        """Set the drawing paths, one or more lists of coordinates.

        We'll loop through the lists, selecting a new colour and drawing the
        relevant lines.
        """
        self._selected_paths = paths
        self.update()

    def paintEvent(self, a0: QPaintEvent) -> None:
        """Paint the lines"""

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.line_palette.reset()

        pen = QPen()
        pen.setWidth(self.LINE_WIDTH)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        for index, path in enumerate(self._selected_paths):
            # make lines more visible by offsetting successive lines
            offset = index * self.LINE_WIDTH

            color = self.line_palette.next()

            pen.setColor(color)
            painter.setPen(pen)

            line_segments = _build_line_segments(path, offset)
            painter.drawLines(line_segments)  # type: ignore

            # draw a line across the end of the last line segment
            self._draw_end_bar(painter, path, offset)

            # draw a filled circle centered on the first letter
            self._draw_start_circle(painter, path, offset, color)

    def _draw_start_circle(
        self,
        painter: QPainter,
        path: list[tuple[int, int]],
        offset: int,
        color: QColor,
    ) -> None:
        # save the current pen
        pen = painter.pen()

        brush = QBrush(color)
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        painter.setBrush(brush)
        ellipse_pen = QPen()
        ellipse_pen.setStyle(Qt.PenStyle.NoPen)

        painter.setPen(ellipse_pen)

        painter.drawEllipse(
            QPoint(path[0][0] + offset, path[0][1] + offset),
            self.CIRCLE_RADIUS,
            self.CIRCLE_RADIUS,
        )

        # restore the pen
        painter.setPen(pen)

    def _draw_end_bar(
        self, painter: QPainter, path: list[tuple[int, int]], offset: int
    ) -> None:
        scaled_end_bar: Vector = self._calculate_end_bar_vector(
            path[-1][0] - path[-2][0], path[-1][1] - path[-2][1]
        )

        painter.drawLine(
            path[-1][0] + offset - int(scaled_end_bar.x),
            path[-1][1] + offset - int(scaled_end_bar.y),
            path[-1][0] + offset + int(scaled_end_bar.x),
            path[-1][1] + offset + int(scaled_end_bar.y),
        )

    def _calculate_end_bar_vector(self, x: int, y: int) -> Vector:
        """Calculate a vector to draw a line across the end of a line.
        x and y are the vector components for the last two points in the path.
        """
        vec = Vector(x, y)

        return vec.rotate_90().normalize() * self.LINE_WIDTH * 2
