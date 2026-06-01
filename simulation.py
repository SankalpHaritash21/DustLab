import random

from settings import *
from materials import materials
from cell import create_cell


def get_density(material_id):
    if material_id == 0:
        return -1
    
    return materials[material_id]["density"]

def get_type(material_id):
    if material_id == 0:
        return None
    
    return materials[material_id]["type"]

def get_material(cell):

    if cell == 0:
        return 0

    return cell["material"]

def update_simulation(grid):

    updated = set()

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

                    directions = [-1, 1]
                    random.shuffle(directions)

                    for direction in directions:
                        new_col = col + direction

                        if (
                            0 <= new_col < COLS
                            and (grid[row + 1][new_col] == 0 or get_density(cell) > get_density(get_material(grid[row + 1][new_col])))
                        ):

                            target = grid[row + 1][new_col]

                            grid[row][col] = target
                            grid[row + 1][new_col] = cell_data

                            updated.add((row + 1, new_col))
                            updated.add((row, col))
                            break

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
                if grid[row + 1][col] == 0:

                    grid[row][col] = 0
                    grid[row + 1][col] = cell_data

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
                            grid[row + 1][new_col] = cell_data

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
                                grid[row][new_col] = cell_data

                                updated.add((row, new_col))

                                break
    

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
                            if ( neighbor_data != 0 and get_material(neighbor_data) == OIL  and random.random() < 0.3):
                                grid[ny][nx] = create_cell(FIRE, 200)
                                updated.add((ny, nx))

                # random FIRE death
                if cell == FIRE:
                    
                    # fule burn
                    cell_data["fuel"] -= 1

                    # emit heat while burning 
                    cell_data["temperature"] += 2
                    
                    # fire dies when fuel exhausted
                    if cell_data["fuel"] <= 0: 
                        grid[row][col] = create_cell( SMOKE, cell_data["temperature"] )  
                        continue

                
                # SMOKE Lifetime
                if cell == SMOKE:
                    if random.random() < 0.02:
                        grid[row][col] = 0
                        continue
            

                if cell == FIRE:
                    directions = [-1, 0, 1]

                elif cell == SMOKE:
                    directions = [-2, -1, 0, 1, 2]

                elif cell == STEAM:
                    directions = [-2, -1, 0, 1, 2]

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

                