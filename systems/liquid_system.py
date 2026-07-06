import random

from settings import *
from simulation_utils import get_density, get_type, get_material, get_liquid_pressure, get_sediment_capacity, count_adjacent_sand
from cell import create_cell

def update_liquids(grid, updated):
    # liquid SIMULATION

    for row in range(ROWS - 2, -1, -1):

        for col in range(COLS):

            if (row, col) in updated:
                continue

            cell_data = grid[row][col]
            if cell_data == 0:
                continue

            cell = get_material(cell_data)

            

            if cell == WATER:

                cell_data["velocity"] = max(0, cell_data.get("velocity", 0) - 0.05)

            if get_type(cell) == "liquid":

                # Surface evaporation for water

                if cell == WATER:

                    # only near surface

                    if row < ROWS // 5:

                        evaporation_chance = 0.0005

                        # hot water eveporates faster

                        if cell_data["temperature"] > 50:
                            evaporation_chance *= 5

                        if random.random() < evaporation_chance:

                            steam = create_cell(STEAM)
                            steam["lifetime"] = 80

                            steam["temperature"] = max(100,cell_data["temperature"])

                            grid[row][col] = steam
                            updated.add((row, col))
                            continue

                is_lava= (cell == LAVA)



                pressure = get_liquid_pressure(grid, row, col)


                below = grid[row + 1][col]

                if below != 0:
                    current_density = get_density(cell)
                    below_density = get_density(get_material(below))

                    below_type = get_type(get_material(below))

                    if ( below_type in ["liquid", "gas"] and current_density > below_density):
                        grid[row][col] = below
                        grid[row + 1][col] = cell_data

                        if cell == WATER:

                            cell_data["velocity"] = min(10, cell_data.get("velocity", 0) + 0.5)

                        # downward movement resets directional momentum
                        if "flow_dir" in cell_data:
                            del cell_data["flow_dir"]

                        updated.add((row + 1, col))
                        updated.add((row, col))


                        continue

                # fall downward

                can_fall = True

                if is_lava:
                    can_fall = (random.random() < 0.25)


                if ( can_fall and (grid[row + 1][col] == 0)):

                    grid[row][col] = 0
                    grid[row + 1][col] = cell_data

                    cell_data["velocity"] = min(10, cell_data.get("velocity", 0) + 1)

                    # waterfall splash mist

                    # if cell == WATER:

                    #     if row > 0 and random.random() < 0.02:
                            
                    #         for dx in [-1, 0, 1]:

                    #             nx = col + dx

                    #             if 0 <= nx < COLS:

                    #                 if grid[row][nx] == 0 and grid[row - 1][nx] == 0:

                    #                     mist =  create_cell(STEAM)
                    #                     mist["lifetime"] = 5

                    #                     grid[row][nx] = mist


                    # downward movement resets directional momentum
                    if "flow_dir" in cell_data:
                        del cell_data["flow_dir"]

                    # sediment transport

                    if cell == WATER:

                        for dx in [ -1, 1]:
                            nx = col + dx

                            if not (0 <= nx < COLS):
                                continue

                            neighbor = grid[row][nx]

                            if neighbor == 0:
                                continue

                            neighbor_material = get_material(neighbor)

                            # drag loose sand

                            if neighbor_material == SAND:

                                capacity = get_sediment_capacity(pressure)

                                if cell_data["sediment"] < capacity:
                                    
                                    if random.random() < 0.08:
                                        cell_data["sediment"] += 1
                                        grid[row][nx] = 0
                                        break



                    updated.add((row + 1, col))
                    updated.add((row, col))

                else:

                    # Pressure-based flow

                    if is_lava:
                        directions = [-1, 1]

                    else:
                        if pressure >= 6:
                            directions = [ -2, -1, 1, 2, ]
                        else:
                            directions = [-1, 1]

                    if cell == WATER and "flow_dir" in cell_data:

                        preferred = cell_data["flow_dir"]

                        directions = [preferred]

                        if preferred == -1:
                            directions.append(1)
                        else:
                            directions.append(-1)

                    else:

                        bias = cell_data.get("river_bias", 1)
                        directions = [bias, -bias]


                    moved = False

                     # sediment deposition
                    if (cell == WATER and cell_data.get("sediment", 0) > 0 and pressure <= 2 and cell_data.get("velocity", 0) < 2):
                        

                        bank_factor = count_adjacent_sand(grid, row, col)
                        deposit_chance = 0.002 + (bank_factor * 0.003)

                        if random.random() < deposit_chance:

                            below_y = row + 1

                            if below_y < ROWS:

                                # try to place sand above ground

                                deposit_y = row

                                # deposit only if ground exists below
                                if grid[deposit_y][col] == cell_data:

                                    flow_dir = cell_data.get("flow_dir", 0)

                                    deposit_order = []

                                    # fallback side

                                    if flow_dir == -1:
                                        deposit_order = [1, -1]
                                    elif flow_dir == 1:
                                        deposit_order = [-1, 1]
                                    else:
                                        deposit_order = [-1, 1]

                                    for dx in deposit_order:

                                        nx = col + dx

                                        if not (0 <= nx < COLS):
                                            continue

                                        # need  solid support underneath

                                        if (
                                            grid[row][nx] == 0 and
                                            row + 1 < ROWS and
                                            grid[row + 1][nx] != 0 
                                        ):
                                            
                                            grid[row][nx] = create_cell(SAND)

                                            cell_data["sediment"] -= 1
                                            
                                            # water loses energy while dropping sediment

                                            cell_data["velocity"] = max(0, cell_data["velocity"] - 1)

                                            updated.add((row, nx))

                                            moved = True
                                            break

                    if moved:
                        continue


                    # diagonal flow
                    for direction in directions:
                       

                       new_col = (col + direction)

                       if (
                            0 <= new_col < COLS
                            and grid[row + 1][new_col] == 0
                            and grid[row][new_col] == 0
                        ):

                            grid[row][col] = 0
                            grid[row + 1][new_col] = cell_data

                            cell_data["velocity"] = min(10, cell_data.get("velocity", 0) + 1)
                            cell_data["flow_dir"] = direction

                            # Occasionally change preferred river direction

                            if random.random() < 0.002:
                                cell_data["river_bias"] *= -1 

                            if pressure >= 6:
                                cell_data["foam"] = min(40, cell_data.get("foam", 0) + 10)

                            # directional river errosion

                            if cell == WATER:

                                erosion_targets = [
                                    # front wall
                                    (new_col + direction, row - 1),
                                    (new_col + direction, row),
                                    (new_col + direction, row + 1),

                                    # slightly ahead

                                    (new_col + 2 * direction, row),
                                    (new_col + 2 * direction, row - 1),
                                    (new_col + 2 * direction, row + 1),
                                ]

                                for erosion_x, erosion_y in erosion_targets:

                                    if not (0 <= erosion_x < COLS and 0 <= erosion_y < ROWS):
                                        continue

                                    target = grid[erosion_y][erosion_x]

                                    if target == 0:
                                        continue

                                    if get_material(target) != SAND:
                                        continue


                                    # support sand is harder to erode

                                    support = 0

                                    for check_y in range( erosion_y + 1, min(ROWS, erosion_y + 3)):

                                        if grid[check_y][erosion_x] != 0:

                                            support += 1

                                    velocity = cell_data.get("velocity", 0)

                                    erosion_chance = 0.001 + (pressure * 0.002) + (velocity * 0.003)

                                    # Dense support make erosion harder

                                    erosion_chance /= (1 + support)

                                    # wet sand resists erosion

                                    if "wetness" in target:

                                        wetness = target["wetness"]

                                        erosion_chance *= max(0.2, 1 - wetness / 100)

                                    # Persistent flow cuts stronger

                                    if abs(cell_data.get("flow_dir", 0)) == 1:
                                        erosion_chance *= 1.2

                                    if random.random() < erosion_chance:

                                        # Remove support sand
                                        grid[erosion_y][erosion_x] = 0

                                        # Small chance to destabilize adjacent sand

                                        for dx in [-1, 1]:
                                            nx = erosion_x + dx

                                            if 0 <= nx < COLS:
                                                neighbor = grid[erosion_y][nx]

                                                if (
                                                    neighbor != 0
                                                    and get_material(neighbor) == SAND
                                                    and random.random() < 0.15
                                                ):
                                                    
                                                    updated.add((erosion_y, nx))

                                        # Carry the removed material
                                        capacity = get_sediment_capacity(pressure)

                                        if cell_data["sediment"] < capacity:
                                            cell_data["sediment"] += 1
                                            

                                            # Cutting terrain slows water slightly

                                            cell_data["velocity"] = max(0, cell_data["velocity"] - 1)

                                        updated.add((erosion_y, erosion_x))
                                

                            updated.add((row + 1, new_col))
                            updated.add((row, col))

                            moved = True
                            break
                       
                   
                    # sideways flow

                    sideways_chance = 0.15

                    if cell == WATER:

                        sideways_chance += cell_data.get("velocity", 0) * 0.03

                        sideways_chance = min(0.6, sideways_chance)

                        if not moved and random.random() < ( 0.01 if is_lava else sideways_chance ):

                            for direction in directions:

                                new_col = (col + direction)

                                if (
                                    0 <= new_col < COLS
                                    and grid[row][new_col] == 0
                                ):

                                    grid[row][col] = 0
                                    grid[row][new_col] = cell_data

                                    cell_data["velocity"] = max( 0.5, cell_data.get("velocity", 0))
                                    cell_data["flow_dir"]= direction

                                    if pressure >= 6 or cell_data.get("velocity", 0) >= 5:
                                        cell_data["foam"] = min(40, cell_data.get("foam", 0) + 10)

                                    updated.add((row, new_col))
                                    updated.add((row, col))

                                    break