from trie import Trie
import argparse
import math
import sys
from puzzle import Puzzle

parser = argparse.ArgumentParser(
  prog = 'PySquaredle',
  description='Solves the Squaredle puzzle, as seen on https://squaredle.app',
  epilog = '(C) 2022 Robert Rainthorpe.'
)

parser.add_argument('letters')
#parser.add_argument('-d','--differentiate', action='store_true')
parser.add_argument('-c','--single-column',action='store_true')
parser.add_argument('-g', '--grid', action='store_true')
parser.add_argument('-l','--length', action='store_true')
parser.add_argument('-n', '--neighbours', action='store_true')
parser.add_argument('-N','--no-headers', dest="headers", action='store_true')
parser.add_argument('-s', '--sort', action='store_true')
parser.add_argument('-w','--word-list')

args = parser.parse_args()

try:
  puzzle = Puzzle(args.letters)
except Exception as e:
  print("Couldn't create puzzle:",e)
  sys.exit(-1)

if args.grid:
  print(puzzle.grid())

if args.neighbours:
  print(puzzle.list_neighbours())

puzzle.solve()
puzzle.print_solutions(args)
