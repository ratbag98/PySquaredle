"""
Solutions class. Stores and formats a list of words and solution paths for those words.
A solution path is the list of indexes in the puzzle grid that make up a word.
"""

from collections import defaultdict
from itertools import groupby

class Solutions:
    """
    Dictionary of unique words with path(s) to build them.
    """

    def __init__(self) -> None:
        self._solutions: dict[str, list[list[int]]] = defaultdict(list[list[int]])

    def add(self, word: str, path: list[int]) -> None:
        """
        Add a solution to the list of solutions.

        Adds a path to the list of paths for a given word
        """
        self._solutions[word].append(path)

    def words(self) -> list[str]:
        """
        Return a list of unique words in the solutions
        """
        return list(self._solutions.keys())

    def paths(self, word: str) -> list[list[int]]:
        """
        Return a list of paths for a given word
        """
        return self._solutions[word]

    def word_count(self) -> int:
        """Unique words in the solution"""
        return len(self._solutions)

    def path_count(self) -> int:
        """Total number of paths in the solutions"""
        return sum(len(paths) for paths in self._solutions.values())

    def formatted_solutions(
        self,
        alpha_sort: bool = False,
        length_group: bool = False,
        single_column: bool = False,
        headers: bool = False,
    ) -> str:
        """
        Return a formatted list of solutions, modified by any bool arguments:
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

        solutions: list[str] = self.words()
        if sort:
            solutions.sort()
        if length:
            solutions.sort(key=len)
        return solutions
