import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import copy

SlotList = ["Bacardi Carta Blanca", "Tanquerey", "Bacardi Carta Oro", "Tanquerey LE", "2Bacardi Carta Blanca",
           "2Tanquerey", "2Bacardi Carta Oro", "2Tanquerey LE", "3Bacardi Carta Blanca", "3Tanquerey", "3Bacardi Carta Oro",
           "3Tanquerey LE"]

def checkItems(SKU=None, Orders=None):
    for ord in Orders:
        for ordi in ord[1]:
            if ordi not in SKU:
                print(f"ordi={ordi}")
                return False
    return True

def sendBatch(batchedOrder, mainBatchList):

    mainBatchList.append(batchedOrder)
    return mainBatchList

def getAisleList(SKULIST, slottinglist, num_aisles_per_alane):
    aislenum = []
    for skusku in SKULIST:
        for slotted in range(len(slottinglist)):
            if skusku == slottinglist[slotted]:
                aislenum.append(slotted//num_aisles_per_alane)
                break
    assert len(SKULIST)==len(aislenum), "getaislelist: lists don't hav the same length"
    return aislenum


def BPA(ArrivedOrder):
    BTypeList = ["BT1",  "BT2"]
    if len(ArrivedOrder[1]) > 2:
        return BTypeList[1]
    else:
        return BTypeList[0]

def CalcMaxMetric(BTOrders = None, thresh = 2, BoxTypeSegregation = 0, slotting_list=None, n_a_p_al=None):
    LolMetricPairs = []

    for oiter, oo in enumerate(BTOrders):
        for oio in range(oiter + 1, len(BTOrders)):

            commonpicklines = len(list(set(oo[1]).intersection(BTOrders[oio][1])))

            Alist1 = getAisleList(list(set(oo[1])), slottinglist=slotting_list, num_aisles_per_alane=n_a_p_al)
            Alist2 = getAisleList(list(set(BTOrders[oio][1])), slottinglist=slotting_list, num_aisles_per_alane=n_a_p_al)

            noncommonaisles = len(Alist1) + len(Alist2) - 2 * len(list(set(Alist1).intersection(set(Alist2))))

            metric_o = commonpicklines - noncommonaisles

            LolMetricPairs.append([oiter, oio, metric_o])

    maxmetricpairs, chosen_index = 0, -1

    for lmp_iji in range(len(LolMetricPairs)):
        if LolMetricPairs[lmp_iji][2] > maxmetricpairs:
            maxmetricpairs = LolMetricPairs[lmp_iji][2]
            chosen_index = lmp_iji

    if maxmetricpairs < thresh:
        print(f"No more sub-batching can be performed on this batch (of BoxType {BoxTypeSegregation}) as maximum shared picklines in batch ({maxmetricpairs}) doesn't reach the threshold ({thresh})")
        return "NOBATCH"

    return chosen_index, maxmetricpairs, LolMetricPairs, LolMetricPairs[chosen_index][0], LolMetricPairs[chosen_index][1]


def CalcMaxPicklines(BTOrders = None, thresh = 2, BoxTypeSegregation = 0):

    LolCommonPicklines = []

    for oiter, oo in enumerate(BTOrders):
        for oio in range(oiter+1, len(BTOrders)):
            LolCommonPicklines.append([oiter, oio, len(list(set(oo[1]).intersection(BTOrders[oio][1])))]) # Change to SKU IDs instead of index

    maxpicklineval, chosen_index = 0, -1

    for iji in range(len(LolCommonPicklines)):
        if LolCommonPicklines[iji][2] > maxpicklineval:
            maxpicklineval = LolCommonPicklines[iji][2]
            chosen_index = iji

    if maxpicklineval < thresh:
        print(f"No more sub-batching can be performed on this batch (of BoxType {BoxTypeSegregation}) as maximum shared picklines in batch ({maxpicklineval}) doesn't reach the threshold ({thresh})")
        return "NOBATCH"

    return chosen_index, maxpicklineval, LolCommonPicklines, LolCommonPicklines[chosen_index][0], LolCommonPicklines[chosen_index][1]

def makeBatches(display=0, Orders= None, SKU=None, threshold = 2, minCartThreshold=100, num_aisles_per_alane=None):

    BT1List, BT2List = [], []
    Batches = []

    print(f"Batching started for Orders: {Orders}")

    for od in Orders:

        if BPA(od) == "BT1":
            BT1List.append(od)
            print(f"{od} added to BT1")
        elif BPA(od) == "BT2":
            BT2List.append(od)
            print(f"{od} added to BT2")
        elif BPA(od) != "BT1" and BPA(od) != "BT2":
            print(f"{BPA(od)}: No such type of box exists")
            # raise ValueError

    print(f"\nBT1: {BT1List}; \n BT2: {BT2List}\n")

    # LoLCommonPicklinesBT1, LoLCommonPicklinesBT2 = [], []
    #
    # for o1iter, o1 in enumerate(BT1List):
    #     for o11 in range(o1iter, len(BT1List)):
    #         LoLCommonPicklinesBT1.append([o1iter, o11, len(list(set(o1[1]).intersection(BT1List[o11][1])))])
    #
    # maxpicklineval1, chosen_index1 = 0, -1
    #
    # for j in range(len(LoLCommonPicklinesBT1)):
    #     if LoLCommonPicklinesBT1[j][2] > maxpicklineval1:
    #         maxpicklineval1 = LoLCommonPicklinesBT1[j][2]
    #         chosen_index1 = j
    #
    # for o2iter, o2 in enumerate(BT2List):
    #     for o22 in range(o2iter, len(BT2List)):
    #         LoLCommonPicklinesBT2.append([o2iter, o22, len(list(set(o2[1]).intersection(BT1List[o22][1])))])
    #
    # maxpicklineval2, chosen_index2 = 0, -2
    #
    # for k in range(len(LoLCommonPicklinesBT2)):
    #     if LoLCommonPicklinesBT2[k][2] > maxpicklineval2:
    #         maxpicklineval2 = LoLCommonPicklinesBT2[k][2]
    #         chosen_index2 = k

    mainBatchList, FLAGVAR = [], 0

    # While loop with f string for iter based batching

    while FLAGVAR != 5:

        for checker in BT1List:
            if checker[2] >= minCartThreshold:
                mainBatchList = sendBatch(checker, mainBatchList)

        for checker2 in BT2List:
            if checker2[2] >= minCartThreshold:
                mainBatchList = sendBatch(checker2, mainBatchList)

        FLAGVAR = 0

        if CalcMaxMetric(BT1List, thresh=threshold, BoxTypeSegregation=1, slotting_list=SKU, n_a_p_al=num_aisles_per_alane) == "NOBATCH":
        # if CalcMaxPicklines(BT1List, thresh=threshold, BoxTypeSegregation=1) == "NOBATCH":
            print("we be here vibin'.")
            # print("\n")
            FLAGVAR = 2

            if CalcMaxMetric(BT2List, thresh=threshold, BoxTypeSegregation=2, slotting_list=SKU, n_a_p_al=num_aisles_per_alane) == "NOBATCH":
            # if CalcMaxPicklines(BT2List, thresh=threshold, BoxTypeSegregation=2) == "NOBATCH":

                print("max vibes, exit. fin.")
                # print("\n")
                FLAGVAR = 5

        else:
            # ci1, mpl1, llcpl1, cci1, ccci1 = CalcMaxPicklines(BT1List, thresh=threshold, BoxTypeSegregation=1)
            etricci1, etricmpl1, etricllcpl1, etriccci1, etricccci1 = CalcMaxMetric(BT1List, thresh=threshold, BoxTypeSegregation=1, slotting_list=SKU, n_a_p_al=num_aisles_per_alane)
            print(f"MaxMetricData for BT1: {etricllcpl1[etricci1]}")

            Temp1List, TempProductList = [], []

            for prod in BT1List[etriccci1][1]:
                TempProductList.append(prod)
            for produ in BT1List[etricccci1][1]:
                TempProductList.append(produ)

            totOrders = BT1List[etriccci1][2] + BT1List[etricccci1][2]

            TempProductList = list(set(TempProductList))

            # Add num order in batch

            first_order = etricllcpl1[etricci1][0]
            second_order = etricllcpl1[etricci1][1]

            tempfirstorderstore = copy.deepcopy(BT1List[first_order])

            # BT1List[first_order][0].append(BT1List[second_order][0])
            for eletempp in BT1List[second_order][0]:
                BT1List[first_order][0].append(eletempp)
            BT1List[first_order][1] = TempProductList
            BT1List[first_order][2] = totOrders

            print(f"Order sub-batched in BT1: {BT1List[first_order]}")

            # merged_order1 = [llcpl1[ci1][0], TempProductList, totOrders]
            # BT1List.append(merged_order1) #Change first parameter to better reflect both the SKU IDs which were batched

            # popped11 = BT1List.pop(first_order) #Check if pop index correct and llcpl index works / gets index to be popped from BTList of maxpicklines
            popped12 = BT1List.pop(second_order) #Check if pop index correct and llcpl index works

            print(f"Removed: {tempfirstorderstore} | {popped12}\n")

        if CalcMaxMetric(BT2List, thresh=threshold, BoxTypeSegregation=2, slotting_list=SKU, n_a_p_al=num_aisles_per_alane) != "NOBATCH":

            etricci2, etricmpl2, etricllcpl2, etriccci2, etricccci2 = CalcMaxMetric(BT2List, thresh=threshold, BoxTypeSegregation=2, slotting_list=SKU, n_a_p_al=num_aisles_per_alane)
            # ci2, mpl2, llcpl2, cci2, ccci2 = CalcMaxPicklines(BT2List, thresh=threshold, BoxTypeSegregation=2)
            print(f"MaxPicklineData for BT2: {etricllcpl2[etricci2]}")

            Temp1List, TempProductList = [], []

            for prod2 in BT2List[etriccci2][1]:
                TempProductList.append(prod2)
            for produ2 in BT2List[etricccci2][1]:
                TempProductList.append(produ2)

            totOrders = BT2List[etriccci2][2] + BT2List[etricccci2][2]

            TempProductList = list(set(TempProductList))

            # Add num order in batch

            first_order = etricllcpl2[etricci2][0]
            second_order = etricllcpl2[etricci2][1]

            tempfirstorderstore = copy.deepcopy(BT2List[first_order])
            print(tempfirstorderstore)

            # BT2List[first_order][0].append(BT2List[second_order][0])
            for eletemp in BT2List[second_order][0]:
                BT2List[first_order][0].append(eletemp)
            BT2List[first_order][1] = TempProductList
            BT2List[first_order][2] = totOrders

            print(f"Order sub-batched in BT2: {BT2List[first_order]}")

            # merged_order2 = [llcpl2[ci2][0], TempProductList, totOrders] # Change first parameter to better reflect both the SKU IDs which were batched

            # BT2List.append(merged_order2)  # Change first parameter to better reflect both the SKU IDs which were batched

            # popped21 = BT2List.pop(llcpl2[ci2][0])  # Check if pop index correct and llcpl index works / gets index to be popped from BTList of maxpicklines
            popped22 = BT2List.pop(second_order)  # Check if pop index correct and llcpl index works

            print(f"Removed: {tempfirstorderstore} | {popped22}")

    return mainBatchList



