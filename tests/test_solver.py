"""
Test the Solver class
"""

import pytest

from pysquaredle.puzzle import Puzzle
from pysquaredle.solver import Solver

test_words = "test_word_list.txt"


@pytest.fixture
def good_puzzle() -> Puzzle:
    """Just a good puzzle"""
    return Puzzle("ABCDEFGHI")


@pytest.fixture
def anthropomorphize_puzzle() -> Puzzle:
    """A puzzle with the word ANTHROPOMORPHIZE in it"""
    return Puzzle("HTEZRONIOPAHMORP")


def test_puzzle_created(good_puzzle: Puzzle) -> None:
    """
    With a valid set of letters, create Solver without error
    """
    Solver(good_puzzle, word_list_path=test_words)


def test_word_list_count(good_puzzle: Puzzle) -> None:
    """
    Has the word list been filtered correctly
    """
    solver = Solver(good_puzzle, word_list_path=test_words)
    solver2 = Solver(Puzzle("ABCDEFGHIJKLMNOP"), word_list_path=test_words)

    assert solver.word_list_count == 3
    assert solver2.word_list_count == 109


def test_solution_includes_all_letter_word(anthropomorphize_puzzle: Puzzle) -> None:
    """
    Can we solve when the word is the same length as the letters? Bounds
    """
    solver = Solver(anthropomorphize_puzzle, word_list_path=test_words)

    assert "ANTHROPOMORPHIZE" in solver.raw_solution_words()


def test_solution_excludes_unlinked_words(anthropomorphize_puzzle: Puzzle) -> None:
    """
    Solution shouldn't include impossible words that can't be formed
    by tracing a continuous line.
    """
    solver = Solver(anthropomorphize_puzzle, word_list_path=test_words)

    assert "OPERA" not in solver.raw_solution_words()


def test_solution_excludes_repeat_visits(good_puzzle: Puzzle) -> None:
    """
    There should be no words that require repeated visit to same cell
    """
    solver = Solver(good_puzzle, word_list_path=test_words)
    assert "CEDE" not in solver.raw_solution_words()


def test_can_get_or_print_solutions_if_solve_called(good_puzzle: Puzzle) -> None:
    """
    Okay to request solutions when the solution has been found.
    """
    solver = Solver(good_puzzle, word_list_path=test_words)

    solutions = solver.raw_solution_words()

    assert len(solutions) > 0

    solver.formatted_solutions()
