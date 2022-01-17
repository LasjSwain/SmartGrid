# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper (12416657) & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA
# output draws a visual representation and produces a .json

import sys
import matplotlib.pyplot as plt
import numpy as np

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

    return total_cable_len

def make_json(DISTRICT, total_cable_len):
    battery_price = 5000
    cable_price = 9
    number_batteries = 5
    own_costs = number_batteries * battery_price + total_cable_len * cable_price
    print("District:", DISTRICT)
    print("own-costs:", own_costs)
    return