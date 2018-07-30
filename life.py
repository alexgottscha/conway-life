import logging
import pygame
from random import random


class Grid:
    def __init__(self, width, height, populate=('random', 0.25), torus=True,
                 graphics=False, wsize={'x': 1280, 'y': 800}):
        self.torus = torus
        self.width = width
        self.height = height
        if populate[0] == 'random':
            self.grid = self.fill_grid_random(fill=populate[1])
        else:
            raise ValueError('populate parameter only supports "random"')

    def fill_grid_random(self, fill=0.25):
        logging.debug('filling grid randomly')
        return [[Cell(True, {'x': x, 'y': y}, self) if random() < fill else
                 Cell(False, {'x': x, 'y': y}, self)
                 for x in range(self.width)] for y in range(self.height)]

    def get_cell(self, coords):
        logging.debug(f'asked for cell at {coords}')
        if not self.torus:
            if coords['x'] < 0 or coords['x'] > (self.width + 1) or \
                    coords['y'] < 0 or coords['y'] > (self.height + 1):
                logging.debug('coords exceeded boundaries on non-torus grid')
                return None

        return self.grid[coords['y'] % self.height][coords['x'] % self.width]

    def print(self, debug=False):
        for row in self.grid:
            for cell in row:
                if debug:
                    cell._debug_print()
                else:
                    cell.print()
            print()

    def update(self):
        for row in self.grid:
            for cell in row:
                nn = cell.count_neighbors()
                if cell.state is Cell.alive:
                    if nn < 2 or nn > 3:
                        cell.next_state = Cell.dead
                    else:
                        cell.next_state = Cell.alive
                else:
                    if nn == 3:
                        cell.next_state = Cell.alive
                    else:
                        cell.next_state = Cell.dead
        for row in self.grid:
            for cell in row:
                cell.state = cell.next_state
                cell.next_state = None


class Cell:
    alive = True
    dead = False

    def __init__(self, state, coords, grid):
        self.state = state
        self.coords = coords
        self.grid = grid
        self.next_state = None

    def _debug_print(self):
        print((f"| y:{self.coords['y']} x:{self.coords['x']} "
               f"a:{self.state} n:{self.count_neighbors()}"), end='')

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
        logging.debug(f'neighborhood: {neighbor_coords}')
        count = 0
        for loc in neighbor_coords:
            if self.grid.get_cell(loc) is not None and \
                    self.grid.get_cell(loc).state is Cell.alive:
                count += 1
        return count

    def draw(self):
        pass

    def print(self):
        if self.state is Cell.alive:
            print('O', end='')
        else:
            print(' ', end='')


class Screen:
    def __init__(self, grid, cell_size):
        '''the width and height params are grid cells, not pixels'''
        self.grid = grid
        self.cell_size = cell_size
        self.res_width = grid.width * cell_size
        self.res_height = grid.height * cell_size
        self.size = (self.res_width, self.res_height)
        self.screen = pygame.display.set_mode(self.size)

    def draw(self):
        size = (self.cell_size, self.cell_size)
        for y, row in enumerate(self.grid.grid):
            for x, cell in enumerate(row):
                coords = (x*self.cell_size, y*self.cell_size)
                if cell.state is Cell.alive:
                    color = pygame.Color('white')
                else:
                    color = pygame.Color('black')
                self.screen.fill(color, rect=pygame.Rect(coords, size))
        pygame.display.update()
