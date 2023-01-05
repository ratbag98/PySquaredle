"""
GUI's main window class
"""

from typing import Callable

from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QTabWidget, QWidget

from pysquaredle.solver import Solver
from ui.letter_grid import LetterGridWidget
from ui.solutions_tab_widget import SolutionsTabWidget


class MainWindow(QMainWindow):
    """
    Main window for the application.
    """

    def __init__(self, solver: Solver):
        super().__init__()

        self.setWindowTitle("PySquaredle")

        self.solver = solver
        self.words = solver.raw_solution_words(True)
        self.words.sort(key=len)

        # set up the interface (a simple HBox)
        self.hbox = QHBoxLayout()
        container = QWidget()
        container.setLayout(self.hbox)
        self.setCentralWidget(container)

        # the actual interface is just two widgets side-by-side
        self.letter_grid = LetterGridWidget(solver.letters, solver.side_length)
        self.solutions = self._create_solution_widget(
            self.words, self.current_text_changed
        )

        self.hbox.addWidget(self.letter_grid)
        self.hbox.addWidget(self.solutions)

    def build_grid_geometry(self):
        """
        Gather details about the grid ready for drawing lines on it
        Can only be called after the window is shown.
        """
        self.letter_grid.build_geometry()

    def _create_solution_widget(
        self, words: list[str], current_text_changed: Callable[[str], None]
    ) -> SolutionsTabWidget:
        """
        Create the solution widget from a grouped-by-len list of solution words.
        """

        solutions = SolutionsTabWidget(words, current_text_changed)
        solutions.setTabPosition(QTabWidget.TabPosition.West)
        solutions.setMovable(True)
        return solutions

    def current_text_changed(self, current_text: str):
        """
        Print the current text for now. Will soon send up to the main window.
        """
        print(current_text)
        path: list[list[tuple[int, int]]] = []
        for chain in self.solver.solutions.paths(current_text):
            path.append(self.letter_grid.path_from_indexes(chain))
        self.letter_grid.set_drawing_paths(path)
        print(self.solver.solutions.paths(current_text))
