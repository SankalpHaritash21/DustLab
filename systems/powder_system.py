import random

from settings import *
from simulation_utils import get_density, get_type, get_material


def update_powders(grid, updated):
    # Powder SIMULATION

    for row in range(ROWS - 2, -1, -1):

        for col in range(COLS):

            if (row, col) in updated:
                continue
            
            cell_data = grid[row][col]
            if cell_data == 0:
                continue

            cell = get_material(cell_data)

            if get_type(cell) == "powder":
                moved = False

                below = grid[row + 1][col]

                # fall downward
                if below == 0:

                    grid[row][col] = 0
                    grid[row + 1][col] = cell_data

                    updated.add((row + 1, col))
                    moved = True

                #! density-based interaction: density swap
                elif below != 0:
                    current_density= get_density(cell)
                    below_density = get_density(get_material(below))


                    if ( current_density > below_density):
                        grid[row][col] = below
                        grid[row + 1][col] = cell_data

                        updated.add((row + 1, col))
                        updated.add((row, col))
                        moved = True

                if not moved:

                    directions = [-1, 1]
                    random.shuffle(directions)

                    for direction in directions:
                        new_col = col + direction

                        if (
                            0 <= new_col < COLS
                            and (grid[row + 1][new_col] == 0 or get_density(cell) > get_density(get_material(grid[row + 1][new_col])))
                        ):

                            target = grid[row + 1][new_col]

                            grid[row][col] = target
                            grid[row + 1][new_col] = cell_data

                            updated.add((row + 1, new_col))
                            updated.add((row, col))
                            break