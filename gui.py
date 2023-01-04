"""
Main GUI for PySquredle.

Interface will show grid and lists of solutions.

User can click on a word and show the path on the grid.

Animated mode will show solutions as they are found.
"""

import sys

from PyQt6.QtWidgets import QApplication

from pysquaredle.solver import Solver
from ui.main_window import MainWindow


class Application(QApplication):
    """
    Main application for the application. Encapsulates any calls to Solver or Puzzle.
    """

    def __init__(self, solver: Solver):
        super().__init__(sys.argv)

        self.main_window = MainWindow(
            solver.puzzle.letters, solver.raw_solutions(True), solver.puzzle.side_length
        )
        self.main_window.show()
