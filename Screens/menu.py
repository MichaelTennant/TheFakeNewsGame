"""
The menu screen for the fake news game, imported by __main__.py
"""

import pygame.color, pygame.mouse
from widgets import Button

from Screens import playgame, settings, about
from sys import exit

class GUI():
    def __init__(self, parent):
        self.parent = parent
        self.parent.display.set_caption("The Fake News Game - Menu")

        self.width, self.height = self.parent.window.get_size()

        # Create Title Object
        self.title_font = pygame.font.SysFont(".\\Assets\\Fonts\\PatrickHand-Regular.ttf", int(self.width/8))
        self.title_text = self.title_font.render("The Fake News Game", True, pygame.Color(51,51,51))

        self.title_rect = self.title_text.get_rect()
        self.title_rect.center = (self.width/2, self.height*0.09)

        # Create buttons
        self.new_game_btn = Button("Play", (self.width/2, self.height*0.28), self.width/1024, 4, "forward")
        self.settings_btn = Button("Settings", (self.width/2, self.height*0.48), self.width/1024, 4, "forward")
        self.about_btn = Button("About", (self.width/2, self.height*0.68), self.width/1024, 4, "forward")
        self.exit_btn = Button("Exit", (self.width/2, self.height*0.88), self.width/1024, 4, "forward")

    def update(self):
        self.parent.window.fill(pygame.Color(242,242,242))
        self.parent.window.blit(self.title_text, self.title_rect)

        x, y = pygame.mouse.get_pos()
        lmb = pygame.mouse.get_pressed()[0]

        # Get button updates
        if self.new_game_btn.update(self.parent, (x, y, lmb)) == 3:
            self.parent.screen = playgame.GUI(self.parent)

        if self.settings_btn.update(self.parent, (x, y, lmb)) == 3:
            self.parent.screen = settings.GUI(self.parent)

        if self.about_btn.update(self.parent, (x, y, lmb)) == 3:
            self.parent.screen = about.GUI(self.parent)

        if self.exit_btn.update(self.parent, (x, y, lmb)) == 3:
            exit()