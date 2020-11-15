import time

import pygame
from maze import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

pygame.init()

space = 30
length = 5
width = 5

sizex = 200 + length * space
sizey = 200 + width * space

size = (sizex, sizey)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze2D")

# clock = pygame.time.Clock()
screen.fill(WHITE)

pygame.draw.rect(screen, BLACK, [100, 100, sizex - 200, sizey - 200], 2)

pygame.display.flip()

for x in range(length):
    pygame.draw.line(screen, BLACK, [(x * space + 100), 100], [(x * space + 100), sizey - 100], 2)  # Vertical lines.
for x in range(width):
    pygame.draw.line(screen, BLACK, [100, (x * space + 100)], [sizex - 100, (x * space + 100)], 2)  # Horizontal lines.

pygame.display.flip()
place = [[0 for y in range(width)] for x in range(length)]
wall = [[[1 for z in range(4)] for y in range(width)] for x in range(length)]

start_i, start_j, dest_i, dest_j = generate_maze(place, wall, screen, length, width)

pygame.display.flip()
time.sleep(10)

solve_maze()
