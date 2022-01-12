# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper () & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA

import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import random

# GENERAL CLASS COMMENT:
# registry part is necessary to easily loop over all instances of the object later

# a class that represents a House object
class House(object):
    _registry = []

    def __init__(self, x, y, maxoutput):
        self._registry.append(self)
        self.x = x
        self.y = y
        self.maxoutput = maxoutput
        self.connected = False

# a class that represents a Battery object
class Battery:
    _registry = []

    def __init__(self, x, y, capacity):
        self._registry.append(self)
        self.x = x
        self.y = y
        self.capacity = capacity

# a class that represents a Cable object
# havent done anything with this yet
class Cable:
    _registry = []

    def __init__(self, x_coords, y_coords):
        self._registry.append(self)
        self.x_coords = x_coords
        self.y_coords = y_coords

# load in the locations of the houses and batteries as provided
def load_district(dis_id):
    # read the csv's into dataframes
    df_bat = pd.read_csv("data/district_{0}/district-{0}_batteries.csv".format(dis_id))
    df_hou = pd.read_csv("data/district_{0}/district-{0}_houses.csv".format(dis_id))

    # make objects of each instance in the dataframe
    for idx, bat in df_bat.iterrows():
        # comma separated string -> list of [x, y] ints
        coord_pair = list(map(int, bat['positie'].split(',')))
        battery = Battery(coord_pair[0], coord_pair[1], bat['capaciteit'])
    
    for idx, hou in df_hou.iterrows():
        # comma separated string -> list of [x, y] ints
        coord_pair = [int(hou['x']), int(hou['y'])]
        house = House(coord_pair[0], coord_pair[1], hou['maxoutput'])

    return

def make_cable():

    for hou in House._registry:

        cable_instance = [[hou.x, hou.y]]
        for idx in range(100): 

            # checks if cable from house reached battery already
                if hou.connected == False:

                    # making sure cables dont run outside of the grid
                    if cable_instance[-1][0] == 50 and cable_instance[-1][1] == 50:
                        # random step of one grid segment, but not in positive x direction
                        dx = random.randint(-1, 0)
                        dy = random.randint(-1, 0)

                        while dx**2 + dy**2 != 1:
                            dx = random.randint(-1, 0)
                            dy = random.randint(-1, 0)
                    
                    elif cable_instance[-1][0] == 0 and cable_instance[-1][1] == 0:
                        # random step of one grid segment, but not in positive x direction
                        dx = random.randint(0, 1)
                        dy = random.randint(0, 1)

                        while dx**2 + dy**2 != 1:
                            dx = random.randint(0, 1)
                            dy = random.randint(0, 1)
                    
                    elif cable_instance[-1][0] == 50 and cable_instance[-1][1] == 0:
                        # random step of one grid segment, but not in positive x direction
                        dx = random.randint(-1, 0)
                        dy = random.randint(0, 1)

                        while dx**2 + dy**2 != 1:
                            dx = random.randint(-1, 0)
                            dy = random.randint(0, 1)

                    elif cable_instance[-1][0] == 0 and cable_instance[-1][1] == 50:
                        # random step of one grid segment, but not in positive x direction
                        dx = random.randint(0, 1)
                        dy = random.randint(-1, 0)

                        while dx**2 + dy**2 != 1:
                            dx = random.randint(0, 1)
                            dy = random.randint(-1, 0)

                    elif cable_instance[-1][0] == 50:
                        # random step of one grid segment, but not in positive x direction
                        dx = random.randint(-1, 0)
                        dy = random.randint(-1, 1)

                        while dx**2 + dy**2 != 1:
                            dx = random.randint(-1, 0)
                            dy = random.randint(-1, 1)

                    elif cable_instance[-1][0] == 0:
                        # random step of one grid segment, but not in negative x direction
                        dx = random.randint(0, 1)
                        dy = random.randint(-1, 1)

                        while dx**2 + dy**2 != 1:
                            dx = random.randint(0, 1)
                            dy = random.randint(-1, 1)

                    elif cable_instance[-1][1] == 50:
                        # random step of one grid segment but not in positive y direction
                        dx = random.randint(-1, 1)
                        dy = random.randint(-1, 0)

                        while dx**2 + dy**2 != 1:
                            dx = random.randint(-1, 1)
                            dy = random.randint(-1, 0)
                    
                    elif cable_instance[-1][1] == 0:
                        # random step of one grid segment, but not in negative y direction
                        dx = random.randint(-1, 1)
                        dy = random.randint(0, 1)

                        while dx**2 + dy**2 != 1:
                            dx = random.randint(-1, 1)
                            dy = random.randint(0, 1)
                    
                    else:
                        # random step of one grid segment
                        dx = random.randint(-1, 1)
                        dy = random.randint(-1, 1)

                        # make sure diagonal movement is illegal
                        while dx**2 + dy**2 != 1:
                            dx = random.randint(-1, 1)
                            dy = random.randint(-1, 1)

                    # calc coords of new cable point
                    cable_point = [cable_instance[idx][0] + dx, cable_instance[idx][1] + dy]
                    cable_instance.append(cable_point)
                    
                    # checks if cable reached a battery and updates house registry if reached
                    for battery in Battery._registry:
                        if battery.x == cable_point[0] and battery.y == cable_point[1]:
                            hou.connected = True

        # this can be done easier i know sry
        cable_instance = np.array(cable_instance)
        cable_instance = cable_instance.T

        cable = Cable(cable_instance[0], cable_instance[1])
        
    return

# draw a basic visualisation of the provided elements
def draw_grid():

    bat_coords = [[], []]
    hou_coords = [[], []]
    # prob diff structure, line instead of point
    cab_coords = [[], []]

    # gather coords of all object instances and format in scatterable way
    for hou in House._registry:
        hou_coords[0].append(hou.x)
        hou_coords[1].append(hou.y)

    for bat in Battery._registry:
        bat_coords[0].append(bat.x)
        bat_coords[1].append(bat.y)

    fig, ax = plt.subplots()
    ax.scatter(bat_coords[0], bat_coords[1], c='red', label="batteries")
    ax.scatter(hou_coords[0], hou_coords[1], c='blue', label="houses")

    # just draw a random line to see how it looks
    # x = [0, 1, 2, 3, 4, 5]
    # y = [0, 0, 0, 0, 0, 0]
    # ax.plot(x, y, c='green')

    # plot the semi random lines
    for cab in Cable._registry:
        ax.plot(cab.x_coords, cab.y_coords, c='green')


    # some nice ticks and grid etc
    ax.set(xlim=(-5, 55), xticks=np.arange(0, 51, 5), 
       ylim=(-5, 55), yticks=np.arange(0, 51, 5))
    ax.minorticks_on()
    ax.grid(which='both')
    ax.legend()

    plt.show()

    return

load_district(2)
make_cable()
draw_grid()
