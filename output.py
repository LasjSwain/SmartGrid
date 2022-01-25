# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper (12416657) & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA
# output draws a visual representation and produces a .json

import sys
import matplotlib.pyplot as plt
import numpy as np
import json

from classes import House, Battery, Cable

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
    cable_len_own = 0
    counted_cab_points = []
    done = False
    first_circled = False
    for cab in Cable._registry:
        cable_len_own += cab.length + 1

        # if a cable point is at a previously empty point, count it
        for idx in range(len(cab.x_coords)):
            cab_point = [cab.x_coords[idx], cab.y_coords[idx]]
            if cab_point not in counted_cab_points:
                counted_cab_points.append(cab_point)

        ax.plot(cab.x_coords, cab.y_coords, c='green')

    cable_len_shared = len(counted_cab_points)
    ax.set_title("Cable length own vs shared: {} vs {}".format(cable_len_own, cable_len_shared))

    # some nice ticks and grid etc
    ax.set(xlim=(-5, 55), xticks=np.arange(0, 51, 5), 
       ylim=(-5, 55), yticks=np.arange(0, 51, 5))
    ax.minorticks_on()
    ax.grid(which='both')
    ax.legend()

    plt.show()

    return cable_len_own

# output a json file in the specified format to use check50
def make_json(DISTRICT, cable_len_own):
    # some constants that might differ later
    battery_price = 5000
    cable_price = 9
    number_batteries = 5
    costs_own = number_batteries * battery_price + cable_len_own * cable_price

    # create a list that will be outputted to jason, made of dicts
    output = []

    # a subdict for general info
    general_dict = dict()
    general_dict["costs-own"] = costs_own
    general_dict["district"] = DISTRICT

    output.append(general_dict)

    # a subdict for each battery
    for bat in Battery._registry:
        bat_dict = dict()
        bat_dict["location"] = "{},{}".format(bat.x, bat.y)
        bat_dict["capacity"] = bat.capacity

        all_hou_list = []
        # a subdict for each house
        for hou in bat.connected_to:
            hou_dict = dict()

            hou_dict["location"] = "{},{}".format(hou.x, hou.y)
            hou_dict["output"] = hou.maxoutput

            cable_list = []

            # at each cable segment coordinate as a line to the cable dict
            # + 1 for number of points inst of len, + 1 for arriving at last point
            for cable_idx in range(hou.cable.length + 1):
                x = hou.cable.x_coords[cable_idx]
                y = hou.cable.y_coords[cable_idx]
                cable_list.append("{},{}".format(x, y))

            hou_dict["cables"] = cable_list
            all_hou_list.append(hou_dict)

        bat_dict["houses"] = all_hou_list
        output.append(bat_dict)

    with open('output/output.json', 'w') as fp:
        json.dump(output, fp)

    return