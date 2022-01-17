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
        self.av_cap = capacity

# a class that represents a Cable object
# havent done anything with this yet
class Cable:
    _registry = []

    def __init__(self, x_coords, y_coords, length):
        self._registry.append(self)
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.length = length

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

    sorted_house_objects = sorted([hou for hou in House._registry], key=lambda x: x.maxoutput, reverse=True)

    # creates bitmap for grid to checks for edges
    bitmap = np.pad([[1 for x in range(51)] for y in range(51)], pad_width=1)
    


    # tot_out = 0
    # for hou in House._registry:
    #     tot_out += hou.maxoutput 
    # print("total out", tot_out)
    # tot_cap = 0
    # for bat in Battery._registry:
    #     tot_cap += bat.capacity 
    # print("total cap", tot_cap)

    return sorted_house_objects, bitmap

# creates a new cable segment in random direction
def new_cable_segment(cable_instance):
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
            dx, dy = new_cable_segment(cable_instance)

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
                        else:
                            # THIS DOESNT WORK YET: IF THIS HOUSE DOESNT FIT IT DOESNT MEAN THE BATTERY IS FULL!
                            if bat not in bat_full_list:
                                bat_full_list.append(bat)

                        if len(bat_full_list) == 5:
                            print("alles is vol :(")
                            sys.exit()

                cable_instance.append(cable_point)
                cable_len += 1
            # elses: try again

        print("{} houses connected".format(houses_connected))

        # this can be done easier i know sry
        # transpose the cable list from (xyxyxyxy) to (xxxyyy)
        cable_instance = (np.array(cable_instance)).T

        cable = Cable(cable_instance[0], cable_instance[1], cable_len)
        
    return

# draw a basic visualisation of the provided elements
def draw_grid():

    bat_coords = [[], []]
    hou_coords = [[], []]

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

    # plot the semi random lines
    total_cable_len = 0
    for cab in Cable._registry:
        ax.plot(cab.x_coords, cab.y_coords, c='green')
        total_cable_len += cab.length

    ax.set_title("Total cable length: {}".format(total_cable_len))

    # some nice ticks and grid etc
    ax.set(xlim=(-5, 55), xticks=np.arange(0, 51, 5), 
       ylim=(-5, 55), yticks=np.arange(0, 51, 5))
    ax.minorticks_on()
    ax.grid(which='both')
    ax.legend()

    plt.show()

    return

sorted_house_objects, bitmap = load_district(1)
make_cable(sorted_house_objects, bitmap)
draw_grid()
