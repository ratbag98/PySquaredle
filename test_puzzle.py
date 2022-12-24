import argparse

import pytest

from puzzle import NonSquarePuzzleException, NotSolvedYetException, Puzzle


class TestPuzzle:
    good_letters = "ABCDEFGHI"
    test_words = "test_word_list.txt"

    def test_grid_must_be_square(self):
        with pytest.raises(NonSquarePuzzleException):
            puzzle = Puzzle("ABC", word_list=self.test_words)

    def test_puzzle_created(self):
        puzzle = Puzzle(self.good_letters, word_list=self.test_words)
        pass

    def test_grid_loaded_correctly(self):
        puzzle = Puzzle(self.good_letters, word_list=self.test_words)
        assert puzzle.grid() == "ABC\nDEF\nGHI\n"

    def test_word_list_length(self):
        puzzle = Puzzle(self.good_letters, word_list=self.test_words)
        puzzle2 = Puzzle("ABCDEFGHIJKLMNOP", word_list=self.test_words)

        assert puzzle.word_list_length() == 1345
        assert puzzle2.word_list_length() == 2517

    def test_solution_includes_all_letter_word(self):
        puzzle = Puzzle("HTEZRONIOPAHMORP", word_list=self.test_words)
        puzzle.solve()

        assert "ANTHROPOMORPHIZE" in puzzle.raw_solutions()

    def test_solution_excludes_unlinked_words(self):
        puzzle = Puzzle("HTEZRONIOPAHMORP", word_list=self.test_words)
        puzzle.solve()

        assert not "OPERA" in puzzle.raw_solutions()

    def test_exception_if_solutions_requested_before_solve_called(self):
        puzzle = Puzzle("ABCD", word_list=self.test_words)

        with pytest.raises(NotSolvedYetException):
            puzzle.raw_solutions()

        with pytest.raises(NotSolvedYetException):
            puzzle.print_solutions({"sort": False})

    def test_can_get_or_print_solutions_if_solve_called(self):
        puzzle = Puzzle(self.good_letters, word_list=self.test_words)
        puzzle.solve()

        solutions = puzzle.raw_solutions()

        assert len(solutions) > 0

        puzzle.print_solutions(
            {
                "single_column": True,
                "length": True,
                "headers": False,
                "sort": True,
            }
        )
