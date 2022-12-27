import math


class NonSquarePuzzleException(Exception):
    """
    All puzzles must be square. For example 3x3, 4x4 etc.
    """

    def __init__(
        self,
        message: str ="Length of letters must be a square number (9, 16, 25 etc.)",
        *args: object
    ) -> None:
        super().__init__(*args)


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
        self.neighbours = self._calculate_neighbours()

    def __getitem__(self, index: int):
        """
        Default accessor retrieves a single indexed character from the puzzle
        """
        return self.puzzle[index]

    def grid(self) -> str:
        grid = ""
        for y in range(self.size):
            start = self._idx(0, y)
            end = self._idx(self.size, y)
            grid = grid + self.puzzle[start:end] + "\n"
        return grid

    # generate a list of neighbours for each cell in the grid
    def list_neighbours(self) -> str:
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

    def _coord(self, index: int) -> tuple:
        return index % self.size, index // self.size

    def _on_grid(self, x: int, y: int) -> bool:
        return x in range(0, self.size) and y in range(0, self.size)

    # this only depends on the size of the puzzle, not the letters
    def _calculate_neighbours(self) -> list[list[int]]:
        """
        create list of list of neighbouring cells for every cell in the puzzle
        """
        neighbours = []
        for i in range(self.cell_count):
            neighbours.append([])
            ox, oy = self._coord(i)
            for dx, dy in self.DELTAS:
                nx, ny = ox + dx, oy + dy
                if self._on_grid(nx, ny):
                    neighbours[self._idx(ox, oy)].append(self._idx(nx, ny))
        return neighbours

    def _get_cell_count(self) -> int:
        return self.cell_count

    # size of the grid is the length of a side. So a 3x3 grid is size 3
    def _set_size(self) -> None:
        sideLength = math.sqrt(self.cell_count)

        if sideLength % 1 == 0:
            self.size = int(sideLength)
        else:
            raise NonSquarePuzzleException
