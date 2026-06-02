import random

from settings import *
from materials import materials
from cell import create_cell
from simulation_utils import get_density, get_type, get_material


def update_gases(grid, updated):
     # Gas SIMULATION

    for row in range(ROWS):

        for col in range(COLS):

            cell_data = grid[row][col]
            if cell_data == 0:
                continue

            cell = get_material(cell_data)

            if (row, col) in updated:
                    continue

            if get_type(cell) == "gas":

                if row == 0:
                    grid[row][col] = 0
                    continue

                # fire spread
                for dx in [-1 ,0, 1]:
                    for dy in [-1, 0, 1]:

                        nx = col + dx
                        ny = row + dy

                        if (0 <= ny < ROWS and 0 <= nx < COLS):

                            neighbor_data = grid[ny][nx]
                            if neighbor_data != 0:
                                neighbor_material_id = get_material(neighbor_data)
                                neighbor_material = materials[neighbor_material_id]

                                # Flamable materials can ignite
                                if "ignition_point" in neighbor_material:
                                    ignition_point = neighbor_material["ignition_point"]
                                    neighbor_temperature = neighbor_data["temperature"]

                                    # ignite if hot enough
                                    if (neighbor_temperature >= ignition_point and random.random() < 0.3):
                                        new_fire = create_cell(FIRE, neighbor_temperature)
                                        new_fire["lifetime"] = 80

                                        # Transfer Fuel Value
                                        if "fuel_value" in neighbor_material:
                                            new_fire["fuel"] = neighbor_material["fuel_value"]

                                        grid[ny][nx] = new_fire
                                        updated.add((ny, nx))
                                        

                # random FIRE death
                if cell == FIRE:
                    
                    # Fire Heat Output
                    heat_output = materials[cell]["heat_output"]
                    cell_data["temperature"] += heat_output

                    # Fire lifetime
                    if "lifetime" not in cell_data:
                        cell_data["lifetime"] = 80

                    cell_data["lifetime"] -= 1
                    

                    # Fire Dies

                    if cell_data["lifetime"] <= 0:
                        smoke = create_cell(SMOKE, cell_data["temperature"])
                        smoke["lifetime"] = 100
                        grid[row][col] = smoke
                        updated.add((row, col))
                        continue

                
                # SMOKE Lifetime
                if cell == SMOKE:
                    
                    if "lifetime" not in cell_data:
                        cell_data["lifetime"] = 100

                    cell_data["lifetime"] -= 1

                    if cell_data["lifetime"] <= 0:
                        grid[row][col] = 0
                        updated.add((row, col))
                        continue
            

                buoyancy = materials[cell]["buoyancy"]

                # Higher buoyancy means faster rising
                if buoyancy >= 0.9:
                    directions = [-1, 0, 1]  # More likely to rise straight up
                
                # Moderate buoyancy means more random movement
                elif buoyancy >= 0.7:
                    directions = [-2, -1, 0, 1, 2]  # More likely to rise but can move sideways
                
                # Low buoyancy means very random movement
                else:
                    directions = [-3, -2, -1, 0, 1, 2, 3]  # Can move in a wider range

                random.shuffle(directions)

                moved= False

                # rise upward
                for direction in directions:

                    new_col= col + direction

                    if (0<=new_col< COLS and grid[row - 1][new_col] == 0):

                        grid[row][col]= 0


                        if cell == SMOKE and random.random() < 0.5:
                            continue

                        if cell == STEAM and random.random() < 0.5:
                            continue

                        target_row= row - 1
                        grid[target_row][new_col]= cell_data

                        updated.add((target_row, new_col))

                        moved= True
                        break
                
                # Sideways movement
                if not moved:
                    random.shuffle(directions)

                    for direction in directions:

                        new_col= col + direction

                        if (0<=new_col< COLS and grid[row][new_col] == 0):

                            grid[row][col]= 0
                            grid[row][new_col]= cell_data

                            updated.add((row, new_col))
                            moved= True

                            break
