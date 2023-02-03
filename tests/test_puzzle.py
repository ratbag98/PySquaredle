"""
Test the Puzzle class
"""

import pytest

from pysquaredle.puzzle import Puzzle


@pytest.fixture(name="good_puzzle")
def fixture_good_puzzle() -> Puzzle:
    """Just a good puzzle"""
    return Puzzle("ABCDEFGHI")


def test_grid_loaded_correctly(good_puzzle: Puzzle) -> None:
    """
    Did reading the valid letters create a valid grid?
    """
    assert good_puzzle.grid == "ABC\nDEF\nGHI\n"


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


def test_only_letters_and_underscore_are_valid_cells() -> None:
    """
    The cells in the puzzle must only be letters
    """
    with pytest.raises(ValueError):
        Puzzle("1BCDEFGHI")

    # underscore is valid
    Puzzle("ABCDEF_GH")


def test_puzzle_can_print_itself(good_puzzle: Puzzle) -> None:
    """
    Can the puzzle print itself?
    """
    assert str(good_puzzle) == "ABC\nDEF\nGHI\n"
    assert repr(good_puzzle) == 'Puzzle("ABCDEFGHI")'


def test_neighbours_of(good_puzzle: Puzzle) -> None:
    """
    Do we see the correct neighbours?
    """

    assert good_puzzle.neighbours_of(0) == [1, 3, 4]
    assert good_puzzle.neighbours_of(1) == [0, 2, 3, 4, 5]


def test_list_neighbours(good_puzzle: Puzzle) -> None:
    """
    Do we see the correct neighbours?
    """

    assert (
        good_puzzle.list_neighbours()
        == """1:3:4, 0:2:3:4:5, 1:4:5,
0:1:4:6:7, 0:1:2:3:5:6:7:8, 1:2:4:7:8,
3:4:7, 3:4:5:6:8, 4:5:7"""
    )
