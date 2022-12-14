#!/bin/env python3

import os
import pygame
import utils
from simulate import State, Node
# from widgets import Button, Slider

class GUI():
    def __init__(self, parent):
        self.parent = parent
        self.parent.display.set_caption("Fake-News Simulator")

        self.width, self.height = self.parent.display.get_window_size()
        self.mouse_occupied = [None, 0, 0]
        
        with open("settings.csv", "r") as cfg:
            cfg_sim = eval(cfg.readlines()[4].replace("Simulation", '"Simulation"').replace("\n", ""))
        self.state = [0, State().grid_generate(cfg_sim[1], cfg_sim[2], cfg_sim[3], cfg_sim[4], cfg_sim[5], (self.width, self.height))]


        self.state_history = [self.state[1].__copy__()]

        self.infected_node_img = utils.fill(pygame.transform.scale(pygame.image.load("./Assets/GUI/node.png"), (32,32)), utils.get_color(4))
        self.uninfected_node_img = utils.fill(pygame.transform.scale(pygame.image.load("./Assets/GUI/node.png"), (32,32)), utils.get_color(3))

        self.addtional_info = 0

    def update(self):
        self.parent.window.fill(utils.get_color(0))
        self.width, self.height = self.parent.display.get_window_size()

        mouse_pos =  pygame.mouse.get_pos()
        mouse_btns = pygame.mouse.get_pressed()
        
        # Handle keyboard input
        if isinstance(self.mouse_occupied[0], tuple) and self.parent.pressed != None:

            # Number input to highlighted element
            if 48 <= self.parent.pressed and self.parent.pressed < 58:
                self.mouse_occupied[0][1] = self.parent.pressed/100-0.48
        else:
            # Additional info (Show/Hide)
            if self.parent.pressed == pygame.K_F1:
                self.addtional_info = (self.addtional_info+1)%2

            # Export state to vector
            if self.parent.pressed == pygame.K_e:
                utils.export_vector(self.parent)
            
            # Step backwards
            if self.parent.pressed == pygame.K_LEFT and self.state[0] > 0:
                self.state[0] = self.state[0]-1
                self.state[1] = self.state_history[self.state[0]]

            # Step fowards
            if self.parent.pressed == pygame.K_RIGHT:
                self.state[0] += 1
                if len(self.state_history) == self.state[0]:
                    self.state_history.append(self.state[1].__copy__())
                    self.state[1].step()
                else:
                    self.state[1] = self.state_history[self.state[0]]
        
        # Draw nodes and handle mouse inputs
        for node in self.state[1].nodes:
            self.parent.window.blit(self.uninfected_node_img if node.state == 0 else self.infected_node_img, (node.position[0]*self.width-16, node.position[1]*self.height-16))

            # Move nodes
            if mouse_btns[0] and (self.mouse_occupied[0] == node or (mouse_pos[0]-node.position[0]*self.width)**2 + (mouse_pos[1]-node.position[1]*self.height)**2 <= 256):
                if self.mouse_occupied[0] == None:
                    self.mouse_occupied = [node, mouse_pos[0]/self.width-node.position[0], mouse_pos[1]/self.height-node.position[1]]
                if  self.mouse_occupied[0] == node:
                    node.position = (mouse_pos[0]/self.width-self.mouse_occupied[1], mouse_pos[1]/self.height-self.mouse_occupied[2])

            # Activate node
            elif mouse_btns[2] and (mouse_pos[0]-node.position[0]*self.width)**2 + (mouse_pos[1]-node.position[1]*self.height)**2 <= 256:
                if self.mouse_occupied[0] == None:
                    node.state = (node.state + 1) % 2
                    self.mouse_occupied = [node, mouse_pos[0]/self.width-node.position[0], mouse_pos[1]/self.height-node.position[1]]

            elif not (mouse_btns[0] or mouse_btns[2]) and isinstance(self.mouse_occupied[0], Node):
                self.mouse_occupied[0] = None
            
            # Draw additional info (Node threshold)
            if self.addtional_info:
                threshold_text = self.parent.font_light.render(f"{int(sum([edge[0].state*edge[1] for edge in node.edges])*100)}/{int(node.threshold*100)}", True, (utils.get_color(3+node.state)))
                threshold_text_rect = threshold_text.get_rect()
                threshold_text_rect.center = (node.position[0]*self.width, node.position[1]*self.height+32)

                self.parent.window.blit(threshold_text, threshold_text_rect)

            # Draw edges
            for edge in node.edges:
                AB = (edge[0].position[0]*self.width - node.position[0]*self.width, edge[0].position[1]*self.height - node.position[1]*self.height)
                absAB = (AB[0]**2 + AB[1]**2)**0.5
                if absAB != 0:
                    CB = (AB[0]/absAB*4, AB[1]/absAB*4)       # Point C is on line AB where |CB| = 4
                    CD, CE = (-CB[1], CB[0]), (CB[1], -CB[0]) # Vectors CD and CE are perpendicular to Vector CB
                    D, E = (node.position[0]*self.width+CB[0]*8-CD[0], node.position[1]*self.height+CB[1]*8-CD[1]), (node.position[0]*self.width+CB[0]*8-CE[0], node.position[1]*self.height+CB[1]*8-CE[1])
                    # edge[0].position
                    # node.position[0]

                    if absAB > 64:
                        pygame.draw.polygon(self.parent.window, (utils.get_color(2)), (D, E, (node.position[0]*self.width+CB[0]*6, node.position[1]*self.height+CB[1]*6)))
                        pygame.draw.line(self.parent.window, (utils.get_color(2)), (node.position[0]*self.width+CB[0]*8, node.position[1]*self.height+CB[1]*8), (edge[0].position[0]*self.width-CB[0]*8, edge[0].position[1]*self.height-CB[1]*8), 2)
                    elif absAB > 32:
                        pygame.draw.line(self.parent.window, (utils.get_color(2)), (node.position[0]*self.width+CB[0]*4, node.position[1]*self.height+CB[1]*4), (edge[0].position[0]*self.width-CB[0]*4, edge[0].position[1]*self.height-CB[1]*4), 2)
                
                    # Draw additional info (Edge weight)
                    if self.addtional_info:
                        weight_text = self.parent.font_light.render(f"{int(edge[1]*100)}", True, (utils.get_color(2)))
                        weight_text_rect = weight_text.get_rect()
                        weight_text_rect.center = (AB[0]/2 + node.position[0]*self.width - CD[0]*3, AB[1]/2 + node.position[1]*self.height - CD[1]*3)
                        self.parent.window.blit(weight_text, weight_text_rect)
