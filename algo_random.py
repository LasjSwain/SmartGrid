# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper (12416657) & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA
# algo_random provides a random approach to a solution

import sys
import numpy as np
import random

from classes import House, Battery, Cable

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
def make_cable(sorted_house_objects, bitmap):

    houses_connected = 0
    bat_full_list = []
    for hou in sorted_house_objects:

        cable_instance = [[hou.x, hou.y]]
        cable_len = 0

        # while cable from house hasnt reached battery
        while hou.connected == False:

            # make a random new segment within edges
            dx, dy = new_cable_segment()

            # calc coords of new cable point
            cable_point = [cable_instance[cable_len][0] + dx, cable_instance[cable_len][1] + dy]

            # checks on bitmap if the coordinate is valid (not outside of edges)
            if bitmap[cable_point[0]+1][cable_point[1]+1] == 1:

                # checks if cable reached an available battery
                for bat in Battery._registry:
                    if bat.x == cable_point[0] and bat.y == cable_point[1]:
                        if bat.av_cap >= hou.maxoutput:
                            hou.connected = True
                            houses_connected += 1
                            bat.av_cap -= hou.maxoutput
                            bat.connected_to.append(hou)
                        else:
                            if bat not in bat_full_list:
                                bat_full_list.append(bat)

                        if len(bat_full_list) == 5:
                            print("alles is vol :(")
                            print("return False and try again")
                            return False

                cable_instance.append(cable_point)
                cable_len += 1
            # elses: try again

        # dont print the whole time cause that shit is annoying
        if houses_connected % 10 == 0:
            print("{} houses connected".format(houses_connected))

        # transpose the cable list from ([xy][xy]) to ([xxx][yyy])
        cable_instance = (np.array(cable_instance)).T

        cable = Cable(cable_instance[0], cable_instance[1], cable_len)
        
        hou.cable = cable
        bat.cables.append(cable)
        
    return True