import pytest
from puzzle import Puzzle


class TestPuzzle:
    good_letters = "ABCDEFGHI"
    test_words= 'test_word_list.txt'

    def test_grid_must_be_square(self):
        with pytest.raises(Exception):
            puzzle = Puzzle("ABC", word_list=self.test_words)

    def test_puzzle_created(self):
        puzzle = Puzzle(self.good_letters)
        pass

    def test_grid_loaded_correctly(self):
        puzzle = Puzzle(self.good_letters, word_list=self.test_words)
        assert puzzle.grid() == "ABC\nDEF\nGHI\n"

    def test_word_list_length(self):
        puzzle = Puzzle(self.good_letters, word_list=self.test_words)
        puzzle2 = Puzzle("ABCDEFGHIJKLMNOP", word_list=self.test_words)

        assert puzzle.word_list_length() == 1345
        assert puzzle2.word_list_length() == 2519
