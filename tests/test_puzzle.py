"""
Test the Puzzle class
"""

import pytest

from pysquaredle.puzzle import Puzzle


def test_grid_loaded_correctly() -> None:
    """
    Did reading the valid letters create a valid grid?
    """
    puzzle = Puzzle("ABCDEFGHI")
    assert puzzle.grid == "ABC\nDEF\nGHI\n"


def test_puzzle_must_be_square() -> None:
    """
    The puzzle must be square
    """
    with pytest.raises(ValueError):
        Puzzle("BADGRID")


def test_grid_must_not_be_a_single_character() -> None:
    """
    The number of letters must be at least 2x2
    """
    with pytest.raises(ValueError):
        Puzzle("A")


def test_only_letters_are_valid_cells() -> None:
    """
    The cells in the puzzle must only be letters
    """
    with pytest.raises(ValueError):
        Puzzle("1BCDEFGHI")
