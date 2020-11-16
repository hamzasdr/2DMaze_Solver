import pygame


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        # MIGHT BE IN HERE
        self.game.window.blit(self.game.bg, (0, 0))
        pygame.display.update()
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        if self.game.flag:
            self.mid_w, self.mid_h = self.game.infoObject.current_w / 2, self.game.infoObject.current_h / 2
        else:
            self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.quitx, self.quity = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        testX, testY = self.game.DISPLAY_W, self.game.DISPLAY_H
        if self.game.flag:
            testX, testY = self.game.infoObject.current_w, self.game.infoObject.current_h
        else:
            testX, testY = self.game.DISPLAY_W, self.game.DISPLAY_H
        self.mid_w, self.mid_h = testX / 2, testY / 2
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.quitx, self.quity = self.mid_w, self.mid_h + 70
        while self.run_display:
            self.game.check_events()
            self.move_cursor()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 20, testX / 2,
                                testY / 2 - 20)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Quit", 20, self.quitx, self.quity)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Quit':
                self.game.running = False
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Width'
        self.game.text = ''
        self.wx, self.wy = self.mid_w - 40, self.mid_h + 20
        self.hx, self.hy = self.mid_w - 40, self.mid_h + 40
        self.wix1, self.wih1 = self.mid_w + 10, self.mid_h + 10
        self.wix2, self.wih2 = self.mid_w + 10, self.mid_h + 30
        self.cursor_rect.midtop = (self.wx + self.offset, self.wy)
        self.base_font = pygame.font.Font('8-BIT WONDER.TTF', 10)
        self.user_width = '4'
        self.user_height = '4'
        self.input_rectw = pygame.Rect(self.wix1, self.wih1, 100, 22)
        self.input_recth = pygame.Rect(self.wix2, self.wih2, 100, 22)
        self.color = pygame.Color('lightgray')

    def display_menu(self):
        self.run_display = True
        testX, testY = self.game.DISPLAY_W, self.game.DISPLAY_H
        if self.game.flag:
            testX, testY = self.game.infoObject.current_w, self.game.infoObject.current_h
        else:
            testX, testY = self.game.DISPLAY_W, self.game.DISPLAY_H
        self.game.text = ''
        self.state = 'Width'
        self.mid_w, self.mid_h = testX / 2, testY / 2
        self.wx, self.wy = self.mid_w - 40, self.mid_h + 20
        self.hx, self.hy = self.mid_w - 40, self.mid_h + 40
        self.wix1, self.wih1 = self.mid_w + 10, self.mid_h + 10
        self.wix2, self.wih2 = self.mid_w + 10, self.mid_h + 30
        self.cursor_rect.midtop = (self.wx + self.offset, self.wy)
        self.input_rectw = pygame.Rect(self.wix1, self.wih1, 100, 22)
        self.input_recth = pygame.Rect(self.wix2, self.wih2, 100, 22)
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Options', 20, testX / 2, testY / 2 - 30)
            self.game.draw_text("Width", 15, self.wx, self.wy)
            pygame.draw.rect(self.game.display, self.color, self.input_rectw, 2)
            self.game.draw_text("Height", 15, self.hx, self.hy)
            pygame.draw.rect(self.game.display, self.color, self.input_recth, 2)
            text1 = self.base_font.render(self.user_width, True, (255, 255, 255))
            text2 = self.base_font.render(self.user_height, True, (255, 255, 255))
            self.game.display.blit(text1, (self.input_rectw.x + 45, self.input_rectw.y + 5))
            self.game.display.blit(text2, (self.input_recth.x + 45, self.input_recth.y + 5))
            self.draw_cursor()
            pygame.display.update()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Width':
                self.state = 'Height'
                self.game.text = ''
                self.cursor_rect.midtop = (self.hx + self.offset, self.hy)
            elif self.state == 'Height':
                self.state = 'Width'
                self.game.text = ''
                self.cursor_rect.midtop = (self.wx + self.offset, self.wy)
        elif self.game.TYPE:
            if self.state == 'Width':
                self.user_width = self.game.text
            elif self.state == 'Height':
                self.user_height = self.game.text
        elif self.game.DEL:
            if self.state == 'Width':
                self.user_width = self.game.text
            elif self.state == 'Height':
                self.user_height = self.game.text
