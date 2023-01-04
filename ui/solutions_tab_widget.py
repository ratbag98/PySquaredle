"""
A tab widget with lists of words of a particular length.
"""

from itertools import groupby

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QScrollArea, QTabWidget, QVBoxLayout, QWidget


class WordListWidget(QWidget):
    """
    Present list of words in the solution.
    """

    def __init__(self, words: list[str]):
        super().__init__()
        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignTop)

        for word in words:
            label = QLabel(word)
            self.vbox.addWidget(label)

        self.setLayout(self.vbox)


class SolutionsScroller(QScrollArea):
    """
    Scroller for solutions.
    """

    def __init__(self, word_list_widget: WordListWidget):
        super().__init__()

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.setWidget(word_list_widget)


class SolutionsTabWidget(QTabWidget):
    """
    Tab widget to show solutions.
    """

    def __init__(self, words: list[str]):
        super().__init__()

        for key, group in groupby(words, key=len):
            word_list_widget = WordListWidget(list(group))
            scroller = SolutionsScroller(word_list_widget)
            self.addTab(scroller, f"{key}")
