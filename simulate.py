#!/bin/env python3

from math import floor, ceil
from random import random
import utils

class State():
    def __init__(self, nodes=[]):
        self.nodes = nodes

    def __copy__(self):
        new_state = State([node.__copy__() for node in self.nodes])

        for new_node in new_state.nodes:
            new_node.edges = [[new_state.nodes[self.nodes.index(new_edge[0])], new_edge[1]] for new_edge in new_node.edges]

        return new_state

    def grid_generate(self, node_count: int, node_threshold_range: tuple, edge_freq_range: tuple, edge_weight_range: tuple, max_edge_length: float, window_size: tuple):
        asp = window_size[1]/window_size[0]

        # Generate Node Map Dimentions
        map_width, map_height = (node_count/asp)**0.5, (node_count*asp)**0.5
        round_map_width, round_map_height = round(map_width), floor(map_height)
        map_remainder = node_count - (round_map_width*round_map_height)

        if map_remainder != 0:
            round_map_height = round_map_height + map_remainder//round_map_width
            map_remainder = node_count - round_map_width*round_map_height
        
        # Create Nodes in grid format
        self.nodes = [None for _ in range(node_count)]
        for row in range(round_map_height):
            for column in range(round_map_width):
                position = ((column+1)/(round_map_width+1) + (row%2*2-1)/(round_map_width*3) + random()/(round_map_width*3), (row+1)/(round_map_height+1+(map_remainder!=0)) + random()/(round_map_height*3))

                threshold = node_threshold_range[0] + utils.float_randrange(node_threshold_range)
                self.nodes[row*round_map_width+column] = Node(position, threshold, [], 0)
        
        for remainder in range(map_remainder):
            position = (((remainder+1)/(map_remainder+1) + random()/(round_map_width*3)), (round_map_height+1)/(round_map_height+2) + random()/(round_map_height*3))
            threshold = node_threshold_range[0] + utils.float_randrange(node_threshold_range)
            self.nodes[node_count-map_remainder+remainder] = Node(position, threshold, [], 0)
        
        # Create edges
        for anode in utils.scramble_sequence(self.nodes):
            for bnode in utils.scramble_sequence(self.nodes):
                if anode == bnode:
                    continue

                distance = ((anode.position[0]-bnode.position[0])**2 + (anode.position[1]-bnode.position[1])**2)**0.5
                if node_count*utils.float_randrange(edge_freq_range)/(distance*2+0.001)**2/(len(anode.edges)*len(bnode.edges)**2+1) > 1 and distance < max_edge_length:
                    anode.edges.append([bnode, utils.float_randrange(edge_weight_range)])
                else:
                    for edge in bnode.edges:
                        if edge[0] == anode and random() > 0.3:
                            anode.edges.append([bnode, utils.float_randrange(edge_weight_range)])

        return self

    def read(self, file_dir):
        return self

    def write(self):
        pass

    def step(self):
        updated_states = [0 for _ in range(len(self.nodes))]

        for i, node in enumerate(self.nodes):
            total = sum([edge[1] for edge in node.edges])
            potential = sum([edge[1]*edge[0].state for edge in node.edges])

            if potential > node.threshold:
                updated_states[i] = 1
        
        for i, state in enumerate(updated_states):
            if state: self.nodes[i].state = 1

class Node():
    def __init__(self, position: tuple, threshold: float, edges: list, state: int):
        self.position = (float(position[0]), float(position[1]))
        self.threshold = float(threshold)
        self.edges = list(edges)
        self.state = state
    
    def __copy__(self):
        return Node(self.position, self.threshold, self.edges, self.state)