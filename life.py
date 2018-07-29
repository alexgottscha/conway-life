from random import random


class Grid:
    def __init__(self, width, height, populate=('random', 0.25), torus=True):
        self.torus = torus
        self.width = width
        self.height = height
        if populate[0] == 'random':
            self.grid = self.fill_grid_random(fill=populate[1])
        else:
            raise ValueError('populate parameter only supports "random"')

    def update(self):
        pass

    def fill_grid_random(self, fill=0.25):
        return [[Cell(True, {'x': x, 'y': y}, self) if random() < fill else
                 Cell(False, {'x': x, 'y': y}, self)
                 for x in range(self.width)] for y in range(self.height)]

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
        self.alive = state
        self.coords = coords
        self.grid = grid

    def __bool__(self):
        return self.alive

    def _debug_print(self):
        print((f"| y:{self.coords['y']} x:{self.coords['x']} "
               f"s:{self.alive} n:{self.count_neighbors()}"), end='')

    def print(self):
        if self:
            print('O', end='')
        else:
            print(' ', end='')

    def kill(self):
        self.alive = False

    def spawn(self):
        self.alive = True

    def count_neighbors(self):
        if not self.alive:
            return None
        if self.grid.torus:
            return self.count_neighbors_wrap()
        else:
            return self.count_neighbors_stop()

    def count_neighbors_wrap(self):
        count = 0
        for y in range((self.coords['y'] - 1) % self.grid.height,
                       (self.coords['y'] + 1) % self.grid.height):
            for x in range((self.coords['x'] - 1) % self.grid.width,
                           (self.coords['x'] + 1) % self.grid.width):
                # skip the center cell as it's self
                if y == 0 and x == 0:
                    continue
                if self.grid.grid[y][x]:
                    count += 1
        return count

    def count_neighbors_stop(self):
        pass
