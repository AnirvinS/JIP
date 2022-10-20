import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def getConversion(fname):

    cdf = pd.read_csv(str(fname))
    pd.set_option('display.max_columns', None)
    print(cdf.head())

    for aaa in range(len(cdf['pickstart'])):
        if cdf.at[aaa, 'picktype'] == 'Longtail Picking':
            cdf.at[aaa, 'picktype'] = 'Longtail picking'

    sdt, edt = [], []

    uudt = []

    for (i, s) in enumerate(cdf['pickstart']):
        if not isinstance(s, str):
            s = str(s)
        pass
        if s == 'nan':
            uudt.append(i)
        else:
            sdt.append(datetime.strptime(s, '%Y-%m-%d %H:%M:%S'))

    for u in uudt:
        cdf.drop(cdf.index[u], axis=0, inplace=True)

    cdf['pickstart'] = sdt

    viable_pick_options = ["E-Commerce picking"]

    ccdf = cdf[cdf['picktype'].isin(viable_pick_options)]

    ccdf.set_index('pickstart', inplace=True)

    tyoelistt = []

    for ind in ccdf.index:
        tyoelistt.append(type(ind))

    print(set(tyoelistt))

    uni_year = []

    for a in ccdf.index.year:

        if a not in uni_year:

            uni_year.append(a)

    uni_year = list(set(uni_year))

    ccdf21 = ccdf[ccdf.index.year == uni_year[0]]
    ccdf22 = ccdf[ccdf.index.year == uni_year[1]]

    print(uni_year)
    print("yep")
    print(ccdf22.groupby('Week'))
    print("yep")
    pick_sum_week21 = ccdf21.groupby('Week')['Pick_time'].sum()

    print(pick_sum_week21)

    pick_sum_week_hourly21 = pick_sum_week21 / 3600

    pick_sum_week21['perhour'] = pick_sum_week_hourly21

    pick_sum_week22 = ccdf22.groupby('Week')['Pick_time'].sum()

    print(pick_sum_week22)

    pick_sum_week_hourly22 = pick_sum_week22 / 3600

    pick_sum_week22['perhour'] = pick_sum_week_hourly22

    print(pick_sum_week21)

    print(pick_sum_week22)

    psw21fn = "/Users/anirvin/Downloads/JIPSheets/psw21.csv"
    psw22fn = "/Users/anirvin/Downloads/JIPSheets/psw22.csv"

    pick_sum_week21.to_csv(psw21fn)
    pick_sum_week22.to_csv(psw22fn)