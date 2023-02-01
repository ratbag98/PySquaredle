"""
GUI's main window class
"""

from typing import Callable

from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QTabWidget, QWidget

from pysquaredle.puzzle import Puzzle
from pysquaredle.solver import Solver
from pysquaredle.ui.letter_grid import LetterGridWidget
from pysquaredle.ui.solutions_tab_widget import SolutionsTabWidget


# happy to disable this warning since they're mainly GUI-related
# pylint: disable=too-many-instance-attributes
class MainWindow(QMainWindow):
    """
    Main window for the application.
    """

    def __init__(
        self,
        puzzle: Puzzle,
        solver: Solver,
        alpha_sort: bool,
        multiple: bool = False,
    ):
        super().__init__()

        self.setWindowTitle("PySquaredle")

        self.solver = solver
        self.puzzle = puzzle
        self.multiple = multiple

        self.words: list[str] = solver.raw_solution_words(sort=alpha_sort, length=True)

        # set up the interface (a simple HBox)
        self.hbox = QHBoxLayout()

        container = QWidget()
        container.setLayout(self.hbox)
        self.setCentralWidget(container)

        # big grid of letters to show the solution graphically
        self.letter_grid = LetterGridWidget(puzzle.letters, puzzle.side_length)

        # scrolling list of solutions grouped by word length
        # detect clicks and update the big grid of letters accordingly
        self.solutions_widget = self._create_solution_widget(
            self.words, self.current_text_changed
        )

        # the actual interface is just two widgets side-by-side
        self.hbox.addWidget(self.letter_grid, 100)
        self.hbox.addWidget(self.solutions_widget, 0)
        self.resize(1000, 800)

        self.status_bar = self.statusBar()
        self.status()
        self.show()

    def status(self) -> None:
        """
        Show the solution status in the status bar
        """
        word_count = self.solver.word_count()
        sol_count = self.solver.path_count()
        self.status_bar.showMessage(
            f"{word_count} unique words found, {sol_count} total solutions"
        )

    def _create_solution_widget(
        self, words: list[str], current_text_changed: Callable[[str], None]
    ) -> SolutionsTabWidget:
        """
        Create the solution widget from a grouped-by-len list of solution words.
        """

        solutions_widget = SolutionsTabWidget(words, current_text_changed)
        solutions_widget.setTabPosition(QTabWidget.TabPosition.West)
        solutions_widget.setMovable(True)
        return solutions_widget

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
                self.solver.solutions.paths(current_text)[:1]
            )