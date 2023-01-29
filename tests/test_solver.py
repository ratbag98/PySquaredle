"""
Test the Solver class
"""

import pytest

from pysquaredle.puzzle import Puzzle
from pysquaredle.solver import Solver


class TestSolver:
    """
    A Puzzle is a grid of letters, along with information about neighbours.
    Let's test it
    """

    good_letters = "ABCDEFGHI"
    test_words = "test_word_list.txt"

    @pytest.fixture
    def good_puzzle(self) -> Puzzle:
        """Just a good puzzle"""
        return Puzzle(self.good_letters)

    @pytest.fixture
    def anthropomorphize_puzzle(self) -> Puzzle:
        """A puzzle with the word ANTHROPOMORPHIZE in it"""
        return Puzzle("HTEZRONIOPAHMORP")

    def test_grid_must_be_square(self):
        """
        The number of letters must be a square number (eg 3x3, 4x4)
        """
        with pytest.raises(ValueError):
            Solver(Puzzle("ABC"), word_list_path=self.test_words)

    def test_grid_must_not_be_a_single_character(self):
        """
        The number of letters must be at least 2x2
        """
        with pytest.raises(ValueError):
            Solver(Puzzle("A"), word_list_path=self.test_words)

    def test_only_letters_are_valid_cells(self):
        """
        The cells in the puzzle must only be letters
        """
        with pytest.raises(ValueError):
            Solver(Puzzle("123456789"), word_list_path=self.test_words)

    def test_puzzle_created(self, good_puzzle: Puzzle):
        """
        With a valid set of letters, create Solver without error
        """
        Solver(good_puzzle, word_list_path=self.test_words)

    def test_word_list_count(self, good_puzzle: Puzzle):
        """
        Has the word list been filtered correctly
        """
        solver = Solver(good_puzzle, word_list_path=self.test_words)
        solver2 = Solver(Puzzle("ABCDEFGHIJKLMNOP"), word_list_path=self.test_words)

        assert solver.word_list_count == 3
        assert solver2.word_list_count == 109

    def test_solution_includes_all_letter_word(self, anthropomorphize_puzzle: Puzzle):
        """
        Can we solve when the word is the same length as the letters? Bounds
        """
        solver = Solver(anthropomorphize_puzzle, word_list_path=self.test_words)

        assert "ANTHROPOMORPHIZE" in solver.raw_solution_words()

    def test_solution_excludes_unlinked_words(self, anthropomorphize_puzzle: Puzzle):
        """
        Solution shouldn't include impossible words that can't be formed
        by tracing a continuous line.
        """
        solver = Solver(anthropomorphize_puzzle, word_list_path=self.test_words)

        assert "OPERA" not in solver.raw_solution_words()

    def test_solution_excludes_repeat_visits(self, good_puzzle: Puzzle):
        """
        There should be no words that require repeated visit to same cell
        """
        solver = Solver(good_puzzle, word_list_path=self.test_words)
        assert "CEDE" not in solver.raw_solution_words()

    def test_can_get_or_print_solutions_if_solve_called(self, good_puzzle: Puzzle):
        """
        Okay to request solutions when the solution has been found.
        """
        solver = Solver(good_puzzle, word_list_path=self.test_words)

        solutions = solver.raw_solution_words()

        assert len(solutions) > 0

        solver.formatted_solutions()
