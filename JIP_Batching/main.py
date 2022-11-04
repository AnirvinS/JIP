import random
from matplotlib import pyplot as plt
import pandas as pd
from SlottingMapwoC import makeSlotMap
from Batching import makeBatches, checkItems, getAisleList
import keyboard

# REPLACE VALUES FOR PRINTING BY STORAGE

def createSlotSKU(SKUlist, divisor, divratio = 1, stringo=""):

    for addskusku in range(1, int((divisor)*(divratio/100))+1):
        tempadder = stringo + str(addskusku)
        SKUlist.append(tempadder)

    return SKUlist

def createFakeOrders(SKUlist, num_orders = 500):

    # 1=100 orders for BT3, 2=200 orders for BT3, 3=170 orders for BT2, 4=100 orders for BT1, 5=60 orders for BT1

    bnumstats = [0.27, 0.17, 0.1, 0.102, 0.038, 0.07, 0.25]
    # prodtypestats = [0.08, 0.02, 0.08, 0.56*0.74, 0.74*0.3, 0.74*0.11, 0.74*0.03, 0.06, 0.02] # 8 for 1/12 and 16 for 1/6
    prodtypestats = [0.146, 0.00, 0.226, 0.4*0.781, 0.781*0.4, 0.781*0.15, 0.781*0.05, 0.295, 0.295] # 8 for 1/12 and 16 for 1/6

    prodnums = [360, 0, 360, 1440, 720, 180, 180, 180, 180]

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

    btb = 1
    # while flagellent == 1:
    mCT = 24

    nal, na, nc, ns, np = 10, 20, 12, 5, 3

    SKU = []


    SKU = createSlotSKU(SKU, divisor=na*nc*ns*np, divratio=10, stringo="Multipack ")
    SKU = createSlotSKU(SKU, divisor=0, divratio=12, stringo="Magnum ")
    SKU = createSlotSKU(SKU, divisor=na * nc * ns * np, divratio=10, stringo="100-150cl Bottle ")
    SKU = createSlotSKU(SKU, divisor=na * nc * ns * np, divratio=40, stringo="70-99cl Wijn ")
    SKU = createSlotSKU(SKU, divisor=na * nc * ns * np, divratio=20, stringo="70-99cl Distilled ")
    SKU = createSlotSKU(SKU, divisor=na * nc * ns * np, divratio=5, stringo="70-99cl Aperitif ")
    SKU = createSlotSKU(SKU, divisor=na * nc * ns * np, divratio=5, stringo="70-99cl Other Bottle ")
    SKU = createSlotSKU(SKU, divisor=na * nc * ns * np, divratio=5, stringo="volume<25 cl Can/Bottle ")
    SKU = createSlotSKU(SKU, divisor=na * nc * ns * np, divratio=5, stringo="25-69 cl ")

    nfa, nfp, cba, cbp, nfbtp, nfbta = [], [], [], [], [], []

    for itersss in range(100):

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
            if itersss==0:
                napal = makeSlotMap(display=2, map_save=0, SKU=SKU, num_aisles=na, num_aislelanes=nal, num_shelves=ns, num_pos=np, num_cabinet=nc)

            Batches, FBT_Batch = makeBatches(Orders=Orders, SKU=SKU, minCartThreshold=mCT, num_aisles_per_alane=napal, box_type_batching=btb, FIFOBTYPE=True) #Keep changing box_type_batching for all three results

            if len(Batches)!=0:

                custom_batching_picklines = len(list(set(Batches[1])))

                custom_batching_aisles = len(list(set(getAisleList(SKULIST=Batches[1], slottinglist=SKU, num_c= nc, num_s=ns, num_p=np, mode=2, num_aisles_per_alane=napal))))

                fbt_batching_picklines = len(list(set(FBT_Batch[1])))

                fbt_batching_aisles = len(list(set(getAisleList(SKULIST=FBT_Batch[1], slottinglist=SKU, num_c=nc, num_s=ns, num_p=np, num_aisles_per_alane=napal, mode=2))))

                # Computing picklines and aisles for FIFO

                fifopicklinelist, fifoaislelist = [], []

                for fifoorderiter in range(mCT):
                    # for calculating picklines
                    for fifoskuiter in Orders[fifoorderiter][1]:

                        if fifoskuiter not in fifopicklinelist:

                            fifopicklinelist.append(fifoskuiter)
                    # for calculating aisles
                    # fifoaisles = getAisleList(SKULIST=Orders[fifoorderiter][1], slottinglist=SKU, num_aisles_per_alane=napal)
                    fifoaisles = getAisleList(SKULIST=Orders[fifoorderiter][1], slottinglist=SKU, num_c= nc, num_s=ns, num_p=np, mode=2, num_aisles_per_alane=napal)

                    for fa in fifoaisles:
                        if fa not in fifoaislelist:
                            fifoaislelist.append(fa)

                num_fifo_aisles = len(list(set(fifoaislelist)))
                num_fifo_picklines = len(list(set(fifopicklinelist)))

                print(f"Picklines of FIFO: {list(set(fifopicklinelist))}\nAisles of FIFO: {list(set(fifoaislelist))}\n\nPicklines of CB: {list(set(Batches[1]))}\nAisles of CB: {list(set(getAisleList(SKULIST=Batches[1], slottinglist=SKU, num_c= nc, num_s=ns, num_p=np, mode=2, num_aisles_per_alane=napal)))}\n")
                print(f"Picklines of FBT: {list(set(FBT_Batch[1]))}\nAisles of FBT: {list(set(getAisleList(SKULIST=FBT_Batch[1], slottinglist=SKU, num_c=nc, num_s=ns, num_p=np, num_aisles_per_alane=napal, mode=2)))}")

                print(f"\nBatched Order is: {Batches}\n")

                print(f"\nFIFO Picklines: {num_fifo_picklines}\nFIFO Aisles: {num_fifo_aisles}\n\nCB Picklines: {custom_batching_picklines}\nCB Aisles: {custom_batching_aisles}\n\nFBT PIcklines: {fbt_batching_picklines}\nFBT Aisles: {fbt_batching_aisles}")

                nfbtp.append(fbt_batching_picklines)
                nfbta.append(fbt_batching_aisles)
                nfp.append(num_fifo_picklines)
                nfa.append(num_fifo_aisles)
                cbp.append(custom_batching_picklines)
                cba.append(custom_batching_aisles)

        else:
            print(f"Not all order items have corresponding SKUs")

        # break

        # print(f"")
    nfp_average = sum(nfp)/len(nfp)
    nfa_average = sum(nfa) / len(nfa)
    cbp_average = sum(cbp) / len(cbp)
    cba_average = sum(cba) / len(cba)
    nfbtp_average = sum(nfbtp) / len(nfbtp)
    nfbta_average = sum(nfbta) / len(nfbta)

    nfp_average_list = [nfp_average for nfpai in range(len(nfp))]
    nfa_average_list = [nfa_average for nfaai in range(len(nfa))]
    cbp_average_list = [cbp_average for cbpai in range(len(cbp))]
    cba_average_list = [cba_average for cbaai in range(len(cba))]
    nfbtp_average_list = [nfbtp_average for nfbtpai in range(len(nfbtp))]
    nfbta_average_list = [nfbta_average for nfbtaai in range(len(nfbta))]


        # keyboard.wait('a')
    plt.plot(nfp, label="Number of FIFO Picklines")
    plt.plot(cbp, color="green", label="Number of Custom Batching Picklines")
    plt.plot(nfbtp, 'r-', label="Number of [FIFO + B_Type] Batching Picklines")
    plt.plot(nfp_average_list, 'b-.', label="Average Number of FIFO Picklines")
    plt.plot(cbp_average_list, '-.', color="green", label="Average Number of CB Picklines")
    plt.plot(nfbtp_average_list, 'r-.', label="Average Number of [FIFO + B_Type] Picklines")
    plt.xlabel("Iterations")
    plt.ylabel("Number of Picklines Visited (in a pickrun)")
    plt.legend(bbox_to_anchor=(1.5, 1.5))
    plt.show()

    plt.plot(nfa, label="Number of FIFO Aisles")
    plt.plot(cba, color="green", label="Number of Custom Batching Aisles")
    plt.plot(nfbta, 'r-', label="Number of [FIFO + B_Type] Aisles")
    plt.plot(nfa_average_list, 'b-.', label="Average Number of FIFO Aisles")
    plt.plot(cba_average_list, '-.', color="green", label="Average Number of CB Aisles")
    plt.plot(nfbta_average_list, 'r-.', label="Average Number of [FIFO + B_Type] Aisles")
    plt.xlabel("Iterations")
    plt.ylabel("Number of Aisles Traversed (in a pickrun)")
    plt.legend(bbox_to_anchor=(1.5, 1.5))
    plt.show()

    f_name_datasave = f"/Users/anirvin/Downloads/JIPSheets/ControlenVerify/FIFOvFBTvCB_BT{btb}_500fake_100iter.csv"

    # Plot Average Line
    # Baseline with BoxType

    picklines_aisles_df = pd.DataFrame(list(zip(nfp, nfa, cbp, cba, nfbtp, nfbta)), columns=['FIFO_Picklines', 'FIFO_Aisles', 'CB_Picklines', 'CB_Aisles', 'FBT_Picklines', 'FBT_Aisles'])
    average_row = {'FIFO_Picklines':nfp_average, 'FIFO_Aisles':nfa_average, 'CB_Picklines':cbp_average, 'CB_Aisles': cba_average, 'FBT_Picklines':nfbtp_average, 'FBT_Aisles':nfbta_average}

    picklines_aisles_df.to_csv(f_name_datasave)