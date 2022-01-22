# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper (12416657) & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA
# algo_astar provides an approach to a solution via the A* algorithm for pathfinding

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
def make_cable(sorted_house_objects, bitmap):

    # del later
    hou_count = 0

    bat_full_list = []
    for hou in sorted_house_objects:
        
        bat_to_cnct = ''
        closest_connectpoint = ''

        # set a initial value of the max distance possible
        min_distance = 100

        # find the nearest connectable point to a battery
        for bat in Battery._registry:
            if bat not in bat_full_list:

                # if bat has no cables, closest connectable point = bat self
                if len(bat.cables) == 0:
                    if manhattan_distance([hou.x, hou.y], [bat.x, bat.y]) < min_distance:
                        min_distance = manhattan_distance([hou.x, hou.y], [bat.x, bat.y])
                        closest_connectpoint = [bat.x, bat.y]
                        bat_to_cnct = bat
                # else find closest cable connected to that battery
                else:                   
                    for cable in bat.cables:
                        for idx in range(len(cable.x_coords)):
                            cab_point = [cable.x_coords[idx], cable.y_coords[idx]]
                            if manhattan_distance([hou.x, hou.y], cab_point) < min_distance:
                                min_distance = manhattan_distance([hou.x, hou.y], [bat.x, bat.y])
                                closest_connectpoint = cab_point
                                bat_to_cnct = bat

        cable_instance = [[hou.x, hou.y]]
        cable_len = 0
        distance_to_cnctpoint = manhattan_distance([hou.x, hou.y], closest_connectpoint)

        # print("house is at: {}, {}".format(hou.x, hou.y))
        # print("closest bat is at: {}, {}".format(bat_to_cnct.x, bat_to_cnct.y))
        # print("closest connectpoint is at: {}".format(closest_connectpoint))
        # print("distance hou-cntpoint: ", distance_to_cnctpoint)

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

                    # checks if cable reached an available battery
                    if cable_point[0] == closest_connectpoint[0] and cable_point[1] == closest_connectpoint[1]:

                        if bat_to_cnct.av_cap >= hou.maxoutput:
                            bat_to_cnct.av_cap -= hou.maxoutput
                            bat_to_cnct.connected_to.append(hou)
                            hou.connected = True
                            hou_count += 1

                            # loop through houses and check if any house fits.
                            # find the smallest available maxoutput
                            min_output = 100
                            for hou_for_min_find in House._registry:
                                if hou_for_min_find.connected == False:
                                    if hou_for_min_find.maxoutput < min_output:
                                        min_output = hou_for_min_find.maxoutput

                            if min_output > bat_to_cnct.av_cap:
                                print("bat at {},{} is full".format(bat_to_cnct.x, bat_to_cnct.y))
                                if bat_to_cnct not in bat_full_list:
                                    bat_full_list.append(bat_to_cnct)
                                    print(bat_full_list)

                                if len(bat_full_list) == 5:
                                    print("jawel man kijk dan")
                                    for bat in Battery._registry:
                                        print("batleft:", bat.av_cap)
                                    for hou in House._registry:
                                        if hou.connected == False:
                                            print("houleft:", hou.maxoutput)
                                    return False

                    cable_instance.append(cable_point)
                    cable_len += 1
                    distance_to_cnctpoint = manhattan_distance(cable_point, closest_connectpoint)
            # else: try again

        # transpose the cable list from ([xy][xy]) to ([xxx][yyy])
        cable_instance = (np.array(cable_instance)).T

        cable = Cable(cable_instance[0], cable_instance[1], cable_len)
        
        hou.cable = cable
        bat_to_cnct.cables.append(cable)
        
    return True