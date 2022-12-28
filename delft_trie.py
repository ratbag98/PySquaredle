class Node:
    def __init__(self):
        self.children = []
        for i in range(26):
            self.children.append(None)
        self.isLeafNode = False


class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, input_str):
        strLen = len(input_str)
        crawler = self.root
        for level in range(strLen):
            character = input_str[level]
            position = ord(character) - ord("A")
            if crawler.children[position] is None:
                crawler.children[position] = Node()
            crawler = crawler.children[position]
        crawler.isLeafNode = True

    def search(self, input_str):
        crawler = self.root
        strLen = len(input_str)
        for level in range(strLen):
            character = input_str[level]
            position = ord(character) - ord("A")
            if crawler.children[position] is None:
                return False
            crawler = crawler.children[position]
        return crawler.isLeafNode
