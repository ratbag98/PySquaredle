import pytest
from PyQt6.QtWidgets import QMainWindow

from pysquaredle.solver import Solver
from ui.main_window import MainWindow

# from PyQt6 import QtCore


# def update_func(word: str, chain: list[int], hit_count: int) -> None:
#     pass


@pytest.fixture
def app(qtbot) -> MainWindow:
    solver = Solver(
        "ROBERTRAINTHORPE", "./test_word_list.txt"
    )  # , update_func=update_func)
    solver.solve()
    test_squaredle_app = MainWindow(solver, False, False)

    print("Got here")
    qtbot.addWidget(test_squaredle_app)

    return test_squaredle_app


def test_status(app: MainWindow):
    assert app.status_bar.currentMessage() == "3 unique words found, 12 total solutions"
