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

        self.puzzle = str.upper(letters)
        self.cell_count = len(self.puzzle)
        self._set_size()
        self.neighbours: list[list[int]] = self._calculate_neighbours()

    def __repr__(self) -> str:
        return self.grid()

    def __getitem__(self, index: int):
        """
        Default accessor retrieves a single indexed character from the puzzle
        """
        return self.puzzle[index]

    def grid(self) -> str:
        """
        Convert the puzzle grid to a string
        """
        grid = ""
        for y in range(self.size):
            start = self._idx(0, y)
            end = self._idx(self.size, y)
            grid = grid + self.puzzle[start:end] + "\n"
        return grid

    def list_neighbours(self) -> str:
        """
        Generate a list of neighbours for each cell in the grid
        """
        return ",\n".join(self._row_of_neighbours(y) for y in range(self.size))

    def _row_of_neighbours(self, y: int) -> str:
        return ", ".join(
            [self._neighbours_to_string(self._idx(x, y)) for x in range(self.size)]
        )

    def _neighbours_to_string(self, index: int) -> str:
        return ":".join([str(elem) for elem in self.neighbours[index]])

    # find the linear index for a pair of puzzle coordinates
    def _idx(self, x: int, y: int) -> int:
        return x + (y * self.size)

    def _coord(self, index: int) -> tuple[int, int]:
        return index % self.size, index // self.size

    def _on_grid(self, x: int, y: int) -> bool:
        return x in range(0, self.size) and y in range(0, self.size)

    # this only depends on the size of the puzzle, not the letters
    def _calculate_neighbours(self) -> list[list[int]]:
        """
        create list of list of neighbouring cells for every cell in the puzzle
        """
        neighbours: list[list[int]] = []
        for i in range(self.cell_count):
            neighbours.append([])
            ox, oy = self._coord(i)
            for dx, dy in self.DELTAS:
                nx, ny = ox + dx, oy + dy
                if self._on_grid(nx, ny):
                    neighbours[self._idx(ox, oy)].append(self._idx(nx, ny))
        return neighbours

    def get_cell_count(self) -> int:
        """
        Number of letters in the grid
        """
        return self.cell_count

    # size of the grid is the length of a side. So a 3x3 grid is size 3
    def _set_size(self) -> None:
        side_length = math.sqrt(self.cell_count)

        if side_length % 1 == 0:
            self.size = int(side_length)
        else:
            raise ValueError()
