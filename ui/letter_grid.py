"""
A Squaredle-style letter grid using PyQt6
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QLabel, QWidget


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

        self.setFixedSize(400, 400)

        self.letters = letters

        grid = QGridLayout()

        for y in range(side_length):
            for x in range(side_length):
                letter = Letter(f"{letters[x * side_length + y]}")
                grid.addWidget(letter, x, y)

        self.setLayout(grid)
