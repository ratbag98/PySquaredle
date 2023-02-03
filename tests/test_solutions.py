"""
Solution tests
"""

import pytest

from pysquaredle.puzzle import Puzzle
from pysquaredle.solver import Solver

TEST_WORDS = "test_word_list.txt"


@pytest.fixture(name="good_solver")
def fixture_good_solver() -> Solver:
    """Just a good solver"""
    return Solver(Puzzle("UCHEMDRIAEHTRCGA"), word_list_path=TEST_WORDS)


def test_solutions_contains_words(good_solver: Solver) -> None:
    """
    Does the solutions contain the words we expect?
    """
    solutions = good_solver.solutions

    assert "HIRER" in solutions.words()
    assert "HEAD" in solutions.words()


def test_solution_contains_paths(good_solver: Solver) -> None:
    """
    Does the solutions contain the paths we expect?
    """
    solutions = good_solver.solutions

    assert [2, 7, 6, 9, 12] in solutions.paths("HIRER")


def test_solution_paths_can_have_multiple_entries(good_solver: Solver) -> None:
    """
    Can a word have multiple paths?
    """
    solutions = good_solver.solutions

    assert [2, 7, 6, 9, 12] in solutions.paths("HIRER")


def test_solution_paths_is_a_list_for_single_path_words(good_solver: Solver) -> None:
    """
    If a word has only one path, is the path a list or a list of lists?
    """
    solutions = good_solver.solutions

    assert solutions.paths("HEAD") == [[10, 9, 8, 5]]
