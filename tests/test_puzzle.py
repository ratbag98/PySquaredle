"""
Test the Puzzle class
"""

from pysquaredle.puzzle import Puzzle


class TestPuzzle:
    """
    Operations on the Puzzle class
    """

    def test_grid_loaded_correctly(self):
        """
        Did reading the valid letters create a valid grid?
        """
        puzzle = Puzzle("ABCDEFGHI")
        assert puzzle.grid == "ABC\nDEF\nGHI\n"
