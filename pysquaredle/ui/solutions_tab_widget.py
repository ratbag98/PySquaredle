"""
A tab widget with lists of words of a particular length.
"""

from itertools import groupby
from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListWidget, QScrollArea, QSizePolicy, QTabWidget


class WordListWidget(QListWidget):
    """
    Present list of words in the solution.
    """

    def __init__(self, words: list[str], target_for_word_change: Callable[[str], None]):
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

    Takes list of words ordered by length/name. Creates a tab for each length.

    Pass word selections up to the main window via current_text_changed.
    """

    def __init__(
        self, words: list[str], current_text_changed: Callable[[str], None]
    ) -> None:
        super().__init__()

        self.setDocumentMode(True)
        policy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        self.setSizePolicy(policy)

        # word length is the key
        self.scrollers: dict[int, tuple[SolutionsScroller, WordListWidget]] = {}

        for key, group in groupby(words, key=len):
            if not key in self.scrollers:
                word_list_widget = WordListWidget(list(group), current_text_changed)
                scroller = SolutionsScroller(word_list_widget)
                self.scrollers[key] = (scroller, word_list_widget)
                self.addTab(scroller, f"{key}")
            else:
                word_list_widget = self.scrollers[key][1]
                word_list_widget.addItems(list(group))


# so now we can look up a scroller and if needs be create one
# we'll search for the next scroller in the TabWidget and get its
# index, then insert a new one there.
