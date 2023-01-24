"""
A Squaredle-style letter grid using PyQt6
"""

from PyQt6.QtCore import QPoint, QRect, QSize, Qt
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QGridLayout, QLabel, QSizePolicy, QWidget

from ui.overlay import Overlay


class LetterWidget(QLabel):
    """
    A single letter in the grid.
    """

    def __init__(self, letter: str) -> None:
        super().__init__(letter)

        #        self.setAutoFillBackground(True)
        self.setStyleSheet(
            "border: 3px solid gray; border-radius: 12px; background-color: #202020; color: white;"
        )

        font = self.font()
        font.setPointSize(36)
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)


class LetterGridWidget(QWidget):
    """
    Grid of letters.
    """

    def __init__(self, letters: str, side_length: int):
        super().__init__()

        # keep this for resize events, we need to
        # recalculate lines based on new size
        self.current_chains: list[list[int]] = []

        self.grid = QGridLayout(self)

        # grow, but keep square (see resizeEvent)
        policy = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
        )
        self.setSizePolicy(policy)

        # set up the grid
        for row in range(side_length):
            self.grid.setRowStretch(row, 1)
            for col in range(side_length):
                self.grid.setColumnStretch(col, 1)
                letter = LetterWidget(f"{letters[row * side_length + col]}")

                self.grid.addWidget(letter, row, col)
                if letters[row * side_length + col] == "_":
                    letter.setHidden(True)

        # use this for drawing lines over the grid
        self.overlay = Overlay(self)

        # we're a grid, don't forget it
        self.setLayout(self.grid)
        self.current_chains: list[list[int]] = []

    def set_drawing_paths(self, chains: list[list[int]]):
        """
        Tell the overlay canvas to draw the given paths. Remember the raw
        chains of grid coordinates so we can redraw them when the window
        resizes.
        """
        self.current_chains = chains
        paths: list[list[tuple[int, int]]] = [
            self._path_from_indexes(chain) for chain in self.current_chains
        ]

        self.overlay.set_paths(paths)

    def _path_from_indexes(self, indexes: list[int]) -> list[tuple[int, int]]:
        """
        Given a list of indexes, return a list of (x, y) tuples.

        This scales up from the grid coordinates to the Widget coordinates.

        Must be called whenever we resize or the user changes their selected word
        """
        return [(self._centre_of_cell(index)) for index in indexes]

    def _centre_of_cell(self, index: int) -> tuple[int, int]:
        """
        Calculate center of a given Grid cell
        """
        (x, y, _w, _h) = self.grid.getItemPosition(index)
        center: QPoint = self.grid.cellRect(x, y).center()
        return center.x(), center.y()

    # pylint: disable=arguments-differ,invalid-name
    def resizeEvent(self, event: QResizeEvent) -> None:  # type: ignore
        """
        Make sure we're square and resize the overlay to match the grid size
        """

        # kludgy code to keep us square
        super().resizeEvent(event)
        l = min(event.size().width(), event.size().height())
        center = self.rect().center()
        rect = QRect(0, 0, l, l)
        rect.moveCenter(center)
        self.setGeometry(rect)

        # recalculate the coordinates of the path using the new grid size
        self.set_drawing_paths(self.current_chains)

        # tell overlay to resize

        self.overlay.resize(rect.size())

    def sizeHint(self) -> QSize:
        """
        At least start off square
        """
        return QSize(400, 400)

    # pylint: enable=arguments-differ,invalid-name
