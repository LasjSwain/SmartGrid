# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper (12416657) & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA
# main runs all the necessary functions: spine of the program

from lib2to3.pytree import HUGE
import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import random

DISTRICT = 2
NUMBER_HOUSES = 150
NUMBER_BATTERIES = 5

from classes.house import House
from classes.battery import Battery
from classes.cable import Cable

# load in the locations of the houses and batteries as provided
def load_district(dis_id):
    # read the csv's into dataframes
    df_bat = pd.read_csv("data/district_{0}/district-{0}_batteries.csv".format(dis_id))
    df_hou = pd.read_csv("data/district_{0}/district-{0}_houses.csv".format(dis_id))

    # make objects of each instance in the dataframe
    for idx, bat in df_bat.iterrows():
        # comma separated string -> list of [x, y] ints
        coord_pair = list(map(int, bat['positie'].split(',')))
        battery = Battery(idx, coord_pair[0], coord_pair[1], bat['capaciteit'])
    
    for idx, hou in df_hou.iterrows():
        # comma separated string -> list of [x, y] ints
        coord_pair = [int(hou['x']), int(hou['y'])]
        house = House(idx, coord_pair[0], coord_pair[1], hou['maxoutput'], 'here will be a cable')

    # creates bitmap for grid to checks for edges
    bitmap = np.pad([[1 for x in range(51)] for y in range(51)], pad_width=1)

    return bitmap

from algorithms.algo_combi import find_random_combi, find_closest_combi, make_dist_list, convert_dist_to_id
from algorithms.algo_astar import make_cable

# THIS WAS FOR RANDOM: LATER DO SOMETHING COOL WITH IT
# find ... configurations to later calculate shortest length
# configurations = []
# while len(configurations) < ATTEMPTS:

#     legal_solution = False
#     while not legal_solution:
#         Battery._registry = []
#         House._registry = []

#         # load in all houses, batteries and borders
#         bitmap = load_district(DISTRICT)

#         # find a house-battery configuration
#         legal_solution, combi_dict = find_random_combi()

#     configurations.append(combi_dict)

#     if len(configurations) % 10 == 0:
#         print("We got {} configs".format(len(configurations)))

# do you want to switch houses or batteries?
switch_what = 'only houses'
# switch_what = 'both'

if switch_what == 'only houses':
    number_options = NUMBER_HOUSES
elif switch_what == 'both':
    number_options = NUMBER_HOUSES * NUMBER_BATTERIES

# find ... configurations to later calculate shortest length
configurations = []
orders = []
current_attempt = 0

while current_attempt < number_options:

    legal_solution = False
    while not legal_solution:
        Battery._registry = []
        House._registry = []

        # load in all houses, batteries and borders
        bitmap = load_district(DISTRICT)

        # make a (shuffled based on current_attempt) new possible config order
        dist_list = make_dist_list(current_attempt, switch_what)
        id_list = convert_dist_to_id(dist_list)

        # find a house-battery configuration
        legal_solution, combi_dict = find_closest_combi(dist_list)

        current_attempt += 1
        print(current_attempt)

    if id_list not in orders:
        configurations.append(combi_dict)
        orders.append(id_list)

        if len(configurations) % 1 == 0:
            print("We got {} configs".format(len(configurations)))

print("out of a possible {} options".format(number_options))

from output import draw_rep_plot, draw_all_plot, draw_start_end, find_cable_length
from output import make_json, jason_remakes, length_csv, csv_hist

min_cable_length = 10**6

# save a list of each length
lengths = []

# for each config, pull cables, find length, save the shortest
for idx, combi_dict in enumerate(configurations):

    make_cable(combi_dict, bitmap)

    cablen = find_cable_length()
    lengths.append(cablen)


    # print("config {} has len {}".format(idx, cablen))

    # find the shortest configuration
    if cablen < min_cable_length:
        min_cable_length = cablen
        # shortest_config = combi_dict
        make_json(DISTRICT)

    # reset variables related to cables
    Cable._registry = []
    for bat in Battery._registry:
        bat.cables = []
    for hou in House._registry:
        hou.cable = "emptied"


# remake from json:
jason_remakes()

# save all lengths in a csv
length_csv(lengths)

# make a histogram of that csv
csv_hist(number_options)

draw_all_plot()
# draw_rep_plot()
# draw_start_end()
