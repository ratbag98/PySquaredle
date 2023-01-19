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

    def __init__(
        self,
        solver: Solver,
        alpha_sort: bool,
        multiple: bool = False,
    ):
        super().__init__()

        self.setWindowTitle("PySquaredle")

        self.solver = solver
        self.multiple = multiple

        self.words: list[str] = solver.raw_solution_words(sort=alpha_sort, length=True)

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

        self.hbox.addWidget(self.letter_grid, 100)
        self.hbox.addWidget(self.solutions, 0)
        self.resize(1000, 800)

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
        A user has clicked a word. Tell the letter grid to draw the path(s) for it
        """
        if self.multiple:
            self.letter_grid.set_drawing_paths(
                self.solver.solutions.paths(current_text)
            )
        else:
            self.letter_grid.set_drawing_paths(
                self.solver.solutions.paths(current_text)[0:1]
            )
