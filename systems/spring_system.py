import random

from settings import *
from cell import create_cell
from simulation_utils import get_material


def update_springs(grid):

    for row in range(ROWS):

        for col in range(COLS):

            cell = grid[row][col]

            if cell == 0:
                continue

            if get_material(cell) != SPRING:
                continue

            # emit water upward

            if row > 0 and grid[row - 1][col] == 0:
                
                if random.random() < 0.05:
                    grid[row - 1][col] = create_cell(WATER)