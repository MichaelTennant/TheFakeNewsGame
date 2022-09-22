#!.\pythonw.exe

"""
This is a simple game where involving stoping the spread of fake news as quickly 
as possible by adding and removing edges. The faster you stop the spread and the 
least edges you add and remove, the higher your score.

Current ver 0.0.2
"""

import os
import pygame
from py_singleton import singleton
import sys

import inputs
from Screens import game, menu, settings

@singleton # Only one instance of a singleton class can be running at a time
class App():
    def __init__(self):
        # Setup window
        pygame.init()
        pygame.mixer.init()

        self.display = pygame.display
        self.display.set_caption("The Fake News Game")
        self.window = self.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()

        self.icon = pygame.image.load(".\\Assets\\Icons\\512.png")
        pygame.display.set_icon(self.icon)

        self.screen = menu.GUI(self)

        self.mainloop()
        sys.exit()


    def mainloop(self):
        while True:

            # Get inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            # Update screen
            self.screen.update()
            self.display.flip()

            # Set refresh rate to 30fps
            self.clock.tick(30)

if __name__ == "__main__":
    app = App()