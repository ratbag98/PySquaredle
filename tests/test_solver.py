"""
Test the Solver class
"""

from unittest.mock import Mock

import pytest

from pysquaredle.puzzle import Puzzle
from pysquaredle.solver import Solver

TEST_WORDS = "test_word_list.txt"


@pytest.fixture(name="good_puzzle")
def fixture_good_puzzle() -> Puzzle:
    """Just a good puzzle"""
    return Puzzle("ABCDEFGHI")


@pytest.fixture(name="anthropomorphize_puzzle")
def fixture_anthropomorphize_puzzle() -> Puzzle:
    """A puzzle with the word ANTHROPOMORPHIZE in it"""
    return Puzzle("HTEZRONIOPAHMORP")


def test_puzzle_created(good_puzzle: Puzzle) -> None:
    """
    With a valid set of letters, create Solver without error
    """
    Solver(good_puzzle, word_list_path=TEST_WORDS)


def test_word_list_count(good_puzzle: Puzzle) -> None:
    """
    Has the word list been filtered correctly
    """
    solver = Solver(good_puzzle, word_list_path=TEST_WORDS)
    solver2 = Solver(Puzzle("ABCDEFGHIJKLMNOP"), word_list_path=TEST_WORDS)

    assert solver.word_list_count == 3
    assert solver2.word_list_count == 109


def test_solution_includes_all_letter_word(
        anthropomorphize_puzzle: Puzzle) -> None:
    """
    Can we solve when the word is the same length as the letters? Bounds
    """
    solver = Solver(anthropomorphize_puzzle, word_list_path=TEST_WORDS)

    assert "ANTHROPOMORPHIZE" in solver.raw_solution_words()


def test_solution_excludes_unlinked_words(
        anthropomorphize_puzzle: Puzzle) -> None:
    """
    Solution shouldn't include impossible words that can't be formed
    by tracing a continuous line.
    """
    solver = Solver(anthropomorphize_puzzle, word_list_path=TEST_WORDS)

    assert "OPERA" not in solver.raw_solution_words()


def test_solution_excludes_repeat_visits(good_puzzle: Puzzle) -> None:
    """
    There should be no words that require repeated visit to same cell
    """
    solver = Solver(good_puzzle, word_list_path=TEST_WORDS)
    assert "CEDE" not in solver.raw_solution_words()


def test_can_get_or_print_solutions_if_solve_called(
        good_puzzle: Puzzle) -> None:
    """
    Okay to request solutions when the solution has been found.
    """
    solver = Solver(good_puzzle, word_list_path=TEST_WORDS)

    solutions = solver.raw_solution_words()

    assert len(solutions) > 0

    solver.formatted_solutions()


def test_solutions_are_generated_as_part_of_creation(
        good_puzzle: Puzzle) -> None:
    """
    The solutions should be generated as part of the creation of the Solver
    """
    solver = Solver(good_puzzle, word_list_path=TEST_WORDS)
    assert solver.solutions


def test_progress_reporter_is_called(good_puzzle: Puzzle) -> None:
    """
    The progress reporter should be called
    """
    update_func = Mock()

    Solver(good_puzzle, word_list_path=TEST_WORDS, update_func=update_func)
    assert update_func.called
