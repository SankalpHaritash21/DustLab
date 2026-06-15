from settings import *

def update_foam(grid):

    for row in range(ROWS):
        for col in range(COLS):
            cell = grid[row][col]

            if cell == 0:
                continue

            if "foam" in cell:
                cell["foam"] -= 1

                if cell["foam"] <= 0:
                    del cell["foam"]