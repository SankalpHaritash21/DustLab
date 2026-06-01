import pygame

from settings import *
from materials import materials


def draw_grid(screen, grid, current_element, brush_size, simulation_speed):

    screen.fill((30, 30, 80))

    for row in range(ROWS):

        for col in range(COLS):
            cell= grid[row][col]
            if cell != 0:
                color = materials[cell]["color"]
                pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    material_name= materials[current_element]["name"]
    
    hud_text = (f"Material: {material_name} "
                 f"Brush Size: {brush_size} "
                 f"Simulation Speed: {simulation_speed}"
    )

    text_surface = pygame.font.SysFont("Arial", 18).render(hud_text, True, WHITE)
    screen.blit(text_surface, (10, 10))