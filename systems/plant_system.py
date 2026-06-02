import random

from settings import *
from cell import create_cell
from simulation_utils import get_material

def update_plants(grid, updated):


    for row in range(ROWS):
        for col in range(COLS):

           cell= grid[row][col]

           if cell == 0:
                continue
           
           if ( get_material(cell) != PLANT):
                continue
           
           # Support Check
           
           support_y= row + 1

           if support_y < ROWS:
               
               support = grid[support_y][col]

               if support == 0:
                   grid[row][col] = 0
                   updated.add((row, col))
                   continue
               
           

           # Plant Growth Logic

           if "age" not in cell:
                cell["age"] = 0

           cell["age"] += 1
           
           # Old Plant Dies
           if cell["age"] > 500:
               grid[row][col] = 0
               updated.add((row, col))
               continue
           
           # Random Growth

           for dx, dy in [(0, -1)]:
               
               nx, ny = col + dx, row + dy

               if not (0 <= nx < COLS and 0 <= ny < ROWS):
                   continue
               
               if (grid[ny][nx] == 0 and random.random() < 0.001):
                   
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

                   if support_material not in [ SAND, STONE, PLANT]:
                       continue
                   
                   grid[ny][nx] = new_plant
                   updated.add((ny, nx))