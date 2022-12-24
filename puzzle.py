from trie import Trie
from itertools import groupby
import sys
import math

# represent and solve a Squaredle puzzle (httos://squaredle.app)
# a bunch of letters
# a list of neighbours for each cell in a grid
# a word list stored as a trie for speedy starts with searches
# a recursive chain builder to find solutions in the grid


class Puzzle:

    # neighbour coordinates for a cell
    # format off since it shows the shape of neighbours
    # fmt: off
    DELTAS = [[-1, -1], [0, -1],    [1, -1],
              [-1, 0],              [1, 0],
              [-1, 1],  [0, 1],     [1, 1]]
    # fmt: on

    WORD_LIST = "./word_list.txt"

    def __init__(self, letters, word_list=WORD_LIST):
        """
        Create a Squaredle puzzle.

        letters   a string of letters representing the puzzle, left to right, top to bottom

        The letters string's length must be a square number (9, 16, 25 etc).
        """

        self.puzzle = str.upper(letters)
        self.cell_count = len(self.puzzle)
        self.__set_size()
        self.neighbours = self.__calculate_neighbours()

        self.tr = Trie()
        self.solutions = set()
        self.solution_generated = False

        self.word_list_count = 0
        self.__load_words(word_list)

    def grid(self):
        grid = ""
        for y in range(self.size):
            start = self.__idx(0, y)
            end = self.__idx(self.size, y)
            grid = grid + self.puzzle[start:end] + "\n"
        return grid

    # generate a list of neighbours for each cell in the grid
    def list_neighbours(self):
        return ",\n".join(self.__row_of_neighbours(y) for y in range(self.size))

    def __row_of_neighbours(self, y):
        return ", ".join(
            [self.__neighbours_to_string(self.__idx(x, y)) for x in range(self.size)]
        )

    def __neighbours_to_string(self, index):
        return ":".join([str(elem) for elem in self.neighbours[index]])

    def solve(self):
        for index in range(self.cell_count):
            chain = [index]
            word = self.puzzle[index]
            self.__attempt(chain, word)

        self.solution_generated = True

    def print_solutions(self, args):
        solutions_list = self.raw_solutions(args["sort"])

        divider = self.divider(args["single_column"])

        if args["length"]:
            solutions_list.sort(key=len)
            grouped = [list(i) for j, i in groupby(solutions_list, key=len)]

            for group in grouped:
                length = len(group[0])
                if not args["headers"]:
                    print("===> ", length, " letter words\n")
                print(str.join(divider, group))
                if not args["headers"]:
                    print()
        else:
            print(str.join(divider, solutions_list))

    def raw_solutions(self, sorted=False):
        if not self.solution_generated:
            raise Exception(".solve() must be called before .print_solutions()")

        solutions = list(self.solutions)
        if sorted:
            solutions.sort()
        return solutions

    def divider(self, single_column):
        if single_column:
            return "\n"
        else:
            return "\t"

    # find the linear index for a pair of puzzle coordinates
    def __idx(self, x, y):
        return x + (y * self.size)

    def __coord(self, index):
        return index % self.size, index // self.size

    def __on_grid(self, x, y):
        return x in range(0, self.size) and y in range(0, self.size)

    def __calculate_neighbours(self):
        """
        create list of list of neighbouring cells for every cell in the puzzle
        """
        neighbours = []
        for i in range(self.cell_count):
            neighbours.append([])
            ox, oy = self.__coord(i)
            for dx, dy in self.DELTAS:
                nx, ny = ox + dx, oy + dy
                if self.__on_grid(nx, ny):
                    neighbours[self.__idx(ox, oy)].append(self.__idx(nx, ny))
        return neighbours

    def __load_words(self, word_list):
        with open(word_list) as wl:
            lines = wl.readlines()
            for l in [str.upper(line.rstrip()) for line in lines]:
                if len(l) <= self.size * self.size:
                    self.word_list_count += 1
                    self.tr.insert(l)

    def __attempt(self, index_chain, word):
        hits = self.tr.search(word)

        if hits:
            if hits[0] == word:
                self.solutions.add(word)

            for n in self.neighbours[index_chain[-1]]:
                if not n in index_chain:
                    self.__attempt(index_chain + [n], word + self.puzzle[n])

    def __set_size(self):
        sideLength = math.sqrt(self.cell_count)

        if sideLength % 1 == 0:
            self.size = int(sideLength)
        else:
            raise Exception(
                "Length of letters must be a square number (9, 16, 25 etc.)"
            )

    def word_list_length(self):
        """
        Number of words in the filtered list. Only words of length 4 to the
        size of the puzzle are loaded.
        """
        return self.word_list_count
