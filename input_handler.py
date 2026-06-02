import pygame

from settings import *
from cell import create_cell
from materials import materials


def handle_input(grid, current_element, brush_size, simulation_speed, show_temperature, paused, step_frame, selected_cell):


    material_ids = list(materials.keys())


    # EVENTS

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            return (False, current_element, brush_size, simulation_speed, show_temperature, paused, step_frame, selected_cell)
        

        if event.type == pygame.KEYDOWN:

            current_index = material_ids.index(current_element)

            # Next Material
            if event.key == pygame.K_e:
                current_index =(current_index + 1) % len(material_ids)
                current_element = material_ids[current_index]

            # Previous Material
            elif event.key == pygame.K_q:
                current_index =(current_index - 1) % len(material_ids)
                current_element = material_ids[current_index]

            # Temperature View
            elif event.key == pygame.K_t:
                show_temperature = (not show_temperature)

            # Pause/ Unpause
            elif event.key == pygame.K_SPACE:
                paused = (not paused)
            
            # Step Frame
            elif event.key == pygame.K_n:
                step_frame = True


            elif event.key == pygame.K_1:
                current_element = SAND
            elif event.key == pygame.K_2:
                current_element = WATER
            elif event.key == pygame.K_3:
                current_element = LAVA
            elif event.key == pygame.K_4:
                current_element = OIL
            elif event.key == pygame.K_5:
                current_element = STONE
            elif event.key == pygame.K_6:
                current_element = FIRE
            elif event.key == pygame.K_7:
                current_element = SMOKE
            elif event.key == pygame.K_8:
                current_element = STEAM

            elif event.key == pygame.K_UP:
                brush_size += 1
            elif event.key == pygame.K_DOWN:
                brush_size = max(1, brush_size - 1)
            elif event.key == pygame.K_RIGHT:
                simulation_speed = max(1, simulation_speed - 1)
            elif event.key == pygame.K_LEFT:
                simulation_speed += 1

            # Clear Screen
            elif event.key == pygame.K_c:
                for row in range(ROWS): 
                    for col in range(COLS): 
                        grid[row][col] = 0

        elif event.type == pygame.MOUSEWHEEL:
            current_index = material_ids.index(current_element)

            # Scroll Up
            if event.y > 0:
                current_index =(current_index + 1) % len(material_ids)
            
            # Scroll Down
            elif event.y < 0:
                current_index =(current_index - 1) % len(material_ids)

            current_element = material_ids[current_index]

        # Material Bar Click Selection

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left Click
                mouse_x, mouse_y = event.pos

                bar_height = 50

                if mouse_y > HEIGHT - bar_height:  # Assuming material bar is at the bottom 50 pixels
                    material_width = WIDTH // len(material_ids)
                    clicked_index = mouse_x // material_width

                    if clicked_index < len(material_ids):
                        current_element = material_ids[clicked_index]
                
            elif event.button == 2:  # Middle Click
                mouse_x, mouse_y = event.pos
                grid_x = mouse_x // CELL_SIZE
                grid_y = mouse_y // CELL_SIZE

                if (0 <= grid_x < COLS and 0 <= grid_y < ROWS):
                    selected_cell = (grid_x, grid_y)

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
                        if current_element == LAVA:
                            grid[new_y][new_x] = create_cell(current_element, 1500)
                        elif current_element == FIRE:
                            fire= create_cell(current_element, 300)
                            fire["lifetime"] = 80
                            grid[new_y][new_x] = fire
                        else:
                            grid[new_y][new_x] = create_cell(current_element)

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

    return (True, current_element, brush_size, simulation_speed, show_temperature, paused, step_frame, selected_cell)