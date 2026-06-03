import random

from settings import *
from cell import create_cell


def generate_world(grid):

    ground_height = ROWS // 2

    for col in range(COLS):

        # random terain variation

        terrain_height = ground_height + random.randint(-5, 5)

        for row in range(terrain_height, ROWS):

            # deep stone

            if row > terrain_height + 8:
                grid[row][col] = create_cell(STONE)

            # upper sand layer

            else:
                grid[row][col] = create_cell(SAND)
        
        # Random Caves

        if random.random() < 0.08:
            cave_center= random.randint(terrain_height + 12, ROWS - 8)
            cave_radius = random.randint(2, 5)

            for dx in range(- cave_radius, cave_radius + 1):
                for dy in range(-cave_radius, cave_radius + 1):
                    cave_x = col + dx
                    cave_y = cave_center + dy


                    if not (0 <= cave_x < COLS and 0 <= cave_y < ROWS):
                        continue

                    if ((dx ** 2 + dy ** 2) <= cave_radius ** 2):
                        grid[cave_y][cave_x] = 0

            for reinforce_x in range( col - cave_radius - 2, col + cave_radius ):
                for reinforce_y in range(cave_center - cave_radius -2, cave_center - cave_radius - 1):
                
                    if ( 0 <= reinforce_x < COLS and 0 <= reinforce_y < ROWS ):
                        if ( grid[reinforce_y][reinforce_x] != 0 ):
                            grid[ reinforce_y ][reinforce_x] = ( create_cell(STONE) )

            # Lava Caves Baseline
            if random.random() < 0.1:
                    lava_y= (cave_center + cave_radius - 2)

                    for lava_dx in range(-cave_radius + 1, cave_radius):

                        for lava_dy in [0,1]:
                            lava_x = col + lava_dx

                            if (0 <= lava_x < COLS and 0 <= lava_y < ROWS):
                                grid[lava_y + lava_dy ][lava_x] = create_cell(LAVA, 1200)

                                # Stone Floors in caves

                                if lava_y + lava_dy + 1 < ROWS:
                                    grid[lava_y + lava_dy + 1][lava_x] = create_cell(STONE)


            # Underground Water Pockets

            if random.random() < 0.12:

                water_y= ( cave_center + cave_radius - 2 )

                for water_dx in range(-cave_radius + 1, cave_radius):

                    for water_dy in [0, 1, 2]:

                        water_x = col + water_dx

                        if (0 <= water_x < COLS and 0 <= water_y < ROWS):

                            #  Only place water if no lava

                            if ( 0 <= water_y + water_dy <ROWS and grid[water_y + water_dy][water_x] == 0):
                                grid[water_y + water_dy][water_x] = create_cell(WATER)
        
        # random Plants
        if random.random() < 0.1:
            plant_row = terrain_height - 1

            if plant_row >= 0:
                grid[plant_row][col] = create_cell(PLANT)