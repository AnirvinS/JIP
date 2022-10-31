import random

from SlottingMapwoC import makeSlotMap
from Batching import makeBatches, checkItems, getAisleList
import keyboard

def createSlotSKU(SKUlist, divisor, divratio = 1, stringo=""):

    for addskusku in range(1, int((divisor)/divratio)+1):
        tempadder = stringo + str(addskusku)
        SKUlist.append(tempadder)

    return SKUlist

def createFakeOrders(SKUlist, num_orders = 100):
    bnumstats = [0.27, 0.17, 0.1, 0.102, 0.038, 0.07, 0.25]
    prodtypestats = [0.08, 0.02, 0.08, 0.56*0.74, 0.74*0.3, 0.74*0.11, 0.74*0.03, 0.06, 0.02] # 8 for 1/12 and 16 for 1/6
    prodnums = [8, 8, 16, 16, 16, 8, 8, 8, 8]

    pts_ext = []

    for ptrack, pdn in enumerate(prodnums):
        for pditer in range(pdn):
            pts_ext.append(prodtypestats[ptrack])

    mainorderlist = []
    order_index = 0
    for bnp, botnumprob in enumerate(bnumstats):
        for botnum in range(int(num_orders*botnumprob)):
            if bnp<len(bnumstats)-1:
                sampleorderskus = random.choices(SKUlist, weights=pts_ext, k=bnp+1)
            else:
                sampleorderskus = random.choices(SKUlist, weights=pts_ext, k=12)

            mainorderlist.append([[order_index], sampleorderskus, 1])
            order_index += 1

    return mainorderlist


# flagellent = 1

if __name__ == '__main__':

    # while flagellent == 1:
    mCT = 10

    nal, na, nc, ns, np = 6, 12, 2, 2, 2

    SKU = []

    SKU = createSlotSKU(SKU, divisor=na*nc*ns*np, divratio=12, stringo="Multipack ")
    SKU = createSlotSKU(SKU, divisor=na * nc * ns * np, divratio=12, stringo="Magnum ")
    SKU = createSlotSKU(SKU, divisor=na * nc * ns * np, divratio=6, stringo="100-150cl Bottle ")
    SKU = createSlotSKU(SKU, divisor=na * nc * ns * np, divratio=6, stringo="70-99cl Wijn ")
    SKU = createSlotSKU(SKU, divisor=na * nc * ns * np, divratio=6, stringo="70-99cl Distilled ")
    SKU = createSlotSKU(SKU, divisor=na * nc * ns * np, divratio=12, stringo="70-99cl Aperitif ")
    SKU = createSlotSKU(SKU, divisor=na * nc * ns * np, divratio=12, stringo="70-99cl Other Bottle ")
    SKU = createSlotSKU(SKU, divisor=na * nc * ns * np, divratio=12, stringo="volume<25 cl Can/Bottle ")
    SKU = createSlotSKU(SKU, divisor=na * nc * ns * np, divratio=12, stringo="25-69 cl ")

    fake_orders = createFakeOrders(SKU)
    print(fake_orders)

    # Orders = [[[0], ["Bacardi Carta Blanca", "2Tanquerey LE"], 1], [[1], ["Bacardi Carta Blanca", "2Tanquerey LE"], 1], [[2], ["3Tanquerey", "2Tanquerey LE"], 1], [[1], ["Tanquerey LE", "2Tanquerey LE"], 1], [[1], ["3Tanquerey", "2Tanquerey LE"], 1], [[1], ["3Tanquerey", "2Tanquerey LE"], 1], [[1], ["3Tanquerey", "2Tanquerey LE"], 1], [[1], ["3Tanquerey", "2Tanquerey LE"], 1], [[1], ["3Tanquerey", "2Tanquerey LE"], 1], [[1], ["3Tanquerey", "2Tanquerey LE"], 1], [[1], ["3Tanquerey", "2Tanquerey LE"], 1], [[1], ["3Tanquerey", "2Tanquerey LE"], 1], [[1], ["3Tanquerey", "2Tanquerey LE"], 1],] #turn first parameter to list as well for batching      "3Bacardi Carta Blanca", "Tanquerey LE"

    # Orders = [[[0], ["Multipack 1", "70-99cl Wijn 3"], 1]]

    Orders = fake_orders
    random.shuffle(Orders)

    for enum_iter, order_nums in enumerate(Orders):
        order_nums[0] = [enum_iter]

    if(checkItems(SKU, Orders)):

        print(f"The order items all have corresponding SKUs")

        napal = makeSlotMap(display=2, map_save=0, SKU=SKU, num_aisles=na, num_aislelanes=nal, num_shelves=ns, num_pos=np, num_cabinet=nc)

        Batches = makeBatches(Orders=Orders, SKU=SKU, minCartThreshold=mCT, num_aisles_per_alane=napal)

        if len(Batches)!=0:

            custom_batching_picklines = len(list(set(Batches[1])))

            custom_batching_aisles = len(list(set(getAisleList(SKULIST=Batches[1], slottinglist=SKU, num_c= 2, num_s=2, num_p=2, mode=2, num_aisles_per_alane=napal))))

            # Computing picklines and aisles for FIFO

            fifopicklinelist, fifoaislelist = [], []

            for fifoorderiter in range(mCT):
                # for calculating picklines
                for fifoskuiter in Orders[fifoorderiter][1]:

                    if fifoskuiter not in fifopicklinelist:

                        fifopicklinelist.append(fifoskuiter)
                # for calculating aisles
                # fifoaisles = getAisleList(SKULIST=Orders[fifoorderiter][1], slottinglist=SKU, num_aisles_per_alane=napal)
                fifoaisles = getAisleList(SKULIST=Orders[fifoorderiter][1], slottinglist=SKU, num_c= 2, num_s=2, num_p=2, mode=2, num_aisles_per_alane=napal)

                for fa in fifoaisles:
                    if fa not in fifoaislelist:
                        fifoaislelist.append(fa)

            num_fifo_aisles = len(list(set(fifoaislelist)))
            num_fifo_picklines = len(list(set(fifopicklinelist)))

            print(f"Picklines of FIFO: {list(set(fifopicklinelist))}\nAisles of FIFO: {list(set(fifoaislelist))}\n\nPicklines of CB: {list(set(Batches[1]))}\nAisles of CB: {list(set(getAisleList(SKULIST=Batches[1], slottinglist=SKU, num_c= 2, num_s=2, num_p=2, mode=2, num_aisles_per_alane=napal)))}\n")

            print(f"\nBatched Order is: {Batches}\n")

            print(f"\nFIFO Picklines: {num_fifo_picklines}\nFIFO Aisles: {num_fifo_aisles}\n\nCB Picklines: {custom_batching_picklines}\nCB Aisles: {custom_batching_aisles}")

    else:
        print(f"Not all order items have corresponding SKUs")

        # break

        # print(f"")

        # keyboard.wait('a')
