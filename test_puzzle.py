import argparse

import pytest

from puzzle import NonSquarePuzzleException, Puzzle
from solver import NotSolvedYetException, Solver


class TestPuzzle:
    good_letters = "ABCDEFGHI"
    test_words = "test_word_list.txt"

    def test_grid_must_be_square(self):
        with pytest.raises(NonSquarePuzzleException):
            solver = Solver("ABC", word_list=self.test_words)

    def test_puzzle_created(self):
        solver = Solver(self.good_letters, word_list=self.test_words)
        pass

    def test_grid_loaded_correctly(self):
        solver = Solver(self.good_letters, word_list=self.test_words)
        assert solver.grid() == "ABC\nDEF\nGHI\n"

    def test_word_list_length(self):
        solver = Solver(self.good_letters, word_list=self.test_words)
        solver2 = Solver("ABCDEFGHIJKLMNOP", word_list=self.test_words)

        assert solver.word_list_length() == 1345
        assert solver2.word_list_length() == 2517

    def test_solution_includes_all_letter_word(self):
        solver = Solver("HTEZRONIOPAHMORP", word_list=self.test_words)
        solver.solve()

        assert "ANTHROPOMORPHIZE" in solver.raw_solutions()

    def test_solution_excludes_unlinked_words(self):
        solver = Solver("HTEZRONIOPAHMORP", word_list=self.test_words)
        solver.solve()

        assert not "OPERA" in solver.raw_solutions()

    def test_exception_if_solutions_requested_before_solve_called(self):
        solver = Solver("ABCD", word_list=self.test_words)

        with pytest.raises(NotSolvedYetException):
            solver.raw_solutions()

        with pytest.raises(NotSolvedYetException):
            solver.print_solutions({"sort": False})

    def test_can_get_or_print_solutions_if_solve_called(self):
        solver = Solver(self.good_letters, word_list=self.test_words)
        solver.solve()

        solutions = solver.raw_solutions()

        assert len(solutions) > 0

        solver.print_solutions(
            {
                "single_column": True,
                "length": True,
                "headers": False,
                "sort": True,
            }
        )
