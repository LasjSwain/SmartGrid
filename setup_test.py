# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper () & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA

import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np

# a class that represents a House object
# i now load in the locations of each house; i should make objects for each of m still
class House:
    def __init__(self, x, y, maxoutput):
        self.x = x
        self.y = y
        self.maxoutput = maxoutput

# a class that represents a Battery object
# i now load in the locations of each battery; i should make objects for each of m still
class Battery:
    def __init__(self, x, y, capacity):
        self.x = x
        self.y = y
        self.capacity = capacity

# a class that represents a Cable_segment object
# havent done anything with this yet
class Cable_segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # this is just a test for me (LZ) to get familiar with classes again
    def talk(self):
        print("There is a cable segment on (x, y) = ({}, {})".format(self.x, self.y))

# this is just a test for me (LZ) to get familiar with classes again
# small_cable = Cable_segment(69, 69)
# small_cable.talk()

# load in the locations of the houses and batteries as provided
def load_district(dis_id):
    # read the csv's into dataframes
    df_bat = pd.read_csv("data/district_{0}/district-{0}_batteries.csv".format(dis_id))
    df_hou = pd.read_csv("data/district_{0}/district-{0}_houses.csv".format(dis_id))

    bat_coords = []
    hou_coords = []

    # make lists of coords (comma separated string -> list of [x, y] ints)
    for bat in df_bat['positie']:
        bat_coords.append(list(map(int, bat.split(','))))
    
    for idx, hou in df_hou.iterrows():
        hou_coords.append([int(hou['x']), int(hou['y'])])

    # make lists into arrays to be able to Transpose later
    # could be more efficient but ok
    bat_coords = np.array(bat_coords)
    hou_coords = np.array(hou_coords)

    return bat_coords, hou_coords

# draw a basic visualisation of the provided elements
def draw_grid(bat_coords, hou_coords):

    # transpose arrays to make m in right order to scatter
    bat_coords = bat_coords.T
    hou_coords = hou_coords.T

    fig, ax = plt.subplots()

    ax.scatter(bat_coords[0], bat_coords[1], c='red', label="batteries")
    ax.scatter(hou_coords[0], hou_coords[1], c='blue', label="houses")

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

# do the process for district (1) / (2) / (3)
draw_grid(load_district(2)[0], load_district(2)[1])
