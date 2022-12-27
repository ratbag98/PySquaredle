"""
Trie https://en.wikipedia.org/wiki/Trie

Classes
    TrieNode
    Trie
"""

# self-referential TrieNode type declaration needs this for 3.10
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TrieNode:
    """
    The basic unit stored in the Trie - a char
    """

    char: str
    children: dict[str, TrieNode] = field(default_factory=dict)
    is_end: bool = False


class Trie:
    """
    A trie structure. Each node contains a letter and a dictionary of children.

    Words can be loaded into the structure and retrieved by navigating the
    tree. In this way speedy starts with searches can be performed
    """

    def __init__(self):
        self.root = TrieNode("")

    def insert(self, word: str):
        """
        Add a word to the Trie by decomposing and navigating the existing
        trie, adding letters as new nodes or children of existing nodes
        """
        # start from top of trie
        node = self.root

        for char in word:
            if char in node.children:
                # down the trie we go, still matching
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        # just added a complete word so flag that in the trie
        node.is_end = True

    def dfs(self, output: list[str], node: TrieNode, pre: str):
        """
        Depth-first search of the Trie. Down we go to find the prefix
        """
        if node.is_end:
            output.append((pre + node.char))

        for child in node.children.values():
            self.dfs(output, child, pre + node.char)

    def search(self, target: str) -> list[str]:
        """
        Attempt to find a prefix string in the Trie
        """
        node = self.root
        for char in target:
            if char in node.children:
                node = node.children[char]
            else:
                return []
        output: list[str] = []
        self.dfs(output, node, target[:-1])

        return output
