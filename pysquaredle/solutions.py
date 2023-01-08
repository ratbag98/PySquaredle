"""
Solutions class
"""

from collections import defaultdict


class Solutions:
    """
    Dictionary of unique words with path(s) to build them.
    """

    def __init__(self) -> None:
        self.solutions: dict[str, list[list[int]]] = defaultdict(list[list[int]])

    def add(self, word: str, path: list[int]) -> None:
        """
        Add a solution to the list of solutions.

        Adds a path to the list of paths for a given word
        """
        self.solutions[word].append(path)

    def words(self) -> list[str]:
        """
        Return a list of words in the solutions
        """
        return list(self.solutions.keys())

    def paths(self, word: str) -> list[list[int]]:
        """
        Return a list of paths for a given word
        """
        return self.solutions[word]
