import pygame
import random

pygame.init()

# -------------------
# CONSTANTS
# -------------------

WIDTH = 800
HEIGHT = 600

CELL_SIZE = 10


ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE


BLACK= (0, 0, 0)
WHITE = (245, 235, 216) #(255, 255, 255)
BLUE = (0, 0, 255)
SAND= 1
WATER= 2





BRUSH_SIZE = 2

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

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_element = SAND
            elif event.key == pygame.K_2:
                current_element = WATER

    mouse_button= pygame.mouse.get_pressed()

    mouse_x, mouse_y = pygame.mouse.get_pos()

    grid_x = mouse_x // CELL_SIZE
    grid_y = mouse_y // CELL_SIZE

    if mouse_button[0]: # left click
        if 0 <= grid_x < COLS and 0 <= grid_y < ROWS:
            for dy in range(-BRUSH_SIZE, BRUSH_SIZE + 1):
                for dx in range(-BRUSH_SIZE, BRUSH_SIZE + 1):
                    new_x = grid_x + dx
                    new_y = grid_y + dy
                    if dx * dx + dy * dy <= BRUSH_SIZE * BRUSH_SIZE:  # Circle brush
                        if (0 <= new_x < COLS and 0 <= new_y < ROWS):
                            grid[new_y][new_x] = current_element

    if mouse_button[2]: # right click
        if 0 <= grid_x < COLS and 0 <= grid_y < ROWS:
            for dy in range(-BRUSH_SIZE, BRUSH_SIZE+1):
                for dx in range(-BRUSH_SIZE, BRUSH_SIZE+1):
                    new_x = grid_x + dx
                    new_y = grid_y + dy
                    if dx * dx + dy * dy <= BRUSH_SIZE * BRUSH_SIZE:  # Circle brush
                        if (0 <= new_x < COLS and 0 <= new_y < ROWS):
                            grid[new_y][new_x] = 0


    if frame_count % simulation_speed == 0:

    # Sand Simulation
        for row in range(ROWS - 2, -1, -1):
            for col in range(COLS):

                if grid[row][col]== SAND:
                    below = grid[row +1][col]

                    if below == 0:
                        grid[row][col]=0
                        grid[row +1][col]= SAND
                    elif below == WATER:
                        grid[row][col]= WATER
                        grid[row +1][col]= SAND
                    else:
                        direction = random.choice([-1, 1])
                        new_col = col + direction
                        if 0 <= new_col < COLS and grid[row +1][new_col] in [0, WATER]:
                            target = grid[row +1][new_col]
                            grid[row][col]= target
                            grid[row +1][new_col]= SAND

    # Water Simulation
        for row in range(ROWS - 2, -1, -1):
            for col in range(COLS):
                if grid[row][col]== WATER:
                    if grid[row +1][col]==0:
                        grid[row][col]=0
                        grid[row +1][col]= WATER
                    else:
                        directions = [-1, 1]
                        random.shuffle(directions)
                        moved = False

                        for direction in directions:
                            new_col = col + direction
                            if (0 <= new_col < COLS and grid[row +1][new_col]==0):
                                grid[row][col]=0
                                grid[row +1][new_col]= WATER
                                moved = True
                                break

                        # If water can't move down, try to move left or right
                        if not moved:
                            for direction in directions:
                                new_col= col+direction
                                if (0<=new_col < COLS and grid[row][new_col]==0):
                                    grid[row][col]=0
                                    grid[row][new_col]= WATER
                                    break

    # RENDER
    screen.fill((30, 30, 80))

    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == SAND:
                pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif grid[row][col] == WATER:
                pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.update()

pygame.quit()