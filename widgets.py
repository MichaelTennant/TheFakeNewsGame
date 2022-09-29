"""
This is a library containing widgets including the Button object for the UI of the game.
"""

import pygame
pygame.mixer.init()

class Button():
    def __init__(self, text, position, magnification, btn_type, sound):
        self.pressed = 0 # 0 = Unpressed, 1 = Pressed this tick, 2 = Pressed before this tick 3 = Released
        self.sound = pygame.mixer.Sound(f".\\Assets\\Audio\\{sound}.wav")
        
        # Load button graphics
        raw_size =  pygame.image.load(f".\\Assets\\GUI\\btn{btn_type}.png").get_size()

        self.unpressed_graphic = pygame.transform.scale(pygame.image.load(f".\\Assets\\GUI\\btn{btn_type}.png"), (raw_size[0]*magnification, raw_size[1]*magnification))
        self.pressed_graphic = pygame.transform.scale(pygame.image.load(f".\\Assets\\GUI\\btn{btn_type}_pressed.png"), (raw_size[0]*magnification, raw_size[1]*magnification))

        width, height = self.unpressed_graphic.get_size()
        self.hitbox = ((position[0]-width//2, position[1]-height//2), (position[0]+width//2, position[1]+height//2))

        # Load text object
        self.font = pygame.font.SysFont(".\\Assets\\Fonts\\PatrickHand-Regular.ttf", int(width/6))
        self.text = self.font.render(text, True, pygame.Color(51,51,51))

        self.text_rect = self.text.get_rect()
        self.text_rect.center = position

        self.text_rect_pressed = self.text.get_rect()
        self.text_rect_pressed.center = (position[0], position[1] - int(8*magnification))

    def update(self, parent, mouse_state): # mouse_state = (x, y, lmb_down)

        # Check if button is being pressed
        if self.hitbox[0][0] < mouse_state[0] and mouse_state[0] <= self.hitbox[1][0] and self.hitbox[0][1] < mouse_state[1] and mouse_state[1] <= self.hitbox[1][1]:
            if mouse_state[2] and not self.pressed:
                self.pressed = 1
                self.sound.play()

            elif mouse_state[2]:
                self.pressed = 2
            
            elif self.pressed == 1 or self.pressed == 2:
                self.pressed = 3
                
            else: self.pressed = 0
        else: self.pressed = 0

        # Draw button graphic to screen
        if self.pressed:
            parent.window.blit(self.pressed_graphic, self.hitbox[0])
            parent.window.blit(self.text, self.text_rect)
        else:
            parent.window.blit(self.unpressed_graphic, self.hitbox[0])
            parent.window.blit(self.text, self.text_rect_pressed)

        return self.pressed