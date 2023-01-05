"""
A Squaredle-style letter grid using PyQt6
"""

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QGridLayout, QLabel, QWidget

from ui.overlay import Overlay


class Letter(QLabel):
    """
    A single letter in the grid.
    """

    def __init__(self, letter: str):
        super().__init__(letter)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.GlobalColor.black)
        palette.setColor(self.foregroundRole(), Qt.GlobalColor.white)
        self.setPalette(palette)

        font = self.font()
        font.setPointSize(30)
        font.setBold(True)
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

        self.setFixedSize(600, 600)

        self.grid = QGridLayout(self)

        for row in range(side_length):
            for col in range(side_length):
                letter = Letter(f"{letters[row * side_length + col]}")
                self.grid.addWidget(letter, row, col)

        # use this for drawing lines over the grid
        self.overlay = Overlay(self)
        self.setLayout(self.grid)

    def set_drawing_paths(self, chains: list[list[int]]):
        """
        Tell the overlay canvas to draw the given paths.
        """
        paths: list[list[tuple[int, int]]] = []
        for chain in chains:
            paths.append(self._path_from_indexes(chain))

        self.overlay.set_paths(paths)

    def _path_from_indexes(self, indexes: list[int]) -> list[tuple[int, int]]:
        """
        Given a list of indexes, return a list of (x, y) tuples.
        """
        points: list[tuple[int, int]] = []
        for index in indexes:
            (x, y, _w, _h) = self.grid.getItemPosition(index)
            center: QPoint = self.grid.cellRect(x, y).center()
            points.append((center.x(), center.y()))
        return points

    # resize the overlay to match the grid size
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.overlay.resize(event.size())
