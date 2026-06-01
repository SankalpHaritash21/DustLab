import pygame
import random
from settings import *
from render import draw_grid
from simulation import update_simulation
from input_handler import handle_input
from temprature import update_temperature
from reactions import update_reactions

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

running = True

while running:

    clock.tick(60)
    frame_count += 1

    (running, current_element, brush_size, simulation_speed )= handle_input(grid, current_element, brush_size, simulation_speed)

    if frame_count % simulation_speed == 0:
        update_simulation(grid)
        update_temperature(grid)
        update_reactions(grid)
    # RENDER
    draw_grid(screen, grid, current_element, brush_size, simulation_speed)
    pygame.display.update()

pygame.quit()