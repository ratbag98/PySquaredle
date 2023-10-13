"""A Qt application for the GUI application."""

from PyQt6.QtWidgets import QApplication

from pysquaredle.puzzle import Puzzle
from pysquaredle.solver import Solver
from pysquaredle.ui.main_window import MainWindow


class Application(QApplication):
    """Main application for the GUI application. Ignored unless --gui is set."""

    def __init__(
        self,
        puzzle: Puzzle,
        solver: Solver,
        alpha_sort: bool = True,
        multiple: bool = False,
    ):
        super().__init__([])

        self.main_window = MainWindow(puzzle, solver, alpha_sort, multiple)
        self.main_window.show()
