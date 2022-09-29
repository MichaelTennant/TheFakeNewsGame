"""
The game screen for the fake news game, imported by __main__.py
"""

import pygame

class GUI():
    def __init__(self, parent):
        self.parent = parent
        self.parent.display.set_caption("The Fake News Game")

        self.width, self.height = self.parent.window.get_size()
    
    def update(self):
        self.parent.window.fill(pygame.Color(242,242,242))