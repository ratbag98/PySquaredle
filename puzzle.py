from trie import Trie

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


    self.__calculateNeighbours()
    self.__loadWords()


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

  def __validNeighbour(self, ox, oy, dx, dy):
    valid = (ox + dx) in range(0,self.size) and (oy + dy) in range(0,self.size) and not (dx ==0 and dy==0)
    return valid

  def __calculateNeighbours(self):
    for n in range(len(self.puzzle)):
      self.neighbours.append([])

    for oy in range(self.size):
      for ox in range(self.size):
        for dy in range(-1,2):
          for dx in range(-1,2):
            if self.__validNeighbour(ox, oy, dx, dy):
              self.neighbours[self.__idx(ox,oy)].append(self.__idx(ox+dx, oy+dy))

  def __loadWords(self):
    with open('word_list.txt') as wl:
      Lines = wl.readlines()
      for line in Lines:
        if len(line) < self.size * self.size:
          self.tr.insert(str.upper(line.rstrip()))
