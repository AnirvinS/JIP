from SlottingMapwoC import makeSlotMap
from Batching import makeBatches

if __name__ == '__main__':

    SKU = ["Bacardi Carta Blanca", "Tanquerey", "Bacardi Carta Oro", "Tanquerey LE", "2Bacardi Carta Blanca",
           "2Tanquerey", "2Bacardi Carta Oro", "2Tanquerey LE", "3Bacardi Carta Blanca", "3Tanquerey", "3Bacardi Carta Oro",
           "3Tanquerey LE"]

    Orders = [[0, ["Bacardi Carta Blanca", "2Tanquerey LE"], 1], [1, ["3Bacardi Carta Blanca", "Tanquerey LE"], 1]] #turn first parameter to list as well for batching

    makeSlotMap(display=1, SKU=SKU, num_aisles= 6, num_aislelanes= 2, num_shelves=2)

    Batches = makeBatches(Orders= Orders, SKU=SKU, threshold = 2, minCartThreshold=100)
