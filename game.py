# x = 0
# y = 30
# import os

# os.environ['SDL_VIDEO_CENTERED'] = '0'
# os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

import pygame
from maze import *
from menu import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LGRAY = (210, 210, 210)


class Game:
    def __init__(self):
        pygame.init()
        self.bg = pygame.image.load("bg.png")
        self.flag = 0
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.TYPE, self.DEL = False, False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 512, 512
        self.space = 15
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.font_name = '8-BIT WONDER.TTF'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.text = '4'
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.curr_menu = self.main_menu
        self.infoObject = pygame.display.Info()

    def game_loop(self):
        length = int(self.options.user_width)
        width = int(self.options.user_height)

        px, py = self.init_maze(length, width)
        pygame.display.flip()
        place = [[0 for y in range(width)] for x in range(length)]
        wall = [[[1 for z in range(4)] for y in range(width)] for x in range(length)]

        coordinates = generate_maze(place, wall, self.window, length, width, self.space, px, py)
        solve_maze(self, coordinates, wall, px, py)

        while self.playing:
            self.check_events()
            if self.START_KEY:
                return
            elif self.BACK_KEY:
                self.playing = False
                if self.flag:
                    self.infoObject = pygame.display.Info()
                    self.window = pygame.display.set_mode((self.infoObject.current_w, self.infoObject.current_h),
                                                          pygame.FULLSCREEN)
                else:
                    self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.DEL = True
                    self.text = self.text[:-1]
                else:
                    self.TYPE = True
                    self.text += event.unicode

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.TYPE, self.DEL = False, False, False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def init_maze(self, length, width):
        sizex = 200 + int(self.options.user_width) * self.space
        sizey = 200 + int(self.options.user_height) * self.space
        coordx = 256 - (sizex - 199) / 2
        coordy = 256 - (sizey - 199) / 2
        wid = self.DISPLAY_W
        hie = self.DISPLAY_H
        if (sizex, sizey) > (wid, hie):
            wid = wid * 2
            hie = int(hie * 1.4)
            self.flag = 1
            coordx = (wid / 2) - ((sizex - 199) / 2)
            coordy = (hie / 2) - ((sizey - 199) / 2) + 25
        else:
            self.flag = 0

        if self.flag:
            self.window = pygame.display.set_mode((wid, hie), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((wid, hie))

        self.window.fill(BLACK)
        pygame.draw.rect(self.window, WHITE, [coordx, coordy, sizex - 199, sizey - 199], 2)
        pygame.display.flip()
        for x in range(length):
            pygame.draw.line(self.window, LGRAY, [(x * self.space + coordx), coordy],
                             [(x * self.space + coordx), coordy + (sizey - 199)],
                             2)  # Vertical lines.
        for x in range(width):
            pygame.draw.line(self.window, LGRAY, [coordx, (x * self.space + coordy)],
                             [coordx + (sizex - 199), (x * self.space + coordy)],
                             2)  # Horizontal lines.
        return coordx, coordy


g = Game()

while g.running:
    g.curr_menu.display_menu()
    if g.playing:
        g.game_loop()
