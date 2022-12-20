from trie import Trie
import argparse

parser = argparse.ArgumentParser(
  prog = 'PySquaredle',
  description='Solves the Squaredle puzzle, as seen on https://squaredle.app',
  epilog = '(C) 2022 Robert Rainthorpe.'
)

parser.add_argument('letters')
parser.add_argument('-w','--word-list')
parser.add_argument('-s', '--sort', action='sort_alphabetically')
parser.add_argument('-l','--length', action='group_by_length')
parser.add_argument('-g', '--grid', action='display_grid')
parser.add_argument('-n', '--neighbours', action='display_neighbours')



argv = sys.argv[:1]








tr = Trie()

with open('word_list.txt') as wl:
  Lines = wl.readlines()
  for line in Lines:
    tr.insert(line.rstrip())
