#!/bin/env python3

"""
A small python file filled with utility functions for the project
"""

import pygame.color as pgc
from random import random, randrange

from tkinter import Tk
from tkinter.filedialog import asksaveasfile


def get_color(index=None):
    with open("settings.csv", "r") as cfg:
        cfg_color_theme = int(cfg.readlines()[3].replace("\n", "").split(",")[1])
    
    with open("./Assets/color_themes.csv", "r") as cf:
        str_colors = cf.readlines()[cfg_color_theme+1].replace("\n", "").split(",")
    colors = [pgc.Color(int(color_val[0]), int(color_val[1]), int(color_val[2])) for color_val in [str_color.split("-") for str_color in str_colors]]
    
    if index == None:
        return colors
    return colors[index]

def float_randrange(*inputs):
    if isinstance(inputs[0], tuple):
        return (inputs[0][1]-inputs[0][0])*random()+inputs[0][0]

    elif isinstance(inputs[0], float) and isinstance(inputs[1], float):
        return (inputs[1]-inputs[0])*random()+inputs[0]

    return None

def scramble_sequence(sequence: list):
    sequence = list(sequence)
    scrambled = []

    while len(sequence) > 0:
        i = randrange(len(sequence))
        scrambled.append(sequence[i])
        sequence.pop(i)

    return scrambled

def fill(surface, color):
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pgc.Color(r, g, b, a))
    return surface

def to_hex_col(dec_array):
    return "".join([hex(item)[2:] for item in dec_array[:-1]]).upper()

def export_vector(parent):
    width, height = parent.display.get_window_size()

    raw = f'<svg viewBox="0 0 1 1" width="{width}px" height="{height}px" style="background-color:{to_hex_col(get_color(0))}">'
    
    arrow_style = f"fill:#{to_hex_col(get_color(2))};stroke:#{to_hex_col(get_color(2))};stroke-width:{1/240};stroke-miterlimit:4;stroke-dasharray:none"
    arrow_paths = []
    
    for node in parent.screen.state[1].nodes:
        for edge in node.edges:

            AB = (edge[0].position[0] - node.position[0], edge[0].position[1] - node.position[1])
            absAB = (AB[0]**2 + AB[1]**2)**0.5
            if absAB != 0:
                CB = (AB[0]/absAB*(1/120), AB[1]/absAB*(1/120)) # Point C is on line AB where |CB| = 1/120
                CD, CE = (-CB[1], CB[0]), (CB[1], -CB[0])       # Vectors CD and CE are perpendicular to Vector CB
                
                arrow_paths.append(f"m {node.position[0]+CB[0]*4},{node.position[1]+CB[1]*4} {edge[0].position[0]-CB[0]*4-(node.position[0]+CB[0]*4)},{edge[0].position[1]-CB[1]*4-(node.position[1]+CB[1]*4)} k")
        
        # Draw nodes
        style = f"fill:#{to_hex_col(get_color(3+node.state))};stroke:#808000;stroke-width:0;stroke-miterlimit:4;stroke-dasharray:none"
        path = f"m 0.3734705,0.50121194 c -0.106256,0 -0.191752,0.0856 -0.191752,0.19182 v 0.013 c 0,0.10626 0.0855,0.19183 0.191752,0.19183 h 0.253057 c 0.106257,0 0.191753,-0.0856 0.191753,-0.19183 v -0.013 c 0,-0.10625 -0.0855,-0.19182 -0.191753,-0.19182 h -0.01018 a 0.16861575,0.21725927 0 0 1 -0.116457,0.0601 0.16861575,0.21725927 0 0 1 -0.116311,-0.0601 z m 0.279783,-0.15339 a 0.15325691,0.19751661 0 0 1 -0.153257,0.19751 0.15325691,0.19751661 0 0 1 -0.153256,-0.19751 0.15325691,0.19751661 0 0 1 0.153256,-0.19752 0.15325691,0.19751661 0 0 1 0.153257,0.19752 z M 0.4975455,1.9399652e-6 A 0.50001194,0.50001159 0 0 0 5.0082494e-7,0.49996194 0.50001194,0.50001159 0 0 0 0.4999625,1.0000019 0.50001194,0.50001159 0 0 0 0.9999995,0.49996194 0.50001194,0.50001159 0 0 0 0.4999625,1.9399652e-6 a 0.50001194,0.50001159 0 0 0 -0.0024,0 z M 0.4992455,0.12496194 a 0.37503241,0.37503219 0 0 1 7.09e-4,0 0.37503241,0.37503219 0 0 1 0.375083,0.375 0.37503241,0.37503219 0 0 1 -0.375083,0.37509 0.37503241,0.37503219 0 0 1 -0.375008,-0.37509 0.37503241,0.37503219 0 0 1 0.374276,-0.375 z"
        raw += f'<g transform="scale(0.066666) translate{node.position[0]*15-0.5, node.position[1]*15-0.5}"><path style="{style}" d="{path}" /></g>'

    for arrow_path in arrow_paths:
        raw += f'<g><path style="{arrow_style}" d="{arrow_path}"/></g>'
    raw += "</svg>"

    root = Tk()
    root.withdraw()
    root.attributes("-topmost", "true")
    
    try: root.iconbitmap("./Assets/Icons/ems.ico")
    except: pass

    file = asksaveasfile(title="Export Vector", initialdir="", filetypes = (("Vector", "*.svg"),("All Files", "*.*")))
    if file == None:
        return
    with open(file.name, "w") as f:
        f.write(raw)
    