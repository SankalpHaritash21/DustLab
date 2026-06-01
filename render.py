import random
import math

import pygame
import time

from settings import *
from materials import materials


def vary_color(color, variation, row, col):
    
    seed = (row * 928371 + col * 12377) % variation

    r = max(0, min(255, color[0] + seed - variation // 2))
    g = max(0, min(255, color[1] + seed - variation // 2))
    b = max(0, min(255, color[2] + seed - variation // 2))

    return (r, g, b)


def animate_fire_color(base_color, speed=5, intensity=40, row=0, col=0):

    t= time.time() * speed

    flicker= int( math.sin(t + row + col ) * intensity)

    r= max(0, min(255, base_color[0] + flicker))
    g= max(0, min(255, base_color[1] + flicker))
    b= max(0, min(255, base_color[2]))

    return (r, g, b)

def apply_glow(color, glow_strength):
    r = min(255, color[0] + glow_strength)
    g = min(255, color[1] + glow_strength)
    b = min(255, color[2] + glow_strength)

    return (r, g, b)

def draw_grid(screen, grid, current_element, brush_size, simulation_speed):

    screen.fill((30, 30, 80))

    for row in range(ROWS):

        for col in range(COLS):
            cell_data= grid[row][col]
            if cell_data != 0:
                cell = cell_data["material"]
                base_color = materials[cell]["color"]
                near_fire = False

                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx= col + dx
                        ny= row + dy

                        if (0<= nx<COLS and 0<=ny<ROWS):
                            neighbor_data= grid[ny][nx]
                            if ( neighbor_data != 0 and neighbor_data["material"] in [FIRE, LAVA] ):
                                near_fire = True
                                

                if cell == SAND:
                    color = vary_color(base_color, 20, row, col)

                elif cell == STONE:
                    color = vary_color(base_color, 15, row, col)

                elif cell == SMOKE:
                    color = vary_color(base_color, 10, row, col)

                elif cell == FIRE:
                    color = animate_fire_color(base_color, row=row, col=col)

                elif cell == LAVA:
                    color = animate_fire_color(base_color, speed=2, intensity=25, row=row, col=col)

                elif cell == STEAM:
                    color = vary_color(base_color, 5, row, col)

                else:
                    color = base_color

                if near_fire and cell not in [FIRE, LAVA]:
                    color = apply_glow(color, 25)

                pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    material_name= materials[current_element]["name"]
    
    hud_text = (f"Material: {material_name} "
                 f"Brush Size: {brush_size} "
                 f"Simulation Speed: {simulation_speed}"
    )

    text_surface = pygame.font.SysFont("Arial", 18).render(hud_text, True, WHITE)
    screen.blit(text_surface, (10, 10))