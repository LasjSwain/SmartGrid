# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper (12416657) & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA
# main runs all the necessary functions: spine of the program

import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import random

DISTRICT = 2

# GENERAL CLASS COMMENT:
# registry part is necessary to easily loop over all instances of the object later

from classes import House, Battery, Cable

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
        house = House(coord_pair[0], coord_pair[1], hou['maxoutput'], 'here will be a cable')

    # creates bitmap for grid to checks for edges
    bitmap = np.pad([[1 for x in range(51)] for y in range(51)], pad_width=1)

    # return sorted_house_objects, bitmap  
    return bitmap

from algorithms.algo_combi import find_random_combi
from algorithms.algo_astar import make_cable

# find 10 configurations to later calculate shortest length
configurations = []
while len(configurations) < 2:

    legal_solution = False
    while not legal_solution:
        Battery._registry = []
        House._registry = []

        bitmap = load_district(DISTRICT)
        legal_solution, combi_dict = find_random_combi()

    configurations.append(combi_dict)
    print("Bingo! We got config {}".format(len(configurations)))

print("yeah this should be about enough huh")

from output import draw_rep_plot, draw_all_plot, make_json
from output import find_cable_length

min_cable_length = 10**6

for idx, combi_dict in enumerate(configurations):
    # empty cable to reset count
    Cable._registry = []

    make_cable(combi_dict, bitmap)

    cable_length = find_cable_length()
    print("{} has length {}".format(idx+1, cable_length))

    # find the shortest configuration
    if cable_length < min_cable_length:
        min_cable_length = cable_length
        shortest_config = combi_dict

# remake and plot the shortest config:
make_cable(shortest_config, bitmap)
# draw_all_plot()
draw_rep_plot()

# jason quit working after shared algo implementation
# make_json(DISTRICT, total_cable_len)


