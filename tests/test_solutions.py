"""
Solution tests
"""

import pytest

from pysquaredle.puzzle import Puzzle
from pysquaredle.solutions import Solutions
from pysquaredle.solver import Solver

TEST_WORDS = "test_word_list.txt"


@pytest.fixture(name="good_solutions")
def fixture_good_solver() -> Solutions:
    """Just a good solver"""
    return Solver(Puzzle("UCHEMDRIAEHTRCGA"), word_list_path=TEST_WORDS).solutions


def test_solutions_contains_words(good_solutions: Solutions) -> None:
    """
    Does the solutions contain the words we expect?
    """

    assert "HIRER" in good_solutions.words()
    assert "HEAD" in good_solutions.words()


def test_solution_contains_paths(good_solutions: Solutions) -> None:
    """
    Does the solutions contain the paths we expect?
    """

    assert [2, 7, 6, 9, 12] in good_solutions.paths("HIRER")


def test_solution_paths_can_have_multiple_entries(good_solutions: Solutions) -> None:
    """
    Can a word have multiple paths?
    """
    assert [2, 7, 6, 9, 12] in good_solutions.paths("HIRER")


def test_solution_paths_is_a_list_for_single_path_words(
    good_solutions: Solutions,
) -> None:
    """
    If a word has only one path, is the path a list or a list of lists?
    """

    assert good_solutions.paths("HEAD") == [[10, 9, 8, 5]]


def test_formatted_solutions_contains_words(good_solutions: Solutions) -> None:
    """
    Does the formatted solutions contain the words we expect?
    """

    assert "HIRER" in good_solutions.formatted_solutions()
    assert "HEAD" in good_solutions.formatted_solutions()


def test_formatted_solutions_honours_alpha_sort(good_solutions: Solutions) -> None:
    """
    Does the formatted solutions honour the alpha sort?
    """
    assert good_solutions.formatted_solutions(alpha_sort=False) == "HIRER\tHEAD"
    assert good_solutions.formatted_solutions(alpha_sort=True) == "HEAD\tHIRER"


def test_formatted_solutions_honours_single_colulmn(good_solutions: Solutions) -> None:
    """
    Does the formatted solutions honour the single column?
    """
    assert good_solutions.formatted_solutions(single_column=False) == "HIRER\tHEAD"
    assert good_solutions.formatted_solutions(single_column=True) == "HIRER\nHEAD"


def test_formatted_solutions_honours_grouping(good_solutions: Solutions) -> None:
    """
    Does the formatted solutions honour the grouping?
    """
    assert (
        good_solutions.formatted_solutions(length_group=False, headers=True)
        == "HIRER\tHEAD"
    )
    assert (
        good_solutions.formatted_solutions(length_group=False, headers=False)
        == "HIRER\tHEAD"
    )

    assert "4 letter words" in good_solutions.formatted_solutions(
        length_group=True, headers=True
    )
    assert "5 letter words" in good_solutions.formatted_solutions(
        length_group=True, headers=True
    )

    assert (
        good_solutions.formatted_solutions(length_group=True, headers=False)
        == "HEAD\tHIRER\t"
    )


# TODO test more combinations of options?
