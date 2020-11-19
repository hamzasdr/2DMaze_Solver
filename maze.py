import sys

sys.setrecursionlimit(10000)
import pygame
import random
from queue import PriorityQueue
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LORANGE = (255, 153, 0)  # (255, 204, 203)
clock = pygame.time.Clock()


class Cell:
    def __init__(self):
        self.parent = (-1, -1)
        self.f, self.g, self.h = sys.maxsize, sys.maxsize, sys.maxsize


def generate_maze(place, wall, screen, length, width, space, px, py):
    i = 0
    j = 0
    place[i][j] = 1

    done = False

    while not done:

        direction = random.randint(0, 3)  # 0:up 1:down 2:left 3:right.
        if direction == 0 and j != 0 and place[i][j - 1] == 0:
            pygame.draw.line(screen, BLACK, [space * i + px + 2, space * j + py],
                             [space * i + px - 1 + space, space * j + py], 2)
            wall[i][j][0] = 0
            j = j - 1
            place[i][j] = 1
            wall[i][j][1] = 0
        elif direction == 1 and j != width - 1 and place[i][j + 1] == 0:
            pygame.draw.line(screen, BLACK, [space * i + px + 2, space * j + py + space],
                             [space * i + px - 1 + space, space * j + py + space], 2)
            wall[i][j][1] = 0
            j = j + 1
            place[i][j] = 1
            wall[i][j][0] = 0
        elif direction == 2 and i != 0 and place[i - 1][j] == 0:
            pygame.draw.line(screen, BLACK, [space * i + px, space * j + py + 2],
                             [space * i + px, space * j + py - 1 + space], 2)
            wall[i][j][2] = 0
            i = i - 1
            place[i][j] = 1
            wall[i][j][3] = 0
        elif i != length - 1 and place[i + 1][j] == 0:
            pygame.draw.line(screen, BLACK, [space * i + px + space, space * j + py + 2],
                             [space * i + px + space, space * j + py - 1 + space], 2)
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

    pygame.draw.rect(screen, GREEN, [px + 2 + start_i * space, py + 2 + start_j * space, space - 2, space - 2], 0)

    dest_i = random.randint(0, length - 1)
    dest_j = random.randint(0, width - 1)
    pygame.draw.rect(screen, RED, [px + 2 + dest_i * space, py + 2 + dest_j * space, space - 2, space - 2], 0)
    pygame.display.flip()
    return [start_i, start_j, dest_i, dest_j]


def Manhattan_dist(start, dist):
    start_i, start_j = start
    dist_i, dist_j = dist
    x = start_i - dist_i
    y = start_j - dist_j
    H = abs(x) + abs(y)

    return H


def find_element(list, element):
    i, j = element
    for tuple in list.queue:
        if tuple[1] == i and tuple[2] == j:
            return True
    return False


def solve_maze(game, coordinates, wall, px, py):
    start_i, start_j, dest_i, dest_j = coordinates
    space = game.space
    length = int(game.options.user_width)
    width = int(game.options.user_height)
    solution = A_star(wall, (start_i, start_j), (dest_i, dest_j), (width, length))
    # print(solution)
    solution = reversed(solution)
    time.sleep(0.5)
    for i, j in solution:
        pygame.draw.rect(game.window, GREEN, [px + 2 + i * space, py + 2 + j * space, space - 2, space - 2], 0)
        pygame.display.flip()
        clock.tick(15)
        pygame.draw.rect(game.window, LORANGE, [px + 2 + i * space, py + 2 + j * space, space - 2, space - 2], 0)
        pygame.display.flip()


def get_path(cellDetails, dist):
    i, j = dist
    path = []
    while not ((cellDetails[i][j].parent[0] == i) and (cellDetails[i][j].parent[1] == j)):
        path.append((i, j))
        t_i, t_j = i, j
        i = cellDetails[t_i][t_j].parent[0]
        j = cellDetails[t_i][t_j].parent[1]
    path.append((i, j))
    return path


def A_star(wall, src, dist, size):
    width, length = size
    start_i, start_j = src
    dist_i, dist_j = dist

    if start_i == dist_i and start_j == dist_j:
        print("Done")
        return []

    closed = [[False for i in range(width)] for j in range(length)]
    open = PriorityQueue()
    cells = [[Cell() for i in range(width)] for j in range(length)]

    cells[start_i][start_j].f = 0
    cells[start_i][start_j].g = 0
    cells[start_i][start_j].h = 0
    cells[start_i][start_j].parent = (start_i, start_j)

    open.put((0, start_i, start_j))
    while not open.empty():
        cell = open.get()
        i, j = cell[1], cell[2]
        if i == dist_i and j == dist_j:
            path = get_path(cells, dist)
            return path
        closed[i][j] = True
        for direction in range(0, 4):
            temp_i, temp_j = -1, -1
            if wall[i][j][direction]:
                continue
            else:
                if direction == 0:
                    temp_i, temp_j = i, j - 1
                elif direction == 1:
                    temp_i, temp_j = i, j + 1
                elif direction == 2:
                    temp_i, temp_j = i - 1, j
                elif direction == 3:
                    temp_i, temp_j = i + 1, j
            temp_g = cells[i][j].g + 1
            temp_h = Manhattan_dist((temp_i, temp_j), (dist_i, dist_j))
            temp_f = temp_g + temp_h
            if (not closed[temp_i][temp_j] and not find_element(open, (temp_i, temp_j))) or cells[temp_i][
                temp_j].f > temp_f:
                open.put((temp_f, temp_i, temp_j))
                cells[temp_i][temp_j].g = cells[i][j].g + 1
                cells[temp_i][temp_j].h = Manhattan_dist((temp_i, temp_j), (dist_i, dist_j))
                cells[temp_i][temp_j].f = cells[temp_i][temp_j].h + cells[temp_i][temp_j].g
                # print("new cell : ",i,j,"-->",temp_i,temp_j)
                cells[temp_i][temp_j].parent = (i, j)
                # closed[temp_i][temp_j] = False
    print("Failed to find the Destination Cell")
    return []
