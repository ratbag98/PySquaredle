from itertools import groupby

from puzzle import Puzzle
from trie import Trie


class NotSolvedYetException(Exception):
    """
    Puzzle.solve() must be called before solutions are requested
    """

    def __init__(
        self,
        message: str=".solve() must be called before requesting solutions",
        *args: object
    ) -> None:
        super().__init__(*args)


class Solver:
    """
    Solve a Squaredle Puzzle.

    The puzzle is represented by a Puzzle object.

    We maintain a word list stored as a trie for speedy starts with searches
    We use a recursive chain builder to find solutions in the grid
    """

    DEFAULT_WORD_LIST = "./word_list.txt"

    def __init__(self, letters: str, word_list: str=DEFAULT_WORD_LIST) -> None:
        self.puzzle = Puzzle(letters)
        self.cell_count = self.puzzle._get_cell_count()
        self.max_word_length = self.puzzle._get_cell_count()
        self.tr = Trie()
        self.solutions = set()
        self.solution_generated = False

        self.word_list_count = 0
        self._load_words(word_list)


    def list_neighbours(self) -> str:
        return self.puzzle.list_neighbours()

    def grid(self) -> str:
        return self.puzzle.grid()

    def solve(self) -> None:
        for index in range(self.cell_count):
            chain = [index]
            word = self.puzzle[index]
            self._attempt(chain, word)

        self.solution_generated = True

    def print_solutions(self, args) -> None:
        solutions_list = self.raw_solutions(args["sort"])

        divider = self._divider(args["single_column"])

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

    def raw_solutions(self, sorted=False) -> list[str]:
        if not self.solution_generated:
            raise NotSolvedYetException()

        solutions = list(self.solutions)
        if sorted:
            solutions.sort()
        return solutions

    def word_list_length(self) -> int:
        """
        Number of words in the filtered list. Only words of length 4 to the
        size of the puzzle are loaded.
        """
        return self.word_list_count


    def _attempt(self, index_chain, word) -> None:
        hits = self.tr.search(word)

        if hits:
            if hits[0] == word:
                self.solutions.add(word)

            # TODO worth putting cell and neighour list in a tuple in the Puzzle?
            for n in self.puzzle.neighbours[index_chain[-1]]:
                if not n in index_chain:
                    self._attempt(index_chain + [n], word + self.puzzle[n])

    def _divider(self, single_column) -> str:
        if single_column:
            return "\n"
        else:
            return "\t"

    def _load_words(self, word_list) -> None:
        with open(word_list) as wl:
            lines = wl.readlines()
            for l in [str.upper(line.rstrip()) for line in lines]:
                if len(l) <= self.max_word_length:
                    self.word_list_count += 1
                    self.tr.insert(l)
