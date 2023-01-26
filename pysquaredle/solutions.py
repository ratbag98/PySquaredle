"""
Solutions class
"""

from collections import defaultdict


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
