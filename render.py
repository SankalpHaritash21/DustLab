import random
import math

import pygame
import time

from settings import *
from materials import materials
from simulation_utils import get_gas_pressure, get_local_weight


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

def apply_temperature_tint(color, temperature):

    # Normal Room Temp.

    if temperature <= 20:
        return color

    # HEAT GLOW
    if temperature == float("inf"):
        temperature = 2000
        
    heat= min(255, int((temperature - 20) * 2))
    
    r = min(255, color[0] + heat)
    g = min(255, color[1] + heat // 3)
    b = max(0, color[2] - heat // 2)
    
    return (r, g, b)

def temperature_to_color(temperature):

    # clamp
    temperature = max(0, min(temperature, 1000))

    # cold -> blue
    if temperature < 100:
        blue = 100 + int( temperature * 1.5)
        blue = min(255, blue)
        return (0, 0, blue)
    
    # warm -> yellow
    elif temperature < 300:
        return (255, 255, 0)
    
    # hot -> red
    else:
        return (255, 0, 0)


def draw_grid(screen, grid, current_element, brush_size, simulation_speed, show_temperature, selected_cell, show_wetness, show_stress):


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

                    if "wetness" in cell_data:
                        wetness = cell_data["wetness"]

                        # Darken wet sand
                        darkness = int(wetness * 0.8)

                        color = (
                            max(0, color[0] - darkness),
                            max(0, color[1] - darkness),
                            max(0, color[2] - darkness)
                        )

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

                elif cell == WATER:
                    color = base_color

                    if "foam" in cell_data:

                        if cell_data["foam"] > 0:

                            color = (220, 220, 255)
                else:
                    color = base_color

                if near_fire and cell not in [FIRE, LAVA]:
                    color = apply_glow(color, 25)

                
                temperature= cell_data["temperature"]

                # debug temperature view
                if show_temperature:
                    color = temperature_to_color(temperature)

                elif show_wetness:

                    if "wetness" in cell_data:

                        wetness = cell_data["wetness"]

                        blue_strength=  int((wetness/100)* 255)

                        color= (
                            max(0, color[0] - blue_strength // 3),
                            max(0, color[1] - blue_strength // 3),
                            min(255, color[2] + blue_strength)
                        )
                
                elif show_stress:
                    weight = get_local_weight(grid, row, col)

                    if weight <= 1:
                        color = (0, 255, 0)      # safe

                    elif weight <= 3:
                        color = (255, 255, 0)    # stressed

                    else:
                        color = (255, 0, 0)      # dangerous
                    

                # Normal Rendering
                else:
                    color= apply_temperature_tint(color, temperature)

                pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    material_name= materials[current_element]["name"]
    
    hud_text = (f"Material: {material_name} "
                 f"Brush Size: {brush_size} "
                 f"Simulation Speed: {simulation_speed}"
    )

    text_surface = pygame.font.SysFont("Arial", 18).render(hud_text, True, WHITE)
    screen.blit(text_surface, (10, 10))
    draw_material_bar( screen, current_element)



    # Particle Inspection
    if selected_cell is not None:
        x, y = selected_cell
        cell_data = grid[y][x]

        if cell_data != 0:
            material_id = cell_data["material"]
            material_name = materials[material_id]["name"]
            

            info_lines = [
                f"Material: {material_name}",
                f"Temperature: {int(cell_data['temperature'])}°C",
            ]

            weight = get_local_weight(grid, y, x)
            info_lines.append(f"Weight: {weight}")

            if materials[material_id]["type"] == "gas":
                pressure = get_gas_pressure(grid, y, x)
                info_lines.append(f"Pressure: {pressure}")

            # Optional METADATA

            for key, value in cell_data.items():
                if key not in ["material", "temperature"]:
                    info_lines.append(f"{key.capitalize()}: {value}")

            # Draw Panel

            panel_x= 10
            panel_y= 40

            for index, line in enumerate(info_lines):
                text_surface = pygame.font.SysFont("Arial", 18).render(line, True, WHITE)
                screen.blit(text_surface, (panel_x, panel_y + index * 20))



def draw_material_bar(screen, current_element):

    bar_height = 50
    y= HEIGHT - bar_height

    material_width = WIDTH // len(materials)
    font = pygame.font.SysFont("Arial", 16)

    for index, material_id in enumerate(materials):
        material = materials[material_id]
        color = material["color"]

        x= index * material_width

        rect= pygame.Rect(x, y, material_width, bar_height)
        pygame.draw.rect(screen, color, rect)

        # Selected Material Border
        if material_id == current_element:
            pygame.draw.rect(screen, WHITE, rect, 4)

        # Material Name
        text_surface = font.render(material["name"], True, BLACK)
        text_rect= text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)