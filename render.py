import pygame

from settings import *


def draw_grid(screen, grid, current_element, brush_size, simulation_speed):

    screen.fill((30, 30, 80))

    for row in range(ROWS):

        for col in range(COLS):

            if grid[row][col] == SAND:

                pygame.draw.rect(
                    screen,
                    WHITE,
                    (
                        col * CELL_SIZE,
                        row * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                )

            elif grid[row][col] == WATER:

                pygame.draw.rect(
                    screen,
                    BLUE,
                    (
                        col * CELL_SIZE,
                        row * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                )
    
    material_name = "SAND"

    if current_element == WATER:
        material_name = "WATER"
    
    hud_text = (f"Material: {material_name} "
                 f"Brush Size: {brush_size} "
                 f"Simulation Speed: {simulation_speed}"
    )

    text_surface = pygame.font.SysFont("Arial", 18).render(hud_text, True, WHITE)
    screen.blit(text_surface, (10, 10))