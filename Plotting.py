import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

def plot_my_sheet(f_name):

    monthly_ptype_pb = "/Users/anirvin/Downloads/JIPSheets/monthly_ptype_pb.csv"
    weekly_ptype_pb = "/Users/anirvin/Downloads/JIPSheets/weekly_ptype_pb.csv"
    yearly_ptype_pb = "/Users/anirvin/Downloads/JIPSheets/yearly_ptype_pb.csv"
    monthly_ptpb = "/Users/anirvin/Downloads/JIPSheets/monthly_ptpb.csv"
    weekly_ptpb = "/Users/anirvin/Downloads/JIPSheets/weekly_ptpb.csv"
    ptype_ptpb = "/Users/anirvin/Downloads/JIPSheets/ptype_ptpb.csv"
    monthly_ecom_pb = "/Users/anirvin/Downloads/JIPSheets/monthly_ecom_pb.csv"
    weekly_ecom_pb = "/Users/anirvin/Downloads/JIPSheets/weekly_ecom_pb.csv"
    yearly_ecom_pb = "/Users/anirvin/Downloads/JIPSheets/yearly_ecom_pb.csv"



    pldf = pd.read_csv(str(f_name))
    pd.set_option('display.max_columns', None)
    print(pldf.head())

    for aaa in range(len(pldf['pickstart'])):
        if pldf.at[aaa, 'picktype'] == 'Longtail Picking':
            pldf.at[aaa, 'picktype'] = 'Longtail picking'

    sdt, edt = [], []

    uudt = []

    for (i, s) in enumerate(pldf['pickstart']):
        if not isinstance(s, str):
            s = str(s)
        pass
        if s == 'nan':
            uudt.append(i)
        else:
            sdt.append(datetime.strptime(s, '%Y-%m-%d %H:%M:%S'))

    for u in uudt:

        pldf.drop(pldf.index[u], axis=0, inplace=True)

    pldf['pickstart'] = sdt

    monthcatDF = pldf.copy(deep=True)
    weekcatDF = pldf.copy(deep=True)
    yearcatDF = pldf.copy(deep=True)
    picktypecatDF = pldf.copy(deep=True)

    monthcatDF.set_index('pickstart', inplace=True)
    weekcatDF.set_index('Week', inplace=True)
    yearcatDF.set_index('pickstart', inplace=True)

    print("INDEXX\n\n")

    print(monthcatDF.index)
    print(weekcatDF.index)
    print(yearcatDF.index.year)

    # monthcatDF.groupby([monthcatDF.index.month_name()], sort=False)['Pick_time'].mean().plot(figsize=(18, 5),
    #                                                                            stacked=False, xlabel='Time', ylabel='Average Pick Time (in s)')

    # plt.show()

    # monthcatDF["ToSortMonth"] = pd.to_datetime(monthcatDF.Month, format='%b', errors='coerce').dt.month
    # monthcatDF = monthcatDF.sort_values(by="ToSortMonth")

    yapplefplot = yearcatDF.groupby([yearcatDF.index.year, 'picktype'], sort=False)['Bottling_efficiency'].mean()
    apple_fplot = monthcatDF.groupby([monthcatDF.index.month_name(), 'picktype'], sort=False)['Bottling_efficiency'].mean()
    wapplefplot = weekcatDF.groupby([weekcatDF.index, 'picktype'], sort=False)['Bottling_efficiency'].mean()

    print(monthcatDF.groupby([monthcatDF.index.month_name(), 'picktype'], sort=False)['Bottling_efficiency'].mean())
    print(apple_fplot.shape)

    plot_df_a = apple_fplot.unstack(level=-1)   # .loc[:, 'Bottling_efficiency']
    print(plot_df_a.index.values)
    print(plot_df_a)

    print(weekcatDF.groupby([weekcatDF.index, 'picktype'], sort=False)['Bottling_efficiency'].mean())
    wplot_df_a = wapplefplot.unstack(level=-1)
    print(wplot_df_a.index.values)
    print(wplot_df_a)

    print(yearcatDF.groupby([yearcatDF.index.year, 'picktype'], sort=False)['Bottling_efficiency'].mean())
    yplot_df_a = yapplefplot.unstack(level=-1)
    print(yplot_df_a.index.values)
    print(yplot_df_a)

    plot_df_a.to_csv(monthly_ptype_pb)
    wplot_df_a.to_csv(weekly_ptype_pb)
    yplot_df_a.to_csv(yearly_ptype_pb)

    # plot_df_a.sort_index()

    # month_dict = {'Jan':1,'Feb':2,'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    # plot_df_a.sort_values('month', key=lambda x: x.apply(lambda x: month_dict[x]))



    plt.index = pd.PeriodIndex(plot_df_a.index.tolist(), freq='M')
      #, xlabel='Time (Month)', ylabel='Average Picking Time per bottle (in seconds)'

    average_pick_time_ovr = pldf['Pick_time'].sum() / pldf['b_delivered'].sum()

    viable_pick_options = ["E-Commerce picking"]

    rslt_df = pldf[pldf['picktype'].isin(viable_pick_options)]
    average_pick_time_ovr_ecom = rslt_df['Pick_time'].sum() / rslt_df['b_delivered'].sum()

    print(average_pick_time_ovr_ecom)
    print(average_pick_time_ovr)

    avg_pt_o, avg_pt_ec =[], []

    for jstcnt in range(len(plot_df_a.index)):

        avg_pt_o.append(average_pick_time_ovr)
        avg_pt_ec.append(average_pick_time_ovr_ecom)

    avg_pt_o, avg_pt_ec = pd.DataFrame(avg_pt_o), pd.DataFrame(avg_pt_ec)
    avg_pt_o.columns = ['global average']
    avg_pt_ec.columns = ['global e-commerce average']

    avgm1ax = plt.gca()

    plot_df_a.plot(kind='bar', ax=avgm1ax)
    # plt.plot(avg_pt_ec, 'r', linewidth=1)
    # plt.plot(avg_pt_o, 'k:', linewidth=1, markersize=12)
    avg_pt_ec.plot(kind='line', colormap='Reds_r', linewidth=1, ax=avgm1ax, label='global e-commerce average')
    avg_pt_o.plot(kind='line', style='--', colormap='Purples_r', linewidth=1, ax=avgm1ax, label='global average')

    plt.xlabel = 'Time (Month)'
    plt.ylabel = 'Average Picking Time per bottle (in seconds)'

    plt.legend()

    # LONGTAIL PICKING LEGEND

    fig = plt.figure()
    plt.show()
    fig.savefig('temp.png', dpi=fig.dpi)

    print(monthcatDF.groupby('Month')['Pick_time', "Bottling_efficiency"].mean())

    monthly_ptpb_plotdf = monthcatDF.groupby('Month')['Pick_time', "Bottling_efficiency"].mean()
    monthly_ptpb_plotdf.to_csv(monthly_ptpb)


    # weekcatDF.set_index('Week', inplace=True)
    print(weekcatDF.groupby('Week')['Pick_time', "Bottling_efficiency"].mean())

    weekly_ptpb_plotdf = weekcatDF.groupby('Week')['Pick_time', "Bottling_efficiency"].mean()
    weekly_ptpb_plotdf.to_csv(weekly_ptpb)

    # print(picktypecatDF.groupby('picktype', 'Month')['Pick_time', "Bottling_efficiency"].mean())

    print(picktypecatDF.groupby('picktype')['Pick_time', "Bottling_efficiency"].mean())

    ptype_ptpb_plotdf = picktypecatDF.groupby('picktype')['Pick_time', "Bottling_efficiency"].mean()
    ptype_ptpb_plotdf.to_csv(ptype_ptpb)

    # print(picktypecatDF.groupby('picktype', 'Week')['Pick_time', "Bottling_efficiency"].mean())

    fig, ax = plt.subplots()

    # ax.set_xticks(np.arange(0, picktypecatDF["Pick_time"].max() + 1, 5))

    pldf.groupby('picktype')["Pick_time"].plot(kind='hist', bins=500, xlabel='Pick Time (in secs)', ylabel='Frequency')
    print(pldf.groupby('picktype')["Pick_time"])

    # ax = pldf.hist()
    ax.set_xlim((0, 10000))

    plt.legend()

    plt.show()

    only_ecom_df = monthcatDF[monthcatDF['picktype'].isin(viable_pick_options)]

    ecom_pick_plot = only_ecom_df.groupby([only_ecom_df.index.month_name()], sort=False)['Bottling_efficiency'].mean()

    print(ecom_pick_plot)

    ecom_pick_plot.to_csv(monthly_ecom_pb)

    plt.index = pd.PeriodIndex(ecom_pick_plot.index.tolist(), freq='M')

    ecom_pick_plot.plot(kind='bar', linewidth=1, legend=False, xlabel='Months', rot=90, ylabel='Average Pick Time per bottle (in secs)')

    # ax.set_xlim((0, 10000))

    plt.show()

    wonly_ecom_df = weekcatDF[weekcatDF['picktype'].isin(viable_pick_options)]


    #
    wecom_pick_plot = wonly_ecom_df.groupby([wonly_ecom_df.index], sort=False)['Bottling_efficiency'].mean()
    #
    # plt.index = pd.PeriodIndex(wecom_pick_plot.index.tolist(), freq='W')

    print(wecom_pick_plot)

    wecom_pick_plot.to_csv(weekly_ecom_pb)
    #
    wecom_pick_plot.plot(kind='bar', linewidth=1, legend=False, xlabel='Weeks', ylabel='Average Pick Time per bottle (in secs)')
    #


    plt.show()

    # yonly_ecom_df = yearcatDF[yearcatDF['picktype'].isin(viable_pick_options)]
    #
    # yecom_pick_plot = yonly_ecom_df.groupby([yonly_ecom_df.index], sort=False)['Bottling_efficiency'].mean()
    #
    # # plt.index = pd.PeriodIndex(set(yecom_pick_plot.index.tolist()), freq='Y')
    #
    # yecom_pick_plot.to_csv(yearly_ecom_pb)
    #
    # print(yecom_pick_plot)
    # # plt.index = pd.PeriodIndex(set(yecom_pick_plot.index.tolist()), freq='T')
    #
    # yecom_pick_plot.plot(kind='bar', linewidth=1, legend=False, xlabel='Years', ylabel='Average Pick Time per bottle (in secs)')
    #
    # plt.show()