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

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()
            print()


class Cell:
    def __init__(self, state, coords, grid):
        self.state = state
        self.coords = coords
        self.grid = grid

    def __bool__(self):
        return self.state

    def draw(self):
        if self:
            print('O', end='')
        else:
            print(' ', end='')

    def kill(self):
        self.state = False

    def spawn(self):
        self.state = True

    def count_neighbors(self):
        pass
