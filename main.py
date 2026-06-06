from cell import create_cell
import pygame
from settings import *
from render import draw_grid
from simulation import update_simulation
from input_handler import handle_input
from temperature import update_temperature
from reactions import update_reactions

from save_load import save_world, load_world

from world_generation import generate_world
import random

pygame.init()

# BRUSH_SIZE = 2
brush_size = 2
current_element = SAND
simulation_speed = 3

frame_count = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Sandbox Game")

clock = pygame.time.Clock()

grid=[]


for row in range(ROWS):
    current_row= []

    for col in range(COLS):
        current_row.append(0)

    grid.append(current_row)

# Generate World
generate_world(grid)


# Load World
loaded_grid = load_world()

if loaded_grid is not None:
    grid = loaded_grid

show_temperature = False
show_wetness = False
show_stress = False

running = True
paused = False
step_frame = False
selected_cell = None


while running:
    



    clock.tick(60)
    frame_count += 1

    (running, current_element, brush_size, simulation_speed, show_temperature, paused, step_frame, selected_cell, show_wetness, show_stress )= handle_input(grid, current_element, brush_size, simulation_speed, show_temperature, paused, step_frame, selected_cell, show_wetness, show_stress)

    if (((not paused) and frame_count % simulation_speed == 0) or step_frame):

        # Random Rain
        if frame_count % 30 == 0:

            if random.random() < 0.2:
                rain_col = random.randint(0, COLS - 1)

                if grid[0][rain_col] == 0:
                    grid[0][rain_col] = create_cell(WATER)

        update_simulation(grid)
        for _ in range(3):
            update_temperature(grid)
        update_reactions(grid)
        step_frame = False
    # RENDER

    draw_grid(screen, grid, current_element, brush_size, simulation_speed, show_temperature, selected_cell, show_wetness, show_stress)
    pygame.display.update()

pygame.quit()