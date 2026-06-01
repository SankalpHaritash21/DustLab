from settings import *
from materials import materials


def update_temperature(grid):

    temp_changes = []

    # CREATE BUFFER
    for row in range(ROWS):

        current_row = []

        for col in range(COLS):
            current_row.append(0)

        temp_changes.append(current_row)


    # HEAT PROPAGATION
    for row in range(ROWS):

        for col in range(COLS):

            cell = grid[row][col]

            if cell == 0:
                continue

            material_id = cell["material"]

            material = materials[material_id]

            cell_temp = cell["temperature"]

            conductivity = material["thermal_conductivity"]

            specific_heat = material["specific_heat"]

            neighbors = [
                (0, -1),
                (0, 1),
                (-1, 0),
                (1, 0)
            ]

            for dx, dy in neighbors:

                nx = col + dx
                ny = row + dy

                if not (0 <= nx < COLS and 0 <= ny < ROWS):
                    continue

                neighbor = grid[ny][nx]

                if neighbor == 0:
                    continue

                neighbor_temp = neighbor["temperature"]

                temp_difference = neighbor_temp - cell_temp

                heat_transfer = (
                    temp_difference
                    * conductivity
                    * 0.25
                )

                heat_transfer /= specific_heat

                temp_changes[row][col] += heat_transfer

    # APPLY TEMPERATURE CHANGES
    for row in range(ROWS):

        for col in range(COLS):

            cell = grid[row][col]

            if cell == 0:
                continue

            cell["temperature"] += temp_changes[row][col]

            # AMBIENT COOLING
            AMBIENT_TEMP = 20

            cell["temperature"] += (
                AMBIENT_TEMP - cell["temperature"]
            ) * 0.001
