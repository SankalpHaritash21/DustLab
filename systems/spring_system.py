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
                
                flow_chance = 0.01

                # strong if groundwater nearby

                for dx in range( -3, 4):
                    for dy in range( -3, 4):

                        nx, ny = col + dx, row + dy

                        if not (0 <= nx < COLS and 0 <= ny < ROWS):
                            continue

                        neighbor = grid[ny][nx]

                        if neighbor == 0:
                            continue

                        if "wetness" in neighbor:

                            flow_chance += neighbor["wetness"] / 10000
                
                flow_chance = min(flow_chance, 0.08)
                if random.random() < flow_chance:
                    grid[row - 1][col] = create_cell(WATER)
