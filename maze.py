import itertools
import sys
sys.setrecursionlimit(10000)
import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)



def generate_maze(place ,wall,screen,length,width,space):
    i = 0
    j = 0
    place[i][j] = 1

    done = False

    while not done:

        direction = random.randint(0, 3)  # 0:up 1:down 2:left 3:right.
        if direction == 0 and j != 0 and place[i][j - 1] == 0:
            pygame.draw.line(screen, WHITE, [space * i + 102, space * j + 100],
                             [space * i + 99 + space, space * j + 100], 2)
            wall[i][j][0] = 0
            j = j - 1
            place[i][j] = 1
            wall[i][j][1] = 0
        elif direction == 1 and j != width - 1 and place[i][j + 1] == 0:
            pygame.draw.line(screen, WHITE, [space * i + 102, space * j + 100 + space],
                             [space * i + 99 + space, space * j + 100 + space], 2)
            wall[i][j][1] = 0
            j = j + 1
            place[i][j] = 1
            wall[i][j][0] = 0
        elif direction == 2 and i != 0 and place[i - 1][j] == 0:
            pygame.draw.line(screen, WHITE, [space * i + 100, space * j + 102],
                             [space * i + 100, space * j + 99 + space], 2)
            wall[i][j][2] = 0
            i = i - 1
            place[i][j] = 1
            wall[i][j][3] = 0
        elif i != length - 1 and place[i + 1][j] == 0:
            pygame.draw.line(screen, WHITE, [space * i + 100 + space, space * j + 102],
                             [space * i + 100 + space, space * j + 99 + space], 2)
            wall[i][j][3] = 0
            i = i + 1
            place[i][j] = 1
            wall[i][j][2] = 0

        newplace = 0

        if ((i == 0 and j == 0 and place[i + 1][j] == 1 and place[i][j + 1] == 1)
                or (i == length - 1 and j == 0 and place[i - 1][j] == 1 and place[i][j + 1] == 1)
                or (i == 0 and j == width - 1 and place[i][j - 1] == 1 and place[i + 1][j] == 1)
                or (i == length - 1 and j == width - 1 and place[i][j - 1] == 1 and place[i - 1][j] == 1)
                or (i == 0 and place[i][j - 1] == 1 and place[i + 1][j] == 1 and place[i][j + 1] == 1)
                or (i == length - 1 and place[i][j - 1] == 1 and place[i - 1][j] == 1 and place[i][j + 1] == 1)
                or (j == width - 1 and place[i - 1][j] == 1 and place[i][j - 1] == 1 and place[i + 1][j] == 1)
                or (j == 0 and place[i - 1][j] == 1 and place[i][j + 1] == 1 and place[i + 1][j] == 1)):
            newplace = 1
        elif i != 0 and j != 0 and i != length - 1 and j != width - 1 and place[i][j - 1] == 1 and place[i][
            j + 1] == 1 and place[i - 1][j] == 1 and place[i + 1][j] == 1:
            newplace = 1

        find_place = False
        if newplace == 1:
            while not find_place:
                i = random.randint(0, length - 1)
                j = random.randint(0, width - 1)
                if place[i][j]:
                    find_place = True

        pygame.display.flip()
        sum = 0
        for x in range(length):
            for y in range(width):
                sum = sum + place[x][y]
        if sum == width * length:
            done = True

    start_i = random.randint(0, length - 1)
    start_j = random.randint(0, width - 1)

    pygame.draw.rect(screen, RED, [102 + start_i * space, 102 + start_j * space, space - 2, space - 2], 0)

    dest_i = random.randint(0, length - 1)
    dest_j = random.randint(0, width - 1)
    pygame.draw.rect(screen, GREEN, [102 + dest_i * space, 102 + dest_j * space, space - 2, space - 2], 0)
    pygame.display.flip()
    return start_i , start_j , dest_i , dest_j


#TODO: implement A* Algorithm
def solve_maze():
    pass



