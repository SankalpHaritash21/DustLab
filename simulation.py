import random

from settings import *


def update_simulation(grid):

    updated = set()

    # -------------------
    # SAND SIMULATION
    # -------------------

    for row in range(ROWS - 2, -1, -1):

        for col in range(COLS):

            if (row, col) in updated:
                continue

            if grid[row][col] == SAND:

                below = grid[row + 1][col]

                # fall downward
                if below == 0:

                    grid[row][col] = 0
                    grid[row + 1][col] = SAND

                    updated.add((row + 1, col))

                # sink through water
                elif below == WATER:

                    grid[row][col] = WATER
                    grid[row + 1][col] = SAND

                    updated.add((row + 1, col))
                    updated.add((row, col))

                else:

                    direction = random.choice([-1, 1])

                    new_col = col + direction

                    if (
                        0 <= new_col < COLS
                        and grid[row + 1][new_col] in [0, WATER]
                    ):

                        target = grid[row + 1][new_col]

                        grid[row][col] = target
                        grid[row + 1][new_col] = SAND

                        updated.add((row + 1, new_col))
                        updated.add((row, col))

    # -------------------
    # WATER SIMULATION
    # -------------------

    for row in range(ROWS - 2, -1, -1):

        for col in range(COLS):

            if (row, col) in updated:
                continue

            if grid[row][col] == WATER:

                # fall downward
                if grid[row + 1][col] == 0:

                    grid[row][col] = 0
                    grid[row + 1][col] = WATER

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
                            grid[row + 1][new_col] = WATER

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
                                grid[row][new_col] = WATER

                                updated.add((row, new_col))

                                break