"""
Solve a Squardle Puzzle

Class
    Solver
"""

from functools import cached_property
from itertools import groupby
from typing import Callable

from pysquaredle.puzzle import Puzzle
from pysquaredle.solutions import Solutions
from pysquaredle.trie import Trie


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

    def __init__(
        self,
        letters: str,
        word_list_path: str,
        update_func: Callable[[str, list[int], int], None],
    ) -> None:
        self.progress_reporter = update_func
        self.puzzle = Puzzle(letters)
        self.word_trie: Trie = Trie()
        self._solutions: Solutions = Solutions()
        self.solution_generated = False

        self.word_list_count = 0

        # useful to optimise word list loading (ignore words that don't share
        # letters with the puzzle)
        self.unique_letters = "".join(sorted(set(letters)))
        self._load_words(word_list_path)

    @cached_property
    def solutions(self) -> Solutions:
        """
        Get our solutions
        """
        if not self.solution_generated:
            raise ValueError()
        return self._solutions

    @cached_property
    def list_neighbours(self) -> str:
        """
        Get our puzzle's neighbour list
        """
        return self.puzzle.list_neighbours()

    @cached_property
    def grid(self) -> str:
        """
        Get our puzzle's grid
        """
        return self.puzzle.grid()

    @cached_property
    def letters(self) -> str:
        """
        Get our puzzle's letters
        """
        return self.puzzle.letters

    @cached_property
    def side_length(self) -> int:
        """
        Get our puzzle's side length
        """
        return self.puzzle.side_length

    def solve(self) -> None:
        """
        Solve a puzzle. Builds the `solutions` list.
        """
        for index, letter in enumerate(list(self.letters)):
            chain = [index]
            self._attempt(chain, letter)

        self.solution_generated = True

    def formatted_solutions(
        self,
        alpha_sort: bool = False,
        length_group: bool = False,
        single_column: bool = False,
        headers: bool = False,
    ) -> str:
        """
        Print out a formatted list of solutions, modified by any bool arguments:
            alpha_sort:             alphabetically sort the solutions
            length_group:           group solutions by word length
            single_column:          present results as a single column
            headers:                for grouped results, include header by default
        """
        solutions_list = self.raw_solution_words(sort=alpha_sort, length=length_group)

        divider = "\n" if single_column else "\t"

        if not length_group:
            return str.join(divider, solutions_list)

        formatted = ""

        for key, group in groupby(solutions_list, key=len):
            if headers:
                formatted += (
                    f"===> {key} letter words\n\n{str.join(divider, group)}\n\n"
                )
            else:
                formatted += str.join(divider, group) + divider

        return formatted

    def raw_solution_words(self, sort: bool = False, length: bool = False) -> list[str]:
        """
        Convert solutions set into list, honoring sort flag
        """

        solutions: list[str] = self.solutions.words()
        if sort:
            solutions.sort()
        if length:
            solutions.sort(key=len)
        return solutions

    def _attempt(self, index_chain: list[int], word: str) -> None:
        """
        The recursive word finder. Builds chains of letters by iterating through cell neighbours
        Adds new found words to the solutions set, ignoring duplicates
        """

        hits: list[str] = self.word_trie.search(word)
        self.progress_reporter(word, index_chain, len(hits))

        if not hits:
            return

        if hits[0] == word:
            self._solutions.add(word, index_chain)

        for neighbour in self.puzzle.neighbours_of(index_chain[-1]):
            if neighbour not in index_chain:
                self._attempt(
                    index_chain + [neighbour],
                    "".join([word, self.letters[neighbour]]),
                )

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
