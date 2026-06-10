import random

from settings import *
from cell import create_cell
from simulation_utils import get_material


def update_moss(grid, update):

    for row in range(ROWS):

        for col in range(COLS):

            if (row, col) in update:
                continue

            cell = grid[row][col]

            if cell == 0:
                continue

            material = get_material(cell)

            # moss grows on stone and sand

            if material not in [STONE, SAND]:
                continue

            # required wetness

            if "wetness" not in cell:
                continue

            wetness = cell["wetness"]

            if wetness < 40:
                continue

            # surface exposeure check 

            exposed = False

            for dx, dy in [(0, -1), (-1, 0), (1, 0)]:

                nx = col + dx
                ny = row + dy

                if 0 <= nx < COLS and 0 <= ny < ROWS:

                    if grid[ny][nx] == 0:
                        exposed = True
                        break

            if not exposed:
                continue

            # slow moss growth

            if random.random() < 0.0005:

                grid[row][col] = create_cell(MOSS)
                update.add((row, col))

