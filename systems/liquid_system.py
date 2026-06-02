import random

from settings import *
from simulation_utils import get_density, get_type, get_material


def update_liquids(grid, updated):
    # liquid SIMULATION

    for row in range(ROWS - 2, -1, -1):

        for col in range(COLS):

            if (row, col) in updated:
                continue

            cell_data = grid[row][col]
            if cell_data == 0:
                continue

            cell = get_material(cell_data)

            if get_type(cell) == "liquid":
                below = grid[row + 1][col]

                if below != 0:
                    current_density = get_density(cell)
                    below_density = get_density(get_material(below))

                    below_type = get_type(get_material(below))

                    if ( below_type in ["liquid", "gas"] and current_density > below_density):
                        grid[row][col] = below
                        grid[row + 1][col] = cell_data

                        updated.add((row + 1, col))
                        updated.add((row, col))
                        continue

                # fall downward
                if grid[row + 1][col] == 0:

                    grid[row][col] = 0
                    grid[row + 1][col] = cell_data

                    updated.add((row + 1, col))

                else:

                    directions = [-1, 1]
                    random.shuffle(directions)

                    moved = False

                    # diagonal flow
                    for direction in directions:

                        new_col = col + direction

                        if (
                            0 <= new_col < COLS
                            and grid[row + 1][new_col] == 0
                            and grid[row][new_col] == 0
                        ):

                            grid[row][col] = 0
                            grid[row + 1][new_col] = cell_data

                            updated.add((row + 1, new_col))

                            moved = True
                            break

                    # sideways flow
                    if not moved and random.random() < 0.5:

                        for direction in directions:

                            new_col = col + direction

                            if (
                                0 <= new_col < COLS
                                and grid[row][new_col] == 0
                            ):

                                grid[row][col] = 0
                                grid[row][new_col] = cell_data

                                updated.add((row, new_col))

                                break