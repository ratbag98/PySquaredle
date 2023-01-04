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

        self.hbox = QHBoxLayout()

        self.letter_grid = LetterGridWidget(letters, grid_side_length)

        words.sort(key=len)

        solutions = self.create_solution_widget(words)

        container = QWidget()
        container.setLayout(self.hbox)
        self.setCentralWidget(container)

        self.hbox.addWidget(self.letter_grid)

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
