"""
Test the GUI
"""

import platform

import pytest

from pysquaredle.puzzle import Puzzle
from pysquaredle.solver import Solver

if platform.processor() == "aarch64":
    pytest.skip("Skipping UI tests on ARM", allow_module_level=True)
else:
    from pysquaredle.ui.main_window import MainWindow


@pytest.fixture(name="main_window")
def fixture_main_window(qtbot) -> MainWindow:
    """
    Test fixture for the main window
    """
    puzzle = Puzzle("TESTPUZZLEABCDEF")
    solver = Solver(puzzle, "./test_word_list.txt")
    test_squaredle_app = MainWindow(puzzle, solver, False, False)

    qtbot.add_widget(test_squaredle_app)

    return test_squaredle_app


def test_status(main_window: MainWindow) -> None:
    """
    The GUI is connected to the solver and updates the status bar
    """
    assert (
        main_window.status_bar.currentMessage()
        == "3 unique words found, 4 total solutions"
    )
