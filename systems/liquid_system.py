import random

from settings import *
from simulation_utils import get_density, get_type, get_material, get_liquid_pressure


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

                is_lava= (cell == LAVA)



                pressure = get_liquid_pressure(grid, row, col)


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

                can_fall = True

                if is_lava:
                    can_fall = (random.random() < 0.25)


                if ( can_fall and (grid[row + 1][col] == 0)):

                    grid[row][col] = 0
                    grid[row + 1][col] = cell_data

                    updated.add((row + 1, col))

                else:

                    # Pressure-based flow

                    if is_lava:
                        directions = [-1, 1]

                    else:
                        if pressure >= 6:
                            directions = [ -2, -1, 1, 2, ]
                        else:
                            directions = [-1, 1]

                    random.shuffle(directions)
                    moved = False

                    # diagonal flow
                    for direction in directions:
                       

                       new_col = (col + direction)

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
                    if not moved and random.random() < (0.01 if is_lava else 0.15):

                        for direction in directions:

                            new_col = (col + direction)

                            if (
                                0 <= new_col < COLS
                                and grid[row][new_col] == 0
                            ):

                                grid[row][col] = 0
                                grid[row][new_col] = cell_data

                                updated.add((row, new_col))

                                break