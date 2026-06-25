from settings import *
from simulation_utils import get_material
import random
from cell import create_cell

def update_wetness(grid):

    for row in range(ROWS):

        for col in range(COLS):

            cell = grid[row][col]

            if cell == 0:
                continue

            # only cell with wetness metadate
            if "wetness" not in cell:
                continue

            near_water = False

            # check nearby cells for water

            # check nearby cells
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:

                nx = col + dx
                ny = row + dy

                if not (0 <= nx < COLS and 0 <= ny < ROWS):
                    continue

                neighbor = grid[ny][nx]

                if neighbor == 0:
                    continue

                if get_material(neighbor) == WATER:
                    near_water = True
                    break

            # absorb moisture if near water
            if near_water:
                cell["wetness"] += 2

            # Moisture diffusion

            if cell["wetness"] > 20:

                for dx in [-1, 1]:

                    nx = col + dx

                    if not (0 <= nx < COLS):
                        continue

                    neighbor = grid[row][nx]

                    if neighbor == 0:
                        continue

                    if "wetness" not in neighbor:
                        continue

                    moisture_diffusion = (cell["wetness"] - neighbor["wetness"])

                    if moisture_diffusion > 10:
                        transfer = moisture_diffusion * 0.05
                        cell["wetness"] -= transfer
                        neighbor["wetness"] += transfer

            # Dry out slowly
            else:

                cell["wetness"] -= 0.2

            # Clamp values
            cell["wetness"] = max(0, min(100, cell["wetness"]))

            # Ground water seepage

            if cell["wetness"] > 70:

                below_y = row + 1

                if below_y < ROWS and grid[below_y][col] == 0:

                    if random.random() < 0.0007:
                        grid[below_y][col] = create_cell(WATER)