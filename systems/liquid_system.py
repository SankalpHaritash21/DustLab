import random

from settings import *
from simulation_utils import get_density, get_type, get_material, get_liquid_pressure
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

            if get_type(cell) == "liquid":

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

                    # waterfall splash mist

                    if cell == WATER:

                        if row > 0 and random.random() < 0.02:
                            
                            for dx in [-1, 0, 1]:

                                nx = col + dx

                                if 0 <= nx < COLS:

                                    if grid[row][nx] == 0 and grid[row - 1][nx] == 0:

                                        mist =  create_cell(STEAM)
                                        mist["lifetime"] = 5

                                        grid[row][nx] = mist


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
                                if random.random() < 0.08:
                                    cell_data["carrying_sand"] = True
                                    grid[row][nx] = 0
                                    break



                    updated.add((row + 1, col))

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

                        if random.random() < 0.5:
                            directions = [-1, 1]
                        else:
                            directions = [1, -1]
                    moved = False

                     # sediment deposition
                    if (cell == WATER and "carrying_sand" in cell_data):

                        if random.random() < 0.02:

                            below_y = row + 1

                            if below_y < ROWS:

                                # deposit only if ground exists below
                                if grid[below_y][col] != 0:

                                    grid[row][col] = create_cell(SAND)

                                    del cell_data["carrying_sand"]

                                    updated.add((row, col))

                                    moved = True

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
                            cell_data["flow_dir"] = direction

                            if pressure >= 6:
                                cell_data["foam"] = min(40, cell_data.get("foam", 0) + 10)

                            # directional river errosion

                            if cell == WATER:

                                erosion_x = new_col + direction
                                erosion_y = row

                                if (
                                    0 <= erosion_x < COLS
                                    and 0 <= erosion_y < ROWS
                                    
                                ):

                                    target = grid[erosion_y][erosion_x]

                                    if target != 0:

                                        target_material = get_material(target)

                                        # flow water eodes looses terrain

                                        if target_material == SAND:

                                            if random.random() < 0.02:
                                                grid[erosion_y][erosion_x] = 0
                                

                            updated.add((row + 1, new_col))

                            moved = True
                            break
                       
                   
                    # sideways flow
                    if not moved and random.random() < (0.01 if is_lava else 0.15):

                        for direction in directions:

                            new_col = (col + direction)

                            if (
                                0 <= new_col < COLS
                                and grid[row][new_col] == 0
                            ):

                                grid[row][col] = 0
                                grid[row][new_col] = cell_data
                                cell_data["flow_dir"]= direction

                                if pressure >= 6:
                                    cell_data["foam"] = min(40, cell_data.get("foam", 0) + 10)

                                updated.add((row, new_col))

                                break