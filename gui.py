"""
Main GUI for PySquredle.

Interface will show grid and lists of solutions.

User can click on a word and show the path on the grid.

Animated mode will show solutions as they are found.
"""

import sys

from PyQt6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QTabWidget, QWidget

from pysquaredle.solver import Solver
from solutions_tab_widget import SolutionsTabWidget
from ui.letter_grid import LetterGridWidget

for place in sys.path:
    print(place)


class Application(QApplication):
    """
    Main application for the application.
    """

    def __init__(self, solver: Solver):
        super().__init__(sys.argv)

        self.main_window = MainWindow(solver)
        self.main_window.show()


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

        container = QWidget()
        container.setLayout(self.hbox)
        self.setCentralWidget(container)

        self.hbox.addWidget(letter_grid)

        self.hbox.addWidget(solutions)

        self.setMinimumHeight(600)
        self.setMinimumWidth(800)

    def create_solution_widget(self, words: list[str]) -> SolutionsTabWidget:
        """
        Create the solution widget from a grouped-by-len list of solution words.
        """

        solutions = SolutionsTabWidget(words)
        solutions.setTabPosition(QTabWidget.TabPosition.West)
        solutions.setMovable(True)
        return solutions
