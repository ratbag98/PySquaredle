""" Solve a Squardle Puzzle """

from collections.abc import Callable
from functools import cached_property
from typing import Optional

import rich.progress

from pysquaredle.puzzle import Puzzle
from pysquaredle.solutions import Solutions
from pysquaredle.trie import Trie


class Solver:
    """Solve a Squaredle Puzzle.

    We maintain a word list stored as a trie for speedy starts with searches
    We use a recursive chain builder to find solutions in the grid
    """

    # process the word_list.txt using the following command:
    # gsed -e 's/^\(.*\)\s*$/\U\1/g' raw_word_list.txt > word_list.txt
    # in other words, uppercase, no trailing whitespace
    # "gsed" is GNU sed or similar (MacOS sed is BSD sed)

    def __init__(
        self,
        puzzle: Puzzle,
        word_list_path: str,
        update_func: Optional[Callable[[str, list[int], int], None]] = None,
    ) -> None:
        # this can do "something" whilst the solutions are generated
        self._progress_reporter = update_func

        self._puzzle = puzzle
        self._word_trie: Trie = Trie()
        self._solutions: Solutions = Solutions()

        self.word_list_count = 0

        self._load_words(word_list_path)

        # now for the good stuff
        self.solve()

    @cached_property
    def solutions(self) -> Solutions:
        """Get our solutions"""

        return self._solutions

    def has_unacceptable_words(self) -> bool:
        """Does the list of solutions include any unacceptable words"""
        return len(self._solutions.unacceptable_solutions()) > 0

    def solve(self) -> None:
        """Solve a puzzle. Builds the `solutions` list."""

        for index, letter in enumerate(self._puzzle.letters):
            chain = [index]
            self._attempt(chain, letter)

    def formatted_solutions(
        self,
        alpha_sort: bool = False,
        length_group: bool = False,
        single_column: bool = False,
        headers: bool = False,
    ) -> str:
        """Pass the formatted solutions from our solutions object"""

        return self._solutions.formatted_solutions(
            alpha_sort, length_group, single_column, headers
        )

    def raw_solution_words(self, sort: bool = False, length: bool = False) -> list[str]:
        """Pass the raw solution words from our solutions object"""

        return self._solutions.raw_solution_words(sort, length)

    def _attempt(self, index_chain: list[int], word: str) -> None:
        """The recursive word finder. Builds chains of letters by iterating
        through cell neighbours. Adds new found words to the solutions set,
        ignoring duplicates"""

        hits: list[str] = self._word_trie.search(word)

        if self._progress_reporter:
            self._progress_reporter(word, index_chain, len(hits))

        if not hits:
            return

        if hits[0] == word:
            self._solutions.add(word, index_chain)

        for neighbour in self._puzzle.neighbours_of(index_chain[-1]):
            if neighbour not in index_chain:
                self._attempt(
                    index_chain + [neighbour],
                    "".join([word, self._puzzle.letters[neighbour]]),
                )

    def _load_words(self, word_list_path: str) -> None:
        # this is a known issue with Python up to version 3.15 (in the future!)
        # pylint: disable=unspecified-encoding
        with rich.progress.open(word_list_path, "r") as words_file:
            for word in [
                w for w in words_file.read().splitlines() if self.interesting_word(w)
            ]:
                self.word_list_count += 1
                self._word_trie.insert(word)
        # pylint: enable=unspecified-encoding

    def interesting_word(self, word: str) -> bool:
        """Check if a word is interesting
        skip lines that are too long
        skip lines that don't start with a  letter from our puzzle
        skip lines with letters not in our puzzle
        """
        candidate_letters = self._puzzle.unique_letters
        return (
            len(word) <= self._puzzle.cell_count
            and word[0] in candidate_letters
            and word_only_contains_puzzle_letters(word, candidate_letters)
        )

    def word_count(self) -> int:
        """Pass the word count from our solutions object"""

        return self._solutions.word_count()

    def path_count(self) -> int:
        """Pass the number of paths for a given word from our solutions object"""

        return self._solutions.path_count()


def word_only_contains_puzzle_letters(word: str, letters: str) -> bool:
    """Check if a word contains only letters from a given set"""

    return not any(letter not in letters for letter in word)
