import random

from settings import *
from materials import materials


def get_density(material_id):
    if material_id == 0:
        return -1
    
    return materials[material_id]["density"]

def get_type(material_id):
    if material_id == 0:
        return None
    
    return materials[material_id]["type"]



def update_simulation(grid):

    updated = set()

    # -------------------
    # SAND SIMULATION
    # -------------------

    for row in range(ROWS - 2, -1, -1):

        for col in range(COLS):

            if (row, col) in updated:
                continue

            
            cell = grid[row][col]
            if get_type(cell) == "powder":
                moved = False

                below = grid[row + 1][col]

                # fall downward
                if below == 0:

                    grid[row][col] = 0
                    grid[row + 1][col] = cell

                    updated.add((row + 1, col))
                    moved = True

                # density-based interaction: density swap
                elif below != 0:
                    current_density= get_density(cell)
                    below_density = get_density(below)

                    if current_density > below_density:
                        grid[row][col] = below
                        grid[row + 1][col] = cell

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
                            and (grid[row + 1][new_col] == 0 or get_density(cell) > get_density(grid[row + 1][new_col]))
                        ):

                            target = grid[row + 1][new_col]

                            grid[row][col] = target
                            grid[row + 1][new_col] = cell

                            updated.add((row + 1, new_col))
                            updated.add((row, col))
                            break

    # -------------------
    # WATER SIMULATION
    # -------------------

    for row in range(ROWS - 2, -1, -1):

        for col in range(COLS):

            if (row, col) in updated:
                continue

            cell = grid[row][col]
            if get_type(cell) == "liquid":

                # fall downward
                if grid[row + 1][col] == 0:

                    grid[row][col] = 0
                    grid[row + 1][col] = cell

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
                            grid[row + 1][new_col] = cell

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
                                grid[row][new_col] = cell

                                updated.add((row, new_col))

                                break