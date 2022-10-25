import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# SKU = ["Bacardi Carta Blanca", "Tanquerey", "Bacardi Carta Oro", "Tanquerey LE", "Bacardi Carta Blanca", "Tanquerey", "Bacardi Carta Oro", "Tanquerey LE", "Bacardi Carta Blanca", "Tanquerey", "Bacardi Carta Oro", "Tanquerey LE"]
#
# num_aisles = 6
# num_aislelanes = 2
# num_shelves = 2
#
# assert len(SKU) != num_aisles * num_shelves, "Number of SKUs doesn't match Slotting Space"
# print(f"Number of SKUs = {len(SKU)}\n Slotting Space = {num_aisles * num_shelves}\n")
#
# assert num_shelves == 0, "Number of Shelves is 0"
# assert num_aisles == 0, "Number of Aisles is 0"
# assert num_aislelanes == 0, "Number of AisleLanes is 0"
#
# num_ais_per_ais_lane = num_aisles / num_aislelanes


def makeSlotMap(map_save=0, display=0, SKU=None, num_aisles=0, num_shelves=0, num_aislelanes=0):

    print(f"Number of SKUs = {len(SKU)}\n Slotting Space = {num_aisles * num_shelves}\n")
    assert len(SKU) == num_aisles * num_shelves, "Number of SKUs doesn't match Slotting Space"


    assert num_shelves != 0, "Number of Shelves is 0"
    assert num_aisles != 0, "Number of Aisles is 0"
    assert num_aislelanes != 0, "Number of AisleLanes is 0"

    num_ais_per_ais_lane = int(num_aisles / num_aislelanes)

    # print(num_ais_per_ais_lane)

    shelf_list = []
    aisle_list = []
    aislelane_list = []

    # for iter_l1 in range(num_aislelanes):
    #
    #     if (len(aisle_list)) > 0:
    #         aislelane_list.append(aisle_list)
    #     else:
    #         aisle_list = []
    #
    #     for iter_l2 in range(num_ais_per_ais_lane):
    #
    #         if (len(shelf_list)) > 0:
    #             aisle_list.append(shelf_list)
    #         else:
    #             shelf_list = []
    #
    #         for iter_l3 in range(num_shelves):
    #             shelf_list.append(SKU[(iter_l1 * iter_l2) + iter_l3])
    iiii = 0
    for iter_l1 in range(num_aislelanes):

        # if (len(aisle_list)) > 0:
        #     aislelane_list.append(aisle_list)
        #     aisle_list = []
        # else:
        #     aisle_list = []

        for iter_l2 in range(num_ais_per_ais_lane):

            # if (len(shelf_list)) > 0:
            #     aisle_list.append(shelf_list)
            #     shelf_list = []
            # else:
            #     shelf_list = []

            for iter_l3 in range(num_shelves):
                # print(SKU[iiii])
                shelf_list.append(SKU[iiii])
                iiii += 1


    # print(shelf_list)

    if display == 1:

        # SlotMapFileName = f'/Users/anirvin/PycharmProjects/JIP/outputs/SlotMap{self.num_aislelanes}_{self.num_ais_per_ais_lane}_{self.num_shelves}.txt'
        iteri = 0

        for itl1 in range(num_aislelanes):

            if itl1 != 0:
                print(f"\n\n", end="")

            for itl2 in range(num_ais_per_ais_lane):

                if itl2 == 0:
                    print(f"|{itl1*(num_ais_per_ais_lane)+1}|", end="")

                if itl2 != 0:
                    print(f"   |{(itl1*(num_ais_per_ais_lane)+1)+itl2}|", end="")

                for itl3 in range(num_shelves):
                    # major_iter = (itl1*itl2) + itl3
                    # print(f"iteri: {iteri}")
                    print(f" [{shelf_list[iteri]:^30}] ", end="")
                    iteri+=1
                    # print(f' [{SKU[major_iter]}] ')

                print("|", end="")

        print("\n")

    if map_save == 1:
        SlotMapFileName = f'/Users/anirvin/PycharmProjects/JIP/JIP_Batching/SlotMap{num_aislelanes}_{num_ais_per_ais_lane}_{num_shelves}.txt'

        with open(SlotMapFileName, 'w') as f:
            f.writelines(shelf_list)
