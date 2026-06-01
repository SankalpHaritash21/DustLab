from settings import *
from materials import materials
from cell import create_cell


def update_reactions(grid):

    for row in range(ROWS):

        for col in range(COLS):

            cell= grid[row][col]

            if cell == 0:
                continue

            material= cell["material"]

            temprature= cell["temperature"]

            # Water + Lava= Steam

            if material == WATER:
                if temprature >= 50:
                    grid[row][col] = create_cell(STEAM, temprature)

            # lava -> Stone

            if material == LAVA:
                if temprature <= 200:
                    grid[row][col] = create_cell(STONE, temprature)

            if material == OIL:
                if temprature >= 100:

                    fire= create_cell(FIRE, temprature)

                    fire["fuel"] = 200
                    grid[row][col] = fire