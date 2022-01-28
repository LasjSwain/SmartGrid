# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper (12416657) & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA
# algo_astar provides an approach to a solution via the A* algorithm for pathfinding

import dis
from gettext import find
from hashlib import new
import sys
import numpy as np
import random

from classes import House, Battery, Cable

# function to calculate manhattan distance between two points, which is the absolute difference between the coordinates
def manhattan_distance(a, b):
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))

# creates a new cable segment in random direction
def new_cable_segment():
    dx = random.randint(-1, 1)
    dy = random.randint(-1, 1)

    # make sure diagonal movement is illegal
    while dx**2 + dy**2 != 1:
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)

    return dx, dy

# run a cable from a house to a battery (random)
def make_cable(combi_dict, bitmap):

    for bat in combi_dict:
        # print("bat {},{} is connected to {} houses".format(bat.x, bat.y, len(bat.connected_to)))
        for hou in bat.connected_to:

            # number of cable points on battery; not counted in cable_leng
            # bat_connectpoints = 0

            # set all houses to not connected to re-use variable
            hou.connected = False

            closest_connectpoint = ''

            # find the nearest connectable point to this battery
            # if bat has no cables, closest connectable point = bat self
            if len(bat.cables) == 0:
                closest_connectpoint = [bat.x, bat.y]
                # bat_connectpoints += 1

            # else find closest cable connected to that battery
            else:
                # a (high) start value for min distance
                min_distance = 100
                for cable in bat.cables:
                    for idx in range(len(cable.x_coords)):
                        cab_point = [cable.x_coords[idx], cable.y_coords[idx]]
                        if manhattan_distance([hou.x, hou.y], cab_point) < min_distance:
                            min_distance = manhattan_distance([hou.x, hou.y], cab_point)
                            closest_connectpoint = cab_point

            # start building the cable at the house
            cable_instance = [[hou.x, hou.y]]
            cable_len = 0
            distance_to_cnctpoint = manhattan_distance([hou.x, hou.y], closest_connectpoint)

            # dont pull a cable if the house is already at its connectpoint
            if distance_to_cnctpoint == 0:
                hou.connected = True

            # while cable from house hasnt reached battery
            while hou.connected == False:

                # make a random new segment
                dx, dy = new_cable_segment()

                # calc coords of new cable point
                cable_point = [cable_instance[cable_len][0] + dx, cable_instance[cable_len][1] + dy]

                # checks on bitmap if the coordinate is valid (not outside of edges)
                if bitmap[cable_point[0]+1][cable_point[1]+1] == 1:

                    # only move if getting closer to connectpoint, else try another move
                    if manhattan_distance(cable_point, closest_connectpoint) < distance_to_cnctpoint:

                        cable_instance.append(cable_point)
                        cable_len += 1
                        distance_to_cnctpoint = manhattan_distance(cable_point, closest_connectpoint)

                        # checks if cable reached the battery
                        if cable_point[0] == closest_connectpoint[0] and cable_point[1] == closest_connectpoint[1]:
                            hou.connected = True
                # else: try again

            # transpose the cable list from ([xy][xy]) to ([xxx][yyy])
            # print("hou: ", hou.x, hou.y)
            # print("cab: ", cable_instance)
            # print("bat: ", bat.x, bat.y)
            # print("cnct: ", closest_connectpoint)

            cable_instance = (np.array(cable_instance)).T

            cable = Cable(cable_instance[0], cable_instance[1], len(cable_instance[0]))
            
            hou.cable = cable
            bat.cables.append(cable)

            # also change og registry instead of only battery objects in combi_dict
            for find_bat in Battery._registry:
                if find_bat.x == bat.x and find_bat.y == bat.y:
                    find_bat.cables.append(cable)
                    
            for find_hou in House._registry:
                if find_hou.x == hou.x and find_hou.y == hou.y:
                    find_hou.cable = cable
        
    return