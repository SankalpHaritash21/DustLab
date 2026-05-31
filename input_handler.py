import pygame

from settings import *


def handle_input(grid, current_element, brush_size, simulation_speed):

    # EVENTS

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            return False, current_element

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                current_element = SAND

            elif event.key == pygame.K_2:
                current_element = WATER

            elif event.key == pygame.K_UP:
                brush_size += 1
            elif event.key == pygame.K_DOWN:
                brush_size = max(1, brush_size - 1)
            elif event.key == pygame.K_RIGHT:
                simulation_speed = max(1, simulation_speed - 1)
            elif event.key == pygame.K_LEFT:
                simulation_speed += 1

    # MOUSE INPUT

    mouse_buttons = pygame.mouse.get_pressed()

    mouse_x, mouse_y = pygame.mouse.get_pos()

    grid_x = mouse_x // CELL_SIZE
    grid_y = mouse_y // CELL_SIZE

    # LEFT CLICK = DRAW
    if mouse_buttons[0]:

        for dy in range(-brush_size, brush_size + 1):

            for dx in range(-brush_size, brush_size + 1):

                new_x = grid_x + dx
                new_y = grid_y + dy

                # circle brush
                if dx * dx + dy * dy <= brush_size * brush_size:

                    if (
                        0 <= new_x < COLS
                        and 0 <= new_y < ROWS
                    ):

                        grid[new_y][new_x] = current_element

    # RIGHT CLICK = ERASE
    if mouse_buttons[2]:

        for dy in range(-brush_size, brush_size + 1):

            for dx in range(-brush_size, brush_size + 1):

                new_x = grid_x + dx
                new_y = grid_y + dy

                # circle brush
                if dx * dx + dy * dy <= brush_size * brush_size:

                    if (
                        0 <= new_x < COLS
                        and 0 <= new_y < ROWS
                    ):

                        grid[new_y][new_x] = 0

    return (True, current_element, brush_size, simulation_speed)