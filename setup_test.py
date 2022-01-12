# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper (12416657) & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA

import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np

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

    def __init__(self, x, y):
        self._registry.append(self)
        self.x = x
        self.y = y

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

    # just draw a random line to see how it looks
    x = [0, 1, 2, 3, 4, 5]
    y = [0, 0, 0, 0, 0, 0]
    ax.plot(x, y, c='green')

    # some nice ticks and grid etc
    ax.set(xlim=(-5, 55), xticks=np.arange(0, 51, 5), 
       ylim=(-5, 55), yticks=np.arange(0, 51, 5))
    ax.minorticks_on()
    ax.grid(which='both')
    ax.legend()

    plt.show()

    return

load_district(2)
draw_grid()
