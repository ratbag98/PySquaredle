"""
A Squaredle-style letter grid using PyQt6
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QSizePolicy, QWidget


class Letter(QLabel):
    """
    A single letter in the grid.
    """

    def __init__(self, letter: str):
        super().__init__(letter)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.GlobalColor.darkGray)
        palette.setColor(self.foregroundRole(), Qt.GlobalColor.red)
        self.setPalette(palette)

        font = self.font()
        font.setPointSize(30)
        self.setFont(font)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)


class LetterGridWidget(QWidget):
    """
    Grid of letters.
    """

    def __init__(self, letters: str, side_length: int):
        super().__init__()

        self.side_length = side_length
        self.letters = letters

        self.setFixedSize(400, 400)

        self.grid = QGridLayout(self)

        for y in range(side_length):
            for x in range(side_length):
                letter = Letter(f"{letters[x * side_length + y]}")
                self.grid.addWidget(letter, x, y)

        self.setLayout(self.grid)

    def coord(self, index: int) -> tuple[int, int]:
        """
        Get the x, y coordinate for a given index.
        """
        return index % self.side_length, index // self.side_length

    # def line(self, start_index: int, end_index: int, color: Qt.GlobalColor) -> None:
    #     """
    #     Draw a line between two points.
    #     """
    #     start_x, start_y = self.coord(start_index)
    #     end_x, end_y = self.coord(end_index)

    #     # get global coordinates for centre of a QGridLayout cell
    #     g_x = (
    #         self.grid.columnViewportPosition(start_x)
    #         + self.grid.columnWidth(start_x) / 2
    #     )
    #     g_y = self.grid.rowViewportPosition(start_y) + self.grid.rowHeight(start_y) / 2
