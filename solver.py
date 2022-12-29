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

    # process the word_list.txt using the following command:
    # gsed -e 's/^\(.*\)\s*$/\U\1/g' raw_word_list.txt > word_list.txt
    # in other words, uppercase, no trailing whitespace
    # "gsed" is GNU sed or similar (MacOS sed is BSD sed)

    DEFAULT_WORD_LIST = "./word_list.txt"

    def __init__(self, letters: str, word_list_path: str = DEFAULT_WORD_LIST) -> None:

        self.puzzle = Puzzle(letters)
        self.word_trie: Trie = Trie()
        self.solutions: set[str] = set()
        self.solution_generated = False

        self.word_list_count = 0

        # useful to optimise word list loading (ignore words that don't share
        # letters with the puzzle)
        self.unique_letters = "".join(sorted(set(letters)))
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
        for index, letter in enumerate(self.puzzle.letters):
            chain = [index]
            self._attempt(chain, letter)

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
                    print(f"===> {key} letter words\n")
                print(str.join(divider, group))
                if not args["headers"]:
                    print()
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

    def _attempt(self, index_chain: list[int], word: str) -> None:
        """
        The recursive word finder. Builds chains of letters by iterating through cell neighbours
        Adds new found words to the solutions set, ignoring duplicates
        """
        hits: list[str] = self.word_trie.search(word)

        if hits:
            if hits[0] == word:
                self.solutions.add(word)

            for neighbour in self.puzzle.neighbours_of(index_chain[-1]):
                if neighbour not in index_chain:
                    self._attempt(
                        index_chain + [neighbour],
                        "".join([word, self.puzzle.letters[neighbour]]),
                    )

    def _divider(self, single_column: bool) -> str:
        if single_column:
            return "\n"
        return "\t"

    def _load_words(self, word_list_path: str) -> None:
        # this is a known issue with Python up to version 3.15 (in the future!)
        # pylint: disable=unspecified-encoding
        with open(word_list_path) as words_file:
            for word in [
                w for w in words_file.read().splitlines() if self.interesting_word(w)
            ]:
                self.word_list_count += 1
                self.word_trie.insert(word)
        # pylint: enable=unspecified-encoding

    def interesting_word(self, word: str) -> bool:
        """
        Check if a word is interesting
        skip lines that are too long
        skip lines that don't start with a  letter from our puzzle
        skip lines with letters not in our puzzle
        """
        return (
            len(word) <= self.puzzle.cell_count
            and word[0] in self.unique_letters
            and word_only_contains_puzzle_letters(word, self.unique_letters)
        )


def word_only_contains_puzzle_letters(word: str, letters: str) -> bool:
    """
    Check if a word contains only letters from a given set
    """
    for letter in word:
        if letter not in letters:
            return False
    return True