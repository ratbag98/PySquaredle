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
parser.add_argument('-w','--word-list')
parser.add_argument('-s', '--sort', action='store_true')
parser.add_argument('-l','--length', action='store_true')
parser.add_argument('-g', '--grid', action='store_true')
parser.add_argument('-n', '--neighbours', action='store_true')
parser.add_argument('-d','--differentiate', action='store_true')

args = parser.parse_args()

letters = args.letters

sideLength = math.sqrt(len(letters))

# TODO move this into the class
if sideLength % 1 != 0:
  sys.exit('Length of letters must be a square number, eg 9, 16, 25, 36')

puzzle = Puzzle(letters, int(sideLength))

if args.grid:
  print(puzzle.grid())

if args.neighbours:
  print(puzzle.list_neighbours())

puzzle.solve()
puzzle.print_solutions(args.sort, args.length)
