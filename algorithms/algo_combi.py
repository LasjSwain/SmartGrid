# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper (12416657) & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA
# algo_combi divides houses over batteries without overflowing their capacity

import sys
import numpy as np
import random

from classes.house import House
from classes.battery import Battery
from classes.cable import Cable

# randomly find a house-battery configuration that is legal
def find_random_combi():

    # combi dict is the dict in which to save the config
    combi_dict = dict()
    # bat_full_list = []
    
    # make empty lists for each bat to save houses in later
    for bat in Battery._registry:
        combi_dict[bat] = []

    random_house_list = random.sample(House._registry, 150)
    for hou in random_house_list:

        while not hou.connected:
            # later implement some kind of actual algorithm here
            # bat_to_cnct = random.choice(Battery._registry)

            random_battery_list = random.sample(Battery._registry, 5)
            for bat_to_cnct in random_battery_list:

                if hou.connected == False:
                    # if capacity available, connect and lower available capacity
                    if bat_to_cnct.av_cap >= hou.maxoutput:
                        bat_to_cnct.av_cap -= hou.maxoutput
                        bat_to_cnct.connected_to.append(hou)
                        hou.connected = True

            if hou.connected == False:
                return False, combi_dict

        combi_dict[bat_to_cnct].append(hou)
        
    return True, combi_dict