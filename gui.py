"""
Main GUI for PySquredle.

Interface will show grid and lists of solutions.

User can click on a word and show the path on the grid.

Animated mode will show solutions as they are found.
"""

import sys
from itertools import groupby

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
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

    def __init__(self, solver: Solver):
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


class WordListWidget(QWidget):
    """
    List of words in the solution.
    """

    def __init__(self, words: list[str]):
        super().__init__()
        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignTop)

        for word in words:
            label = ClickableLabel(word)
            self.vbox.addWidget(label)

        self.setLayout(self.vbox)


class ClickableLabel(QLabel):
    """
    Label that can be clicked.
    """

    def __init__(self, text: str):
        super().__init__(text)

        self.clicked = False

    def mousePressEvent(self, ev: QMouseEvent):
        """
        User clicked on a label, tell them what they clicked.
        """
        QLabel.mousePressEvent(self, ev)
        self.clicked = True
        print(f"You clicked {self.text()}")


class SolutionsScroller(QScrollArea):
    """
    Scroller for solutions.
    """

    def __init__(self, word_list_widget: WordListWidget):
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
            word_list_widget = WordListWidget(list(group))
            scroller = SolutionsScroller(word_list_widget)
            self.addTab(scroller, f"{key}")


class MainWindow(QMainWindow):
    """
    Main window for the application.
    """

    def __init__(self, solver: Solver):
        super().__init__()
        self.init_ui(solver)

    def init_ui(self, solver: Solver):
        """
        Initialize the UI.
        """

        self.setWindowTitle("PySquaredle")

        self.hbox = QHBoxLayout()

        letter_grid = LetterGridWidget(solver.puzzle.letters, solver.puzzle.side_length)

        words = solver.raw_solutions(sort=True)
        words.sort(key=len)

        solutions = self.create_solution_widget(words)

        self.hbox.addWidget(letter_grid)
        self.hbox.addWidget(solutions)

        container = QWidget()
        container.setLayout(self.hbox)

        self.setMinimumHeight(600)
        self.setMinimumWidth(800)

        self.setCentralWidget(container)

    def create_solution_widget(self, words: list[str]) -> SolutionsTabWidget:
        """
        Create the solution widget from a grouped-by-len list of solution words.
        """

        solutions = SolutionsTabWidget(words)
        solutions.setTabPosition(QTabWidget.TabPosition.West)
        solutions.setMovable(True)
        return solutions
