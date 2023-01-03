"""
Main GUI for PySquredle.

Interface will show grid and lists of solutions.

User can click on a word and show the path on the grid.

Animated mode will show solutions as they are found.
"""

import sys
from itertools import groupby

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
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


class WordList(QWidget):
    """
    List of words in the solution.
    """

    def __init__(self, words: list[str]):
        super().__init__()
        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignTop)

        for word in words:
            self.vbox.addWidget(QLabel(word))

        self.setLayout(self.vbox)


class SolutionsScroller(QScrollArea):
    """
    Scroller for solutions.
    """

    def __init__(self, word_list_widget: WordList):
        super().__init__()

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.setWidget(word_list_widget)


class SolutionsTabWidget(QTabWidget):
    """
    Tab widget to show solutions.
    """

    def __init__(self, words: list[str]):
        super().__init__()

        for key, group in groupby(words, key=len):
            word_list_widget = WordList(list(group))
            scroller = SolutionsScroller(word_list_widget)
            self.addTab(scroller, f"{key}")


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

        words = solver.raw_solutions(sort=True)
        words.sort(key=len)

        solutions = SolutionsTabWidget(words)
        solutions.setTabPosition(QTabWidget.TabPosition.West)
        solutions.setMovable(True)

        layout.addWidget(solutions)

        container = QWidget()
        container.setLayout(layout)

        self.setMinimumHeight(600)
        self.setMinimumWidth(800)

        self.setCentralWidget(container)
