from random import random



class Grid:
    def __init__(self, width, height, fill=0.25, torus=False):
        self.torus = torus
        self.grid = [[
            Cell(True, {'x': x, 'y': y}, self) if random() < fill else
            Cell(False, {'x': x, 'y': y}, self)
            for x in range(width)] for y in range(height)]

    def update(self):
        pass

    def print(self, debug=False):
        for row in self.grid:
            for cell in row:
                if debug:
                    cell._debug_print()
                else:
                    cell.print()
            print('|')


class Cell:
    def __init__(self, state, coords, grid):
        self.state = state
        self.coords = coords
        self.grid = grid

    def __bool__(self):
        return self.state

    def _debug_print(self):
        print((f"| y:{self.coords['y']} x:{self.coords['x']} "
               f"s:{self.state} n:{self.count_neighbors()}"), end='')

    def print(self):
        if self:
            print('O', end='')
        else:
            print(' ', end='')

    def kill(self):
        self.state = False

    def spawn(self):
        self.state = True

    def count_neighbors(self):
        count = 0
        for y in range(self.coords['y'] - 1, self.coords['y'] + 1):
            for x in range(self.coords['x'] - 1, self.coords['x'] + 1):
                if y == 0 and x == 0:
                    continue
                if self.grid[y][x]:
                     count += 1
         return count

