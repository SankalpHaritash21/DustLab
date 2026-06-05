import random

from settings import *
from simulation_utils import get_density, get_type, get_material, get_local_weight



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

                    slip_chance = 1.0
                    unstable = False
                    steep_slope = False

                    # wet terrain became unstable

                    if "wetness" in cell_data:

                        wetness = cell_data["wetness"]

                        if wetness > 40:
                            slip_chance = 0.55

                            left_empty = (col > 0 and grid[row][col - 1] == 0)

                            right_empty = (col < COLS - 1 and grid[row][col + 1] == 0)

                            if left_empty or right_empty:
                                unstable = True



                    if random.random() < 0.5:

                        directions = [-1, 1]

                    else:

                        directions = [1, -1]
                    

                    # Natural slop instability

                    steep_slope = False

                    if row + 1 < ROWS:

                        left_drop = (
                            col > 0
                            and grid[row][col - 1] == 0
                            and grid[row + 1][col - 1] == 0
                        )

                        right_drop = (
                            col < COLS - 1
                            and grid[row][col + 1] == 0
                            and grid[row + 1][col + 1] == 0
                        )

                        if left_drop or right_drop:
                            steep_slope = True

                    weight = get_local_weight(grid, row, col)
                    
                    # unstable wet terrain slide more
                    if unstable or steep_slope or weight >= 3:

                        slip_chance = 0.35
                        directions = [-1, 1, -1, 1]

                    for direction in directions:
                        new_col = col + direction

                        if (
                            random.random() < slip_chance
                            and
                            0 <= new_col < COLS
                        ):

                            # normal diagonal fall

                            if (
                                grid[row + 1][new_col] == 0
                            ):

                                grid[row][col] = 0
                                grid[row + 1][new_col] = cell_data

                                updated.add((row + 1, new_col))
                                updated.add((row, col))

                                break

                            