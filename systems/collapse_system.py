import random

from settings import *
from cell import create_cell
from simulation_utils import get_material
from simulation_utils import get_local_weight


def update_collapse(grid, updated):

    for row in range(ROWS - 2):
        for col in range(COLS):

            if (row, col) in updated:
                continue
            
            cell = grid[row][col]


            if cell == 0:
                continue

            material = get_material(cell)

            # only stone check

            if material not in [STONE, CRACKED_STONE]:
                continue

            # unsupported check

            below = grid[row + 1][col]

            if below != 0:
                continue

            left_support = (
                col > 0 and grid[row + 1][col - 1] != 0
            )

            right_support = (
                col < COLS - 1 and grid[row + 1][col + 1] != 0
            )


            # fully unsupported

            if not left_support and not right_support:

                near_cracked = False

                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:

                    nx= col + dx
                    ny = row + dy

                    if not (0 <= nx < COLS and 0 <= ny < ROWS):
                        continue

                    neighbor = grid[ny][nx]

                    if neighbor == 0:
                        continue

                    if get_material(neighbor) == CRACKED_STONE:
                        near_cracked = True
                        break
                
                crack_chance = 0.01
                if near_cracked:
                    crack_chance = 0.05

                weight = get_local_weight(grid, row, col)

                if weight > 5:
                    crack_chance *= 3

                if material == STONE and random.random() < crack_chance:
                    grid[row][col] = create_cell(CRACKED_STONE)
                    
                    updated.add((row, col))

                if material == CRACKED_STONE:


                    # crack progression

                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:

                        nx= col + dx
                        ny = row + dy

                        if not (0 <= nx < COLS and 0 <= ny < ROWS):
                            continue

                        neighbor = grid[ny][nx]

                        if neighbor == 0:
                            continue

                        if get_material(neighbor) == STONE:

                            if random.random() < 0.005:
                                grid[ny][nx] = create_cell(CRACKED_STONE)
                                updated.add((ny, nx))


                    # Collapse code

                    if random.random() < 0.002:
                        if random.random() < 0.7:
                            grid[row][col] = create_cell(SAND)

                        # debris dust

                        for dx in [-1, 0, 1]:

                            nx = col + dx
                            if 0 <= nx < COLS and row > 0:

                                if grid[row - 1][nx] == 0:

                                    if random.random() < 0.3:

                                        dust = create_cell(SMOKE)

                                        dust["lifetime"] = 20

                                        grid[row - 1][nx] = dust
                        
                        updated.add((row, col))