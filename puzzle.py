from trie import Trie
from itertools import groupby
import sys

# represent and solve a Squaredle puzzle (httos://squaredle.app)
# a bunch of letters
# a list of neighbours for each cell in a grid
# a word list stored as a trie for speedy starts with searches
# a recursive chain builder to find solutions in the grid

class Puzzle:
  def __init__(self, letters, sideLength):
    self.puzzle = str.upper(letters)
    self.size = sideLength
    self.neighbours = []
    self.tr = Trie()
    self.solutions = set()
    self.solution_generated = False

    self.__calculate_neighbours()
    self.__load_words()


  def grid(self):
    grid = ''
    for y in range(self.size):
      start = self.__idx(0, y)
      end = self.__idx(self.size, y)
      grid = grid + self.puzzle[start:end] + "\n"
    return grid

  def list_neighbours(self):
    neighbourhood = ""
    for y in range(self.size):
      for x in range(self.size):
        neighbourhood += str.join(":", [str(elem) for elem in self.neighbours[self.__idx(x,y)]]) + ", "
      neighbourhood += '\n'
    return neighbourhood

  def __idx(self, x, y):
    return x + (y*self.size)

  def __valid_neighbour(self, ox, oy, dx, dy):
    valid = (ox + dx) in range(0,self.size) and (oy + dy) in range(0,self.size) and not (dx ==0 and dy==0)
    return valid

  def __calculate_neighbours(self):
    for n in range(len(self.puzzle)):
      self.neighbours.append([])

    for oy in range(self.size):
      for ox in range(self.size):
        for dy in range(-1,2):
          for dx in range(-1,2):
            if self.__valid_neighbour(ox, oy, dx, dy):
              self.neighbours[self.__idx(ox,oy)].append(self.__idx(ox+dx, oy+dy))

  def __load_words(self):
    with open('word_list.txt') as wl:
      Lines = wl.readlines()
      for l in [str.upper(line.rstrip()) for line in Lines]:
        if len(l) <= self.size * self.size:
          self.tr.insert(l)

  def solve(self):
    for index in range(len(self.puzzle)):
      chain = [index]
      self.__check_letter_chains(chain)

    self.solution_generated = True

  def print_solutions(self, sort_alpha, group_length):
    solutions_list = list(self.solutions)

    if sort_alpha:
      solutions_list.sort()
    # if group_length:
    #   grouped = [list(i) for j,i in groupby(solutions_list,
    #                                         lambda a: len(a))]
    #   print(str(grouped))
    # else:
    print(str.join("\n", solutions_list))



  def __check_letter_chains(self, chain):

    cell_index = chain[-1]

    for neighbour_index in self.neighbours[cell_index]:

      # only one visit to a cell per chain
      if neighbour_index in chain:
        continue

      next_chain = chain.copy()
      next_chain.append(neighbour_index)

      # print(str.join(":", [str(index) for index in next_chain]))

      candidate = self.__word_from_chain(next_chain)

      hits = self.tr.search(candidate)

      if len(hits) >0:
        if hits[0] == candidate:
          self.solutions.add(candidate)

        self.__check_letter_chains(next_chain)

  def __word_from_chain(self, chain):
    word = ""
    for index in chain:
      word += self.puzzle[index]

    return word
