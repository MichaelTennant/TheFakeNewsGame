# #!/bin/env python3

"""
Version: 0.1.6

CONTROLS
LEFT to step foward
RIGHT to step back

F1 to show stats
E to export to vector

# Not implememted - Z to make a new node
# Not implememted - X to delete a node
# Not implememted - C to make a new edge
# Not implememted - V to delete an edge

TODO
 - If changes made while not at latest state, delete future states
 - Add torus node generation
 - Add random node generation
 - Add settings and saves menu
 - Safe and Load files
"""

import pygame
import simulation
from sys import argv, exit, platform

class App():
    def __init__(self, savefile=None):
        # Initialize pygame window
        pygame.init()
        pygame.font.init()

        self.display = pygame.display
        self.display.set_caption("Fake-News Simulator")
        
        self.resizeable = platform == "win32"
        with open("settings.csv", "r") as cfg:
            cfg_size = cfg.readlines()[2].replace("\n", "").split(",")
        self.window = self.display.set_mode((int(cfg_size[1]), (int(cfg_size[2]))), pygame.RESIZABLE if self.resizeable else 0)
        
        self.clock = pygame.time.Clock()

        self.icon = pygame.image.load("./Assets/Icons/ems.ico")
        pygame.display.set_icon(self.icon)
        
        # Declare some useful vars
        self.savefile = savefile
        self.font_light = pygame.font.SysFont("./Assets/Fonts/MotivaSansLight.woff.ttf", 20)
        self.screen = simulation.GUI(self)
        
        self.mainloop()
        exit()

    def mainloop(self):
        while True:

            # Get inputs
            self.pressed, self.released = None, None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                
                # Set window minimum size (Only used in windows 10/11)
                elif event.type == pygame.VIDEORESIZE:
                    width, height = event.size
                    if width < 480:
                        width = 480
                    if height < 360:
                        height = 360
                    self.window = pygame.display.set_mode((width,height), pygame.RESIZABLE)

                # Record key presses
                elif event.type == pygame.KEYDOWN:
                    self.pressed = event.key
                elif event.type == pygame.KEYUP:
                    self.released = event.key

            # Update screen and inputs
            self.screen.update()
            self.display.flip()

            # Set refresh rate to 60fps
            self.clock.tick(60)

# Run app
if __name__ == "__main__":
    App(argv[1] if len(argv) > 1 else "")