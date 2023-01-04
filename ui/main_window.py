"""
GUI's main window class
"""

from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QTabWidget, QWidget

from ui.letter_grid import LetterGridWidget
from ui.solutions_tab_widget import SolutionsTabWidget


class MainWindow(QMainWindow):
    """
    Main window for the application.
    """

    def __init__(self, letters: str, words: list[str], grid_side_length: int):
        super().__init__()

        self.setWindowTitle("PySquaredle")

        # set up the interface (a simple HBox)
        self.hbox = QHBoxLayout()
        container = QWidget()
        container.setLayout(self.hbox)
        self.setCentralWidget(container)

        # the actual interface is just two widgets side-by-side
        self.letter_grid = LetterGridWidget(letters, grid_side_length)
        self.solutions = self._create_solution_widget(words)

        self.hbox.addWidget(self.letter_grid)
        self.hbox.addWidget(self.solutions)

    def _create_solution_widget(self, words: list[str]) -> SolutionsTabWidget:
        """
        Create the solution widget from a grouped-by-len list of solution words.
        """

        solutions = SolutionsTabWidget(words)
        solutions.setTabPosition(QTabWidget.TabPosition.West)
        solutions.setMovable(True)
        return solutions
