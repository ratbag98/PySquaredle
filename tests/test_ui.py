"""
Test the GUI
"""

import pytest

from pysquaredle.solver import Solver
from ui.main_window import MainWindow


@pytest.fixture
def app_fixture(qtbot) -> MainWindow:
    """
    Test fixture for the main window
    """
    solver = Solver("TESTPUZZLEABCDEF", "./test_word_list.txt")
    test_squaredle_app = MainWindow(solver, False, False)

    print("Got here")
    qtbot.add_widget(test_squaredle_app)

    return test_squaredle_app


# pylint: disable=redefined-outer-name
def test_status(app_fixture: MainWindow) -> None:
    """
    The GUI is connected to the solver and updates the status bar
    """
    assert (
        app_fixture.status_bar.currentMessage()
        == "3 unique words found, 4 total solutions"
    )
