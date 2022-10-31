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


def makeSlotMap(map_save=0, display=0, SKU=None, num_aisles=0, num_shelves=0, num_aislelanes=0, num_cabinet=0, num_pos=0):

    print(f"Number of SKUs = {len(SKU)}\n Slotting Space = {num_aisles * num_cabinet * num_shelves * num_pos}\n")
    assert len(SKU) == num_aisles * num_cabinet * num_shelves * num_pos, "Number of SKUs doesn't match Slotting Space"

    assert num_pos != 0, "Number of locations in shelves are 0"
    assert num_shelves != 0, "Number of Shelves in cabinets is 0"
    assert num_cabinet != 0, "Number of Cabinets in aisles is 0"
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
            for iter_l3 in range(num_cabinet):
                for iter_l4 in range(num_shelves):
                    for iter_l5 in range(num_pos):
                # print(SKU[iiii])
                        shelf_list.append(SKU[iiii])
                        iiii += 1

    leftrightdistance = 2

    if display == 2:
        aislenumflagger, iteri = 0, 0
        # for itl1 in range(num_aislelanes):
        #
        #     if itl1 != 0:                               # For displaying content in a new aislelane
        #         print("\n\n\n\n", end="")
        #
        #     # for itl2 in range(leftrightdistance):
        #     #     if aislenumflagger == 1:
        #     #         print(f"", end="")
        #     #     if itl2 != 0:
        #     #         print("\n\n\n", end="")
        #     for itl2 in range(num_ais_per_ais_lane):
        #
        #         for itl3 in range(num_cabinet):
        #
        #             if itl3<num_cabinet/2:
        #
        #                 print("|", end=" ")
        #
        #                 for itl4 in range(num_shelves):
        #
        #                     print("[ ", end="")
        #
        #                     for itl5 in range(num_pos):
        #
        #                         iteri = (itl1*(num_ais_per_ais_lane*num_cabinet*num_shelves*num_pos)) + (itl2*(num_cabinet*num_shelves*num_pos)) + (itl3*(num_shelves*num_pos)) + (itl4*num_pos) + itl5
        #                         print(f"  <{shelf_list[iteri]:^30}>  ")
        #                         # iteri += 1
        #
        #                     print("]", end="")
        #
        #                 print("|", end=" ")

        cabflag , sheflag= 0, 1

        for itl in range(len(shelf_list)):

            if itl % (num_cabinet*num_shelves*num_pos)==0 and itl==0:
                print(f"  | A{int(itl/(num_cabinet*num_shelves*num_pos))+1} |  ", end="")

            if itl==0:
                print(" {  ( ", end="")

            if itl % num_pos == 0 and sheflag != 0 and itl!=0:
                print(" ) ", end="")
                sheflag=0

            if itl % (num_shelves*num_pos)==0 and cabflag==0:
                if itl!=0:
                    print("  } ", end="")
                    cabflag=1

            if itl % (num_ais_per_ais_lane*num_cabinet*num_shelves*num_pos)==0 and itl!=0:
                print("\n\n", end="")

            if itl % (num_cabinet*num_shelves*num_pos)==0 and itl!=0:
                print(f"  | A{int(itl/(num_cabinet*num_shelves*num_pos))+1} |  ", end="")

            if itl % (num_shelves*num_pos)==0 and cabflag==1:
                if itl!=0:
                    print(" {  ", end="")
                    cabflag=0



            if itl % num_pos == 0 and sheflag == 0 and itl!=0:
                print("( ", end="")
                sheflag=1

            print(f" [ {shelf_list[itl]:^30} ] ", end="")

            if itl==len(shelf_list)-1:
                print(")}|")

        print("\n\n")










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

    return num_ais_per_ais_lane