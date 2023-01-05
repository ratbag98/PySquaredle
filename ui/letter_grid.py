"""
A Squaredle-style letter grid using PyQt6
"""

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QGridLayout, QLabel, QWidget

from ui.canvas import Canvas


class Letter(QLabel):
    """
    A single letter in the grid.
    """

    def __init__(self, letter: str):
        super().__init__(letter)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.GlobalColor.black)
        palette.setColor(self.foregroundRole(), Qt.GlobalColor.white)
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

        self.side_length = side_length
        self.letters = letters
        self.centres: dict[tuple[int, int], list[QPoint]] = {}

        self.setFixedSize(400, 400)

        self.grid = QGridLayout(self)

        for row in range(side_length):
            for col in range(side_length):
                letter = Letter(f"{letters[row * side_length + col]}")
                self.grid.addWidget(letter, row, col)

        # use this for drawing lines over the grid
        self.overlay = Canvas(self)
        self.setLayout(self.grid)

    def build_geometry(self) -> None:
        """
        Gather details about the grid ready for drawing lines on it
        Can only be called after the window is shown.
        """
        for i in range(len(self.letters)):
            (x, y) = self.get_grid_coords(i)
            center: QPoint = self.centre_of_cell(x, y)
            print(
                f"index {i} is at {x},{y} in the grid. {center.x()}, {center.y()} in the window."
            )

    def set_drawing_paths(self, paths: list[list[tuple[int, int]]]):
        self.overlay.set_path(paths)

    def path_from_indexes(self, indexes: list[int]) -> list[tuple[int, int]]:
        """
        Given a list of indexes, return a list of (x, y) tuples.
        """
        points: list[tuple[int, int]] = []
        for index in indexes:
            (x, y) = self.get_grid_coords(index)
            center: QPoint = self.centre_of_cell(x, y)
            print(
                f"index {index} is at {x},{y} in the grid. {center.x()}, {center.y()} in the window."
            )
            points.append((center.x(), center.y()))
        return points

    def get_grid_coords(self, index: int) -> tuple[int, int]:
        """
        Get the grid coordinates for a given index.
        """
        (x, y, _w, _h) = self.grid.getItemPosition(index)
        return (x, y)

    def centre_of_cell(self, x: int, y: int) -> QPoint:
        """
        Given a pair of grid x,y coords, get the graphics coords of the centre of the
        cell.
        """
        return self.grid.cellRect(x, y).center()

    # resize the overlay to match the grid size
    def resizeEvent(self, event: QResizeEvent) -> None:
        self.overlay.resize(event.size())

    def coord(self, index: int) -> tuple[int, int]:
        """
        Get the x, y coordinate for a given index.
        """
        return index % self.side_length, index // self.side_length

    # def line(self, start_index: int, end_index: int, color: Qt.GlobalColor) -> None:
    #     """
    #     Draw a line between two points.
    #     """
    #     start_x, start_y = self.coord(start_index)
    #     end_x, end_y = self.coord(end_index)

    #     # get global coordinates for centre of a QGridLayout cell
    #     g_x = (
    #         self.grid.columnViewportPosition(start_x)
    #         + self.grid.columnWidth(start_x) / 2
    #     )
    #     g_y = self.grid.rowViewportPosition(start_y) + self.grid.rowHeight(start_y) / 2
