"""

"""

import pygame

class Button():
    def __init__(self, text, position, size):
        self.text = text
        self.position = position
        self.size = size

        self.state = 0
        self.graphic = pygame.image.load(".\\Assets\\GUI\\"+str(int(size[0]/size[1]))+"btn.png").convert()
        self.bounds = ((self.position[0]-self.graphic.get_width()/2, self.position[1]-self.graphic.get_height()/2), 
                       (self.position[0]+self.graphic.get_width()/2, self.position[1]+self.graphic.get_height()/2))

    def update(self, parent, x, y, lmb):
        if self.bounds[0][0] < x and x < self.bounds[1][0] and self.bounds[0][1] < y and y < self.bounds [1][1]:
            if lmb:

                if self.state != 2:
                    self.graphic = pygame.image.load(".\\Assets\\GUI\\"+str(int(self.size[0]/self.size[1]))+"btn_pressed_highlighted.png").convert()
                    self.state = 2

                    parent.window.blit(self.graphic, self.position)
                    return True

                parent.window.blit(self.graphic, self.position)
                return False

            if self.state != 1:
                self.graphic = pygame.image.load(".\\Assets\\GUI\\"+str(int(self.size[0]/self.size[1]))+"btn_highlighted.png").convert()
                self.state = 1

            parent.window.blit(self.graphic, self.position)
            return False

        if self.state != 0:
            self.graphic = pygame.image.load(".\\Assets\\GUI\\"+str(int(self.size[0]/self.size[1]))+"btn.png").convert()
            self.state = 0
            
        parent.window.blit(self.graphic, self.position)
        return False