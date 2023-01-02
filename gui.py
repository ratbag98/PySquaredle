"""
Main GUI for PySquredle.

Interface will show grid and lists of solutions.

User can click on a word and show the path on the grid.

Animated mode will show solutions as they are found.
"""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QTabWidget,
    QWidget,
)

from solver import Solver


class Application(QApplication):
    """
    Main application for the application.
    """

    def __init__(self, solver: Solver, *args, **kwargs):
        super().__init__(sys.argv)

        self.main_window = MainWindow(solver)
        self.main_window.show()


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


class LetterGrid(QWidget):
    """
    Grid of letters.
    """

    def __init__(self, letters: str, side_length: int):
        super().__init__()

        self.setFixedSize(400, 400)

        self.letters = letters

        layout = QGridLayout()

        for y in range(side_length):
            for x in range(side_length):
                l = Letter(f"{letters[x * side_length + y]}")
                layout.addWidget(l, x, y)

        self.setLayout(layout)


class SolutionsTabWidget(QTabWidget):
    """
    Tab widget to show solutions.
    """

    def __init__(self):
        super().__init__()

        self.setFixedSize(400, 400)

        self.addTab(QWidget(), "Four")
        self.addTab(QWidget(), "Five")
        self.addTab(QWidget(), "Six")
        self.addTab(QWidget(), "Seven")
        self.addTab(QWidget(), "Eight")
        self.addTab(QWidget(), "Nine")
        self.addTab(QWidget(), "Ten")


class MainWindow(QMainWindow):
    """
    Main window for the application.
    """

    def __init__(self, solver: Solver):
        super().__init__()

        self.setWindowTitle("PySquaredle")

        layout = QHBoxLayout()

        letter_grid = LetterGrid(solver.puzzle.letters, solver.puzzle.side_length)

        layout.addWidget(letter_grid)

        solutions = SolutionsTabWidget()
        solutions.setTabPosition(QTabWidget.TabPosition.West)
        solutions.setMovable(True)

        layout.addWidget(solutions)

        container = QWidget()
        container.setLayout(layout)

        self.setMinimumHeight(600)
        self.setMinimumWidth(800)

        self.setCentralWidget(container)
