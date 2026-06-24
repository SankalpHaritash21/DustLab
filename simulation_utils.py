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

def get_material(cell):

    if cell == 0:
        return 0

    return cell["material"]


def get_gas_pressure(grid, row, col):
    # Simple pressure calculation based on the number of gas particles above
    pressure = 0
    
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:

            if dx==0 and dy==0:
                continue

            nx, ny= col + dx, row + dy

            if not (0 <= nx < COLS and 0 <= ny < ROWS):
                continue

            neighbor= grid[ny][nx]

            if neighbor == 0:
                continue

            material= get_material(neighbor)

            if get_type(material) == "gas":
                pressure += 1
        
    return pressure

def get_liquid_pressure(grid, row, col):
    
    pressure = 0
    
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:

            if dx==0 and dy==0:
                continue

            nx, ny= col + dx, row + dy

            if not (0 <= nx < COLS and 0 <= ny < ROWS):
                continue

            neighbor= grid[ny][nx]

            if neighbor == 0:
                continue

            material= get_material(neighbor)

            if get_type(material) == "liquid":
                pressure += 1
        
    return pressure


def has_nearby_water(grid, row, col):

    for dx in [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]:
        for dy in [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]:

            nx, ny= col + dx, row + dy

            if not (0 <= nx < COLS and 0 <= ny < ROWS):
                continue

            neighbor= grid[ny][nx]

            if neighbor == 0:
                continue


            if (get_material(neighbor) == WATER):
                return True

    return False

def get_local_weight(grid, row, col):
    weight = 0
    
    # check few cells above
    for check_y in range(max(0, row - 5), row):

        above = grid[check_y][col]

        if above == 0:
            continue

        material = get_material(above)

        if get_type(material) == "powder":
            weight += 1

        elif get_type(material) == "solid":
            weight += 2

    return weight


def get_sediment_capacity(pressure):

    if pressure <= 1:
        return 1

    elif pressure <= 3:
        return 3

    else:
        return 5

def count_adjacent_sand(grid, row, col):

    count = 0

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:

            if dx==0 and dy==0:
                continue

            nx, ny= col + dx, row + dy

            if not (0 <= nx < COLS and 0 <= ny < ROWS):
                continue

            neighbor= grid[ny][nx]

            if neighbor != 0 and get_material(neighbor) == SAND:
                count += 1

    return count
