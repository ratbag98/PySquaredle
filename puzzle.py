class Puzzle:
  def __init__(self, letters, sideLength):
    self.puzzle = letters
    self.size = sideLength
    self.neighbours = []
    for n in range(len(self.puzzle)):
      self.neighbours.append([])
    self.calculateNeighbours()


  def grid(self):
    grid = ''
    for y in range(self.size):
      start = self.idx(0, y)
      end = self.idx(self.size, y)
      grid = grid + self.puzzle[start:end] + "\n"
    return grid

  def list_neighbours(self):
    neighbourhood = ""
    for y in range(self.size):
      for x in range(self.size):
        neighbourhood += str.join(":", [str(elem) for elem in self.neighbours[self.idx(x,y)]]) + ", "
      neighbourhood += '\n'
    return neighbourhood

  def idx(self, x, y):
    return x + (y*self.size)

  def validNeighbour(self, ox, oy, dx, dy):
    valid = (ox + dx) in range(0,self.size) and (oy + dy) in range(0,self.size) and not (dx ==0 and dy==0)
    return valid

  def calculateNeighbours(self):
    for oy in range(self.size):
      for ox in range(self.size):
        for dy in range(-1,2):
          for dx in range(-1,2):
            if self.validNeighbour(ox, oy, dx, dy):
              self.neighbours[self.idx(ox,oy)].append(self.idx(ox+dx, oy+dy))
