"""Solutions class. A list of words and solution paths for those words.

A solution path is the list of indexes in the puzzle grid that make up a word.
"""

from collections import defaultdict
from itertools import groupby
from pathlib import Path

UNACCEPTABLE_WORDS = "./unacceptable.txt"


class Solutions:
    """Dictionary of unique words with path(s) to build them."""

    def __init__(self) -> None:
        """Create empty solution."""
        self._solutions: dict[str, list[list[int]]] = defaultdict(list[list[int]])
        self._unacceptable_words: list[str]
        self.load_unacceptable_words()

    def add(self, word: str, path: list[int]) -> None:
        """Add a solution path to the list of solutions."""
        self._solutions[word].append(path)

    def words(self) -> list[str]:
        """Return a list of unique words in the solutions."""
        return list(self._solutions.keys())

    def paths(self, word: str) -> list[list[int]]:
        """Return a list of paths for a given word."""
        return self._solutions[word]

    def word_count(self) -> int:
        """Unique words in the solution."""
        return len(self._solutions)

    def path_count(self) -> int:
        """Total number of paths in the solutions."""
        return sum(len(paths) for paths in self._solutions.values())

    def unacceptable_solutions(self) -> list[str]:
        """Return list of unacceptable words found in the puzzle solutions."""
        return [
            u
            for u in self._solutions.keys()  # noqa: SIM118
            if u in self._unacceptable_words
        ]

    def load_unacceptable_words(self) -> None:
        """Read a list of dodgy words to test against the solutions_list."""
        try:
            with Path(UNACCEPTABLE_WORDS).open(encoding="utf-8") as unacceptable:
                self._unacceptable_words = unacceptable.read().split("\n")
        except FileNotFoundError:
            self._unacceptable_words = []

    def formatted_solutions(
        self,
        *,
        alpha_sort: bool = False,
        length_group: bool = False,
        single_column: bool = False,
        headers: bool = False,
    ) -> str:
        """Return a formatted list of solutions.

        Args:
            alpha_sort (bool):    alphabetically sort the solutions
            length_group (bool):  group solutions by word length
            single_column (bool): present results as a single column
            headers (bool):       show group headers (grouping must be enabled)

        Returns:
            str: a formatted list of solutions suitable for printing

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

    def raw_solution_words(self, *, sort: bool, length: bool) -> list[str]:
        """Convert solutions set into list, honoring sort flag."""
        solutions: list[str] = self.words()
        if sort:
            solutions.sort()
        if length:
            solutions.sort(key=len)
        return solutions
