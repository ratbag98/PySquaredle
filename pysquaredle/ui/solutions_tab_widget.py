"""A tab widget with lists of words of a particular length."""

from collections.abc import Callable
from itertools import groupby

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListWidget, QScrollArea, QSizePolicy, QTabWidget


class WordListWidget(QListWidget):
    """Present list of words in the solution."""

    def __init__(self, words: list[str], target_for_word_change: Callable[[str], None]):
        """Create a GUI list of clickable words."""
        super().__init__()
        self.addItems(words)

        self.currentTextChanged.connect(target_for_word_change)


class SolutionsScroller(QScrollArea):
    """Scroller for solutions."""

    def __init__(self, word_list_widget: WordListWidget):
        """Create a scrolling container for a word list."""
        super().__init__()

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.setWidget(word_list_widget)


class SolutionsTabWidget(QTabWidget):
    """Tab widget to show solutions.

    Takes list of words ordered by length/name. Creates a tab for each length.

    Pass word selections up to the main window via current_text_changed.
    """

    def __init__(
        self, words: list[str], current_text_changed: Callable[[str], None]
    ) -> None:
        """Create a tabbed widget to contain the scrolling lists of words."""
        super().__init__()

        self.setDocumentMode(True)
        policy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        self.setSizePolicy(policy)

        # word length is the key
        self.scrollers: dict[int, tuple[SolutionsScroller, WordListWidget]] = {}

        for key, group in groupby(words, key=len):
            if key not in self.scrollers:
                word_list_widget = WordListWidget(list(group), current_text_changed)
                scroller = SolutionsScroller(word_list_widget)
                self.scrollers[key] = (scroller, word_list_widget)
                self.addTab(scroller, f"{key}")
            else:
                word_list_widget = self.scrollers[key][1]
                word_list_widget.addItems(list(group))
