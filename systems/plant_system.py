import random

from settings import *
from cell import create_cell
from simulation_utils import get_material, has_nearby_water, count_nearby_plants

def update_plants(grid, updated):


    for row in range(ROWS):
        for col in range(COLS):

           cell= grid[row][col]

           if cell == 0:
                continue
           
           if ( get_material(cell) != PLANT):
                continue
           

           # plant must have support below
           support_y= row + 1

           if support_y >= ROWS:
               continue
           
           support= grid[support_y][col]

           if support == 0:
               
               grid[row][col] = 0
               updated.add((row, col))
               continue
           
           support_material= get_material(support)

           if support_material not in [SAND, STONE]:
               
               grid[row][col] = 0
               updated.add((row, col))
               continue

           # Plant Growth Logic

           if "age" not in cell:
                cell["age"] = 0

           near_water = has_nearby_water(grid, row, col)
           nearby_plants = count_nearby_plants(grid, row, col)

           # serve overcrouding kills plants

           if nearby_plants > 18:
               if random.random() < 0.01:
                   
                   grid[row][col] = 0
                   updated.add((row, col))
                   continue

           
           if near_water:
               cell["age"] += 0.2
           else:
                cell["age"] += 1


           near_ash = False

           for dx in [-1,0,1]:
               for dy in [-1,0,1]:
                   
                   nx, ny = col + dx, row + dy

                   if not (0 <= nx < COLS and 0 <= ny < ROWS):
                       continue
                   
                   neighbor = grid[ny][nx]

                   if neighbor == 0:
                       continue
                   
                   if get_material(neighbor) == ASH:
                        near_ash = True

           # Old Plant Dies

           max_age = 500
           
           if near_water:
            max_age = 2000

           if cell["age"] > max_age:
               grid[row][col] = 0
               updated.add((row, col))
               continue
           
           # Overcrowding check

           if nearby_plants > 8:
               continue

           # Random Growth

           for dx, dy in [(0, -1)]:
               
               nx, ny = col + dx, row + dy

               if not (0 <= nx < COLS and 0 <= ny < ROWS):
                   continue
               
               growth_chance = (
                    0.005 if near_water and near_ash
                    else 0.002 if near_water
                    else 0.0002
                )
               
               if (grid[ny][nx] == 0 and random.random() < growth_chance):
                   
                   new_plant = create_cell(PLANT)
                   new_plant["age"] = 0

                   # SUPPORT PLANT  Check

                   support_y= ny + 1

                   if support_y >= ROWS:
                       continue
                   
                   support = grid[support_y][nx]

                   if support == 0:
                       continue
                   
                   support_material = get_material(support)

                   if support_material not in [ SAND, STONE]:
                       continue
                   
                   grid[ny][nx] = new_plant
                   updated.add((ny, nx))