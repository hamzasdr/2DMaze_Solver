import pygame
from menu import *
from maze import *
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Game:
    def __init__(self):
        pygame.init()
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

    # toDo: generate maze in here
    def game_loop(self):
        sizex = 200 + int(self.options.user_height) * self.space
        sizey = 200 + int(self.options.user_width) * self.space
        length = int(self.options.user_height)
        width = int(self.options.user_width)
        self.window = pygame.display.set_mode((sizex, sizey))
        self.window.fill(WHITE)
        pygame.draw.rect(self.window, BLACK, [100, 100, sizex - 199, sizey - 199], 2)
        pygame.display.flip()
        for x in range(length):
            pygame.draw.line(self.window, BLACK, [(x * self.space + 100), 100], [(x * self.space + 100), sizey - 100],2)  # Vertical lines.
        for x in range(width):
            pygame.draw.line(self.window, BLACK, [100, (x * self.space + 100)], [sizex - 100, (x * self.space + 100)],2)  # Horizontal lines.

        pygame.display.flip()
        place = [[0 for y in range(width)] for x in range(length)]
        wall = [[[1 for z in range(4)] for y in range(width)] for x in range(length)]

        start_i, start_j, dest_i, dest_j = generate_maze(place, wall, self.window, length, width,self.space)
        # pygame.display.flip()

        while self.playing:
            self.check_events()
            if self.START_KEY:
                return
            elif self.BACK_KEY:
                self.playing = False
                self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
            # self.display.fill(self.BLACK)
            # self.draw_text('MAZE should be in here', 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2)
            # self.window.blit(self.display, (0, 0))
            # pygame.display.update()
            # self.reset_keys()

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


g = Game()

while g.running:
    g.curr_menu.display_menu()
    if g.playing:
        g.game_loop()