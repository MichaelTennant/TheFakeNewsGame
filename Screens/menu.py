"""
The menu screen for the fake news game, imported by __main__.py
"""

import pygame.color, pygame.mouse
from widgets import Button

class GUI():
    def __init__(self, parent):
        self.parent = parent
        self.parent.display.set_caption("The Fake News Game - Menu")

        self.width, self.height = self.parent.window.get_size()

        # Create Title Object
        self.title_font = pygame.font.SysFont(".\\Assets\\Fonts\\PatrickHand-Regular.ttf", int(self.width/8))
        self.title_text = self.title_font.render("The Fake News Game", True, pygame.Color(51,51,51))

        self.title_rect = self.title_text.get_rect()
        self.title_rect.center = (self.width/2, self.height/12)

        # Create button
        self.new_game_btn = Button("New Game", (self.width/2, self.height/4), 0.6, 4, "forward")

    def update(self):
        self.parent.window.fill(pygame.Color(242,242,242))
        self.parent.window.blit(self.title_text, self.title_rect)

        x, y = pygame.mouse.get_pos()
        lmb = pygame.mouse.get_pressed()[0]

        new_game_button_result =  self.new_game_btn.update(self.parent, (x, y, lmb))
        if new_game_button_result == 1:
            print("Pressed")
        

