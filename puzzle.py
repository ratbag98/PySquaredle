class Puzzle:
  def __init__(self, letters, sideLength):
    self.puzzle = letters
    self.size = sideLength


  def grid(self):
    grid = ''
    for y in range(self.size):
      start = self.idx(0, y)
      end = self.idx(self.size, y)
      grid = grid + self.puzzle[start:end] + "\n"
    return grid

  def idx(self, x, y):
    return x + (y*self.size)
