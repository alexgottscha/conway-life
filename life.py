import logging
import pygame
from random import random


class Grid:
    def __init__(self, columns, rows, populate=('random', 0.25), torus=True):
        self.torus = torus
        self.columns = columns
        self.rows = rows
        if populate[0] == 'random':
            self.grid = self.fill_grid_random(fill=populate[1])
        else:
            raise ValueError('populate parameter only supports "random"')

    def fill_grid_random(self, fill=0.25):
        logging.debug('filling grid randomly')
        return [[Cell(Cell.alive, {'col': col, 'row': row}, self)
                 if random() < fill else
                 Cell(Cell.dead, {'col': col, 'row': row}, self)
                 for col in range(self.columns)] for row in range(self.rows)]

    def get_cell(self, coords):
        logging.debug(f'asked for cell at {coords}')
        if not self.torus:
            if coords['col'] < 0 or coords['col'] > (self.columns + 1) or \
                    coords['row'] < 0 or coords['row'] > (self.rows + 1):
                logging.debug('coords exceeded boundaries on non-torus grid')
                return None

        return self.grid[coords['row'] % self.rows][coords['col'] % self.columns]

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
        print((f"| y:{self.coords['row']} x:{self.coords['col']} "
               f"a:{self.state} n:{self.count_neighbors()}"), end='')

    def count_neighbors(self):
        top_row = (self.coords['row'] - 1) % self.grid.rows
        middle_row = self.coords['row']
        bottom_row = (self.coords['row'] + 1) % self.grid.rows
        left_col = (self.coords['col'] - 1) % self.grid.columns
        middle_col = self.coords['col']
        right_col = (self.coords['col'] + 1) % self.grid.columns
        neighbors = [self.grid.grid[top_row][left_col],
                      self.grid.grid[top_row][middle_col],
                      self.grid.grid[top_row][right_col],
                      self.grid.grid[middle_row][left_col],
                      self.grid.grid[middle_row][right_col],
                      self.grid.grid[bottom_row][left_col],
                      self.grid.grid[bottom_row][middle_col],
                      self.grid.grid[bottom_row][right_col]]
        logging.debug(f'neighborhood: {neighbors}')
        count = 0
        for cell in neighbors:
            if cell.state is Cell.alive:
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
        self.res_width = grid.columns * cell_size
        self.res_height = grid.rows * cell_size
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
