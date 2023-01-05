"""
Canvas class, provides surface for drawing solution lines

Inspired by https://gist.github.com/zhanglongqi/78d7b5cd24f7d0c42f5d116d967923e7
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPaintEvent, QPalette, QPen
from PyQt6.QtWidgets import QWidget


class Canvas(QWidget):
    """
    Provide a surface for drawing lines over the Puzzle.

    We're a transparent widget, created by the LetterGridWidget.
    """

    LINE_WIDTH = 12

    def __init__(self, parent=None) -> None:
        super(Canvas, self).__init__(parent)

        palette = QPalette(self.palette())
        palette.setColor(palette.ColorRole.Base, Qt.GlobalColor.transparent)

        self.path: list[list[tuple[int, int]]] = []

    def set_path(self, path: list[list[tuple[int, int]]]):
        """
        Set the drawing path. This is one or more lists of coordinates.

        We'll loop through the lists, selecting a new colour and drawing the
        relevant lines.
        """
        self.path = path
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Paint the lines
        """
        qp = QPainter(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)

        colours = [
            QColor(255, 0, 0, 96),
            QColor(0, 255, 0, 96),
            QColor(0, 0, 255, 96),
        ]

        for index, path in enumerate(self.path):
            pen = QPen(colours[index % len(colours)])
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen.setWidth(self.LINE_WIDTH)
            qp.setPen(pen)

            # # draw a circle at the start of the path
            # qp.drawEllipse(
            #     path[0][0], path[0][1], self.LINE_WIDTH + 2, self.LINE_WIDTH + 2
            # )
            for i in range(len(path) - 1):
                offset = index * self.LINE_WIDTH // 2
                print(offset)
                qp.drawLine(
                    path[i][0] + offset,
                    path[i][1] + offset,
                    path[i + 1][0] + offset,
                    path[i + 1][1] + offset,
                )

            # TODO draw an arrow head for the last segment
