"""
A tab widget with lists of words of a particular length.
"""

from itertools import groupby

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListWidget, QScrollArea, QTabWidget


class WordListWidget(QListWidget):
    """
    Present list of words in the solution.
    """

    def __init__(self, words: list[str], target_for_word_change: callable):
        super().__init__()
        self.addItems(words)

        self.currentTextChanged.connect(target_for_word_change)


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

    Pass wortd selections up to the main window.
    """

    def __init__(self, words: list[str], current_text_changed: callable):
        super().__init__()

        self.setDocumentMode(True)

        for key, group in groupby(words, key=len):
            word_list_widget = WordListWidget(list(group), current_text_changed)
            scroller = SolutionsScroller(word_list_widget)
            self.addTab(scroller, f"{key}")
