# tsja: an attempt to a SmartGrid solution
# Dirk Kuiper (12416657) & Lars Zwaan (12414069)
# part of Programmeertheorie, Minor Programmeren, UvA
# algo_combi divides houses over batteries without overflowing their capacity

import sys
import numpy as np
import random

from classes import House, Battery

# randomly find a house-battery configuration that is legal
def find_random_combi():

    # combi dict is the dict in which to save the config
    combi_dict = dict()
    bat_full_list = []
    
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
                # for bat in Battery._registry:
                #     print("avail:", bat.av_cap)
                # print("needed: ", hou.maxoutput)
                return False, combi_dict

        combi_dict[bat_to_cnct].append(hou)

            # check if unconnectable house exists
            # stuck = True
            # for hou_stuck_find in House._registry:
            #     for bat_stuck_find in Battery._registry:
            #         if hou_stuck_find.maxoutput < bat_stuck_find.av_cap:
            #             stuck = False

            # if stuck == True:
            #     return False, combi_dict

            # if stuck == True:
            #     for bat in Battery._registry:
            #         print("avail:", bat.av_cap)
            #     print("needed: ", hou.maxoutput)

                # this method doesnt work: it might be that minoutput-house
                # still fits, but another doesnt anymore; ^method better
                # check if battery full by trying to fit lowest output house
                # find the smallest available maxoutput
                # min_output = 100
                # for hou_for_min_find in House._registry:
                #     if hou_for_min_find.connected == False:
                #         if hou_for_min_find.maxoutput < min_output:
                #             min_output = hou_for_min_find.maxoutput
                # if min_output > bat_to_cnct.av_cap:
                #     if bat_to_cnct not in bat_full_list:
                #         bat_full_list.append(bat_to_cnct)
                #     if len(bat_full_list) == 5:
                #         return False, combi_dict
        
    return True, combi_dict