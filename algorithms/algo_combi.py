# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper (12416657) & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA
# algo_combi divides houses over batteries without overflowing their capacity

import sys
import numpy as np
import random

from classes import House, Battery, Cable

# randomly find a house-battery configuration that is legal
def find_random_combi(sorted_house_objects):

    # combi dict is the dict in which to save the config
    combi_dict = dict()
    bat_full_list = []
    
    # make empty lists for each bat to save houses in later
    for bat in Battery._registry:
        combi_dict[bat] = []

    for hou in sorted_house_objects:

        cap_available = False

        while not cap_available:
            bat_to_cnct = random.choice(Battery._registry)

            # if capacity available, connect and lower available capacity
            if bat_to_cnct.av_cap >= hou.maxoutput:
                bat_to_cnct.av_cap -= hou.maxoutput
                bat_to_cnct.connected_to.append(hou)
                hou.connected = True
                cap_available = True

                # check if battery full by trying to fit lowest output house

                # find the smallest available maxoutput
                min_output = 100
                for hou_for_min_find in House._registry:
                    if hou_for_min_find.connected == False:
                        if hou_for_min_find.maxoutput < min_output:
                            min_output = hou_for_min_find.maxoutput

                if min_output > bat_to_cnct.av_cap:

                    if bat_to_cnct not in bat_full_list:
                        bat_full_list.append(bat_to_cnct)

                    if len(bat_full_list) == 5:
                        return False, combi_dict

        combi_dict[bat_to_cnct].append(hou)
        
    return True, combi_dict