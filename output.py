# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper (12416657) & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA
# output draws a visual representation and produces a .json

import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd

from classes.house import House
from classes.battery import Battery
from classes.cable import Cable

# find the total cable length of a certain house-battery configuration
def find_cable_length():

    cable_length = 0

    for cab in Cable._registry:
        cable_length += cab.length

    return cable_length

# draw a visualisation of the grid, all battery networks in 1 plot
def draw_all_plot(DISTRICT, CONFIG, SWITCH):

    fig, ax = plt.subplots()
    ax.set_title("District: {}, Total shared cable length:{}".format(DISTRICT, find_cable_length()))

    # some nice ticks and grid etc
    ax.set(xlim=(-5, 55), xticks=np.arange(0, 51, 5),
           ylim=(-5, 55), yticks=np.arange(0, 51, 5))
    ax.minorticks_on()
    ax.grid(which='both')

    # makes grid a nice square to give proper idea of distances
    ax.set_aspect("equal")

    bat_coords = [[], []]
    hou_coords = [[], []]

    # gather coords of all object instances and format in scatterable way
    for hou in House._registry:
        hou_coords[0].append(hou.x)
        hou_coords[1].append(hou.y)

    for bat in Battery._registry:
        bat_coords[0].append(bat.x)
        bat_coords[1].append(bat.y)

    ax.scatter(bat_coords[0], bat_coords[1], c='red', label="batteries")
    ax.scatter(hou_coords[0], hou_coords[1], c='blue', label="houses")

    for cab in Cable._registry:
        ax.plot(cab.x_coords, cab.y_coords, c='green')

    ax.legend()
    plt.savefig('output/plots/{}_all_{}_{}.png'.format(DISTRICT, CONFIG, SWITCH))

    return

# draw a visualisation of the grid, repeated for each battery network
def draw_rep_plot(DISTRICT, CONFIG, SWITCH):

    bat_coords = [[], []]
    for bat in Battery._registry:
        bat_coords[0].append(bat.x)
        bat_coords[1].append(bat.y)

    hou_coords = [[], []]
    for hou in House._registry:
        hou_coords[0].append(hou.x)
        hou_coords[1].append(hou.y)

    # gather coords of all object instances and format in scatterable way
    batnet = 0
    for bat in Battery._registry:
        batnet += 1
        fig, ax = plt.subplots()

        # some nice ticks and grid etc
        ax.set(xlim=(-5, 55), xticks=np.arange(0, 51, 5),
               ylim=(-5, 55), yticks=np.arange(0, 51, 5))
        ax.minorticks_on()
        ax.grid(which='both')

        # makes grid a nice square to give proper idea of distances
        ax.set_aspect("equal")

        ax.set_title("District: {}, Total shared cable length:{}".format(DISTRICT, find_cable_length()))

        ax.scatter(bat_coords[0], bat_coords[1], c='red', label="batteries")
        ax.scatter(hou_coords[0], hou_coords[1], c='blue', label="houses")

        # this doesnt work anymore as bat has wrong cables somehow
        for cab in bat.cables:
            ax.plot(cab.x_coords, cab.y_coords, c='green')

        ax.legend()
        plt.savefig('output/plots/{}_rep{}_{}_{}.png'.format(DISTRICT, batnet, CONFIG, SWITCH))

    return

# output a json file in the specified format to use check50
def make_json(DISTRICT):
    # some constants that might differ later
    battery_price = 5000
    cable_price = 9
    number_batteries = 5
    costs_shared = (number_batteries * battery_price +
                    find_cable_length() * cable_price)

    # create a list that will be outputted to jason, made of dicts
    output = []

    # a subdict for general info
    general_dict = dict()
    general_dict["costs-shared"] = costs_shared
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
            for cable_idx in range(hou.cable.length):
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

# recreate all house, battery and cable objects from the best saved json
def jason_remakes():

    # reset registry's; load new ones from output.json
    Cable._registry = []
    House._registry = []
    Battery._registry = []

    with open('output/output.json', 'r') as fp:
        data = json.load(fp)

    for bat in data[1:]:

        x = int(bat['location'].split(',')[0])
        y = int(bat['location'].split(',')[1])
        cap = bat['capacity']

        # note: dont add actual id here but guess we dont need it here anymore
        battery = Battery(0, x, y, cap)

        for hou in bat['houses']:
            x = int(hou['location'].split(',')[0])
            y = int(hou['location'].split(',')[1])
            maxoutput = hou['output']

            x_coords = []
            y_coords = []
            for cabpoint in hou['cables']:
                x_coords.append(int(cabpoint.split(',')[0]))
                y_coords.append(int(cabpoint.split(',')[1]))

            cable = Cable(x_coords, y_coords, len(x_coords))

            # note: dont add actual id here but guess we dont need it here anymore
            house = House(0, x, y, maxoutput, cable)

            battery.connected_to.append(house)
            battery.cables.append(cable)

    return


# make a csv file of all lengths to later make a histogram
def length_csv(lengths):
    dict = {'length': lengths}
    df = pd.DataFrame(dict)
    df.to_csv('output/lengths.csv', index=False)

    return

# make a histogram of all total cable lengths from the saved csv
def csv_hist(DISTRICT, CONFIG, SWITCH, number_options):

    df = pd.read_csv('output/lengths.csv')
    df.plot(kind='hist',
            bins=int(number_options / 10),
            title='Histogram of cable lengths of district: {},'
                ' attempts: {}'.format(DISTRICT, number_options))
    plt.xlabel('Total cable length')
    plt.ylabel("Frequency")
    plt.savefig('output/plots/{}_hist_{}_{}.png'.format(DISTRICT, CONFIG, SWITCH))

    return
