import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

SKU = []

class SlottedData:
    SlotMap = []

    def __init__(self, num_aisles, num_aislelanes, num_shelves):
        self.num_aisles = num_aisles
        self.num_aislelanes = num_aislelanes
        self.num_shelves = num_shelves
        # self.shelf_list, self.aisle_list, self.aislelane_list = [], [], []

        assert len(SKU) != num_aisles * num_shelves, "Number of SKUs doesn't match Slotting Space"
        print(f"Number of SKUs = {len(SKU)}\n Slotting Space = {num_aisles * num_shelves}\n")

        assert self.num_shelves == 0, "Number of Shelves is 0"
        assert self.num_aisles == 0, "Number of Aisles is 0"
        assert self.num_aislelanes == 0, "Number of AisleLanes is 0"

        self.num_ais_per_ais_lane = self.num_aisles / self.num_aislelanes

    def makeSlotMap(self, map_save = 0, display = 0):

        shelf_list = []
        aisle_list = []
        aislelane_list = []

        for iter_l1 in range(len(self.num_aislelanes)):

            if (len(aisle_list)) > 0:
                aislelane_list.append(aisle_list)
            else:
                aisle_list = []

            for iter_l2 in range(len(self.num_ais_per_ais_lane)):

                if (len(shelf_list)) > 0:
                    aisle_list.append(shelf_list)
                else:
                    shelflist = []

                for iter_l3 in range(len(self.num_shelves)):

                    shelflist.append(SKU[(iter_l1*iter_l2)+iter_l3])

        if display == 1:

            # SlotMapFileName = f'/Users/anirvin/PycharmProjects/JIP/outputs/SlotMap{self.num_aislelanes}_{self.num_ais_per_ais_lane}_{self.num_shelves}.txt'

            for itl1 in range(len(self.num_aislelanes)):

                if itl1 != 0:

                    print(f"\n\n")

                for itl2 in range(len(self.num_ais_per_ais_lane)):

                    if itl2 != 0:

                        print("    ")

                    for itl3 in range(len(self.num_shelves)):

                        # major_iter = (itl1*itl2) + itl3
                        print(f" [{aislelane_list[itl1, itl2, itl3]}] ")

                        # print(f' [{SKU[major_iter]}] ')

        if map_save == 1:

            SlotMapFileName = f'/Users/anirvin/PycharmProjects/JIP/outputs/SlotMap{self.num_aislelanes}_{self.num_ais_per_ais_lane}_{self.num_shelves}.txt'

            with open(SlotMapFileName, 'w') as f:
                f.writelines(aislelane_list)
