from settings import *
from materials import materials
from cell import create_cell
from simulation_utils import get_material


def update_reactions(grid):

    for row in range(ROWS):

        for col in range(COLS):

            cell_data= grid[row][col]

            if cell_data == 0:
                continue

            material_id= get_material(cell_data)
            material= materials[material_id]



            # Check for reactions
            for dx, dy in [(0, -1), (0,1), (-1,0), (1,0)]:

                nx, ny = col + dx, row + dy

                if not (0 <= nx < COLS and 0 <= ny < ROWS):
                    continue

                neighbor_data = grid[ny][nx]

                if neighbor_data == 0:
                    continue

                neighbor_material = get_material(neighbor_data)

                # check reaction rules

                for reaction in material.get("reactions", []):
                    if (neighbor_material == reaction["with"]):
                        
                        # Temperature Check

                        if (cell_data["temperature"] >= reaction["min_temp"]):

                            # TRANSFORM SELF

                            grid[row][col] = create_cell(reaction["result_self"], cell_data["temperature"])

                            # Transform Other
                            grid[ny][nx] = create_cell(reaction["result_other"], neighbor_data["temperature"])

            temperature= cell_data["temperature"]

           # Boiling

            if "boiling_point" in material:
                if temperature >= material["boiling_point"]:
                    new_material = material["boils_into"]

                    grid[row][col] = create_cell(new_material, temperature)

                    continue

            # Condensation

            if "condensation_point" in material:
                if temperature <= material["condensation_point"]:
                    new_material = material["condenses_into"]

                    grid[row][col] = create_cell(new_material, temperature)

                    continue
            
            # Solidification
            if "solidify_point" in material:
                if temperature <= material["solidify_point"]:
                    new_material = material["solidifies_into"]

                    grid[row][col] = create_cell(new_material, temperature)

                    continue

            # Ignition
            if "ignition_point" in material:
                if temperature >= material["ignition_point"]:
                    new_material = material["ignites_into"]

                    new_cell = create_cell(new_material, temperature)

                    # Transfer Fule Value
                    if "fuel_value" in material:
                        new_cell["fuel"] = material["fuel_value"]

                    grid[row][col] = new_cell

            # Melting
            if "melting_point" in material:
                if temperature >= material["melting_point"]:

                    grid[row][col] = 0