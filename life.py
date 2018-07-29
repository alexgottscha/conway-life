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

    def get_cell(self, coords):
        if not self.torus:
            if coords['x'] < 0 or coords['x'] > (self.width + 1) or \
                    coords['y'] < 0 or coords['y'] > (self.height + 1):
                return None

        return self.grid[coords['y'] % self.height][coords['x'] % self.width]

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
        top = self.coords['y'] - 1
        middle_y = self.coords['y']
        bottom = self.coords['y'] + 1
        left = self.coords['x'] - 1
        middle_x = self.coords['x']
        right = self.coords['x'] + 1
        neighbor_coords = [{'y': top, 'x': left},
                           {'y': top, 'x': middle_x},
                           {'y': top, 'x': right},
                           {'y': middle_y, 'x': left},
                           {'y': middle_y, 'x': right},
                           {'y': bottom, 'x': left},
                           {'y': bottom, 'x': middle_x},
                           {'y': bottom, 'x': right}]
        count = 0
        for loc in neighbor_coords:
            if self.grid.get_cell(loc) is not None and \
                    self.grid.get_cell(loc).alive:
                count += 1
        return count
