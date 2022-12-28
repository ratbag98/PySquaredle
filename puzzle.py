"""
Represent Squaredle puzzles

Class:
    Puzzle
"""

import math


class Puzzle:
    """
    represent a Squaredle puzzle (httos://squaredle.app)
    a bunch of letters
    a list of neighbours for each cell in a grid
    """

    # neighbour coordinates for a cell
    # format off since it shows the shape of neighbours
    # fmt: off
    DELTAS = [[-1, -1], [0, -1],    [1, -1],
              [-1, 0],              [1, 0],
              [-1, 1],  [0, 1],     [1, 1]]
    # fmt: on

    def __init__(self, letters: str):
        """
        Create a Squaredle puzzle.

        letters   a string of letters representing the puzzle, left to right, top to bottom

        The letters string's length must be a square number (9, 16, 25 etc).
        """

        self.cell_count = len(letters)
        self.side_length = self._side_length()

        self._letters = str.upper(letters)
        self._neighbours: list[list[int]] = self._calculate_neighbours()

    @property
    def letters(self) -> str:
        """
        The letters in the puzzle
        """
        return self._letters

    def __repr__(self) -> str:
        return self.grid()

    def grid(self) -> str:
        """
        Convert the puzzle grid to a string
        """
        grid = ""
        for y in range(self.side_length):
            start = self._idx(0, y)
            end = self._idx(self.side_length, y)
            grid = "".join([grid, self._letters[start:end], "\n"])
        return grid

    def neighbours_of(self, cell: int) -> list[int]:
        """
        Return a list of neighbours for the referenced cell
        """
        return self._neighbours[cell]

    def list_neighbours(self) -> str:
        """
        Generate a list of neighbours for each cell in the grid
        """
        return ",\n".join(self._row_of_neighbours(y) for y in range(self.side_length))

    def _row_of_neighbours(self, y: int) -> str:
        return ", ".join(
            [
                self._neighbours_to_string(self._idx(x, y))
                for x in range(self.side_length)
            ]
        )

    def _neighbours_to_string(self, index: int) -> str:
        return ":".join([str(elem) for elem in self._neighbours[index]])

    # find the linear index for a pair of puzzle coordinates
    def _idx(self, x: int, y: int) -> int:
        return x + (y * self.side_length)

    def _coord(self, index: int) -> tuple[int, int]:
        return index % self.side_length, index // self.side_length

    def _on_grid(self, x: int, y: int) -> bool:
        return x in range(0, self.side_length) and y in range(0, self.side_length)

    # this only depends on the size of the puzzle, not the letters
    def _calculate_neighbours(self) -> list[list[int]]:
        """
        create list of list of neighbouring cells for every cell in the puzzle
        """
        neighbours: list[list[int]] = []
        for ox, oy in [self._coord(i) for i in range(self.cell_count)]:
            neighbours.append(
                [
                    self._idx(nx, ny)
                    for nx, ny in [(ox + dx, oy + dy) for dx, dy in self.DELTAS]
                    if self._on_grid(nx, ny)
                ]
            )
        return neighbours

    # size of the grid is the length of a side. So a 3x3 grid is size 3
    def _side_length(self) -> int:
        side_length = math.sqrt(self.cell_count)

        if side_length % 1 != 0:
            raise ValueError()

        return int(side_length)
