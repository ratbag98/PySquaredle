"""
Solve a Squardle Puzzle

Class
    Solver
"""

from itertools import groupby

from puzzle import Puzzle
from trie import Trie


class Solver:
    """
    Solve a Squaredle Puzzle.

    The puzzle is represented by a Puzzle object.

    We maintain a word list stored as a trie for speedy starts with searches
    We use a recursive chain builder to find solutions in the grid
    """

    DEFAULT_WORD_LIST = "./word_list.txt"

    def __init__(self, letters: str, word_list_path: str = DEFAULT_WORD_LIST) -> None:
        self.puzzle = Puzzle(letters)
        self.cell_count = self.puzzle.get_cell_count()
        self.max_word_length = self.puzzle.get_cell_count()
        self.word_trie: Trie = Trie()
        self.solutions: set[str] = set()
        self.solution_generated = False

        self.word_list_count = 0
        self._load_words(word_list_path)

    def list_neighbours(self) -> str:
        """
        Get our puzzle's neighbour list
        """
        return self.puzzle.list_neighbours()

    def grid(self) -> str:
        """
        Get our puzzle's grid
        """
        return self.puzzle.grid()

    def solve(self) -> None:
        """
        Solve a puzzle. Builds the `solutions` list.
        """
        for index in range(self.cell_count):
            chain = [index]
            word = self.puzzle[index]
            self._attempt(chain, word)

        self.solution_generated = True

    def print_solutions(self, args: dict[str, bool]) -> None:
        """
        Print out a formatted list of solutions, modified by any bool arguments:
            sort:           alphabetically sort the solutions
            length:         group solutions by word length
            single_column:  present results as a single column
            headers:        for grouped results, include header by default
        """
        solutions_list = self.raw_solutions(args["sort"])

        divider = self._divider(args["single_column"])

        if args["length"]:
            solutions_list.sort(key=len)

            for key, group in groupby(solutions_list, key=len):
                if not args["headers"]:
                    print("===> ", key, " letter words\n")
                print(str.join(divider, group))
                if not args["headers"]:
                    print()

            # grouped = [list(i) for _, i in groupby(solutions_list, key=len)]

            # for group in grouped:
            #     length = len(group[0])
            #     if not args["headers"]:
            #         print("===> ", length, " letter words\n")
            #     print(str.join(divider, group))
            #     if not args["headers"]:
            #         print()
        else:
            print(str.join(divider, solutions_list))

    def raw_solutions(self, sort: bool = False) -> list[str]:
        """
        Convert solutions set into list, honoring sort flag
        """
        if not self.solution_generated:
            raise ValueError()

        solutions: list[str] = list(self.solutions)
        if sort:
            solutions.sort()
        return solutions

    def word_list_length(self) -> int:
        """
        Number of words in the filtered list. Only words of length 4 to the
        size of the puzzle are loaded.
        """
        return self.word_list_count

    def _attempt(self, index_chain: list[int], word: str) -> None:
        hits: list[str] = self.word_trie.search(word)

        if hits:
            if hits[0] == word:
                self.solutions.add(word)

            # TODO worth putting cell and neighour list in a tuple in the Puzzle?
            for n in self.puzzle.neighbours[index_chain[-1]]:
                if not n in index_chain:
                    self._attempt(index_chain + [n], word + self.puzzle[n])

    def _divider(self, single_column: bool) -> str:
        if single_column:
            return "\n"
        return "\t"

    def _load_words(self, word_list_path: str) -> None:
        # this is a known issue with Python up to version 3.15 (in the future!)
        # pylint: disable=unspecified-encoding
        with open(word_list_path) as words_file:
            lines = words_file.readlines()
            for l in [str.upper(line.rstrip()) for line in lines]:
                if len(l) <= self.max_word_length:
                    self.word_list_count += 1
                    self.word_trie.insert(l)
        # pylint: enable=unspecified-encoding
