import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import Plotting as aplt
import ConvertPT as CPT

# Pick Order Times (Average Order
#
#



# def datetimeConvert(date_time_list):
#     # Use a breakpoint in the code line below to debug your script.
#     order_time_list = []
#     order_date_list = []
#     for element in date_time_list:
#         order_date_raw = element[:10]
#         order_date_list.append(order_date_raw)
#         order_time_raw = element[11:-3]
#         if element[-2:] == "PM":
#             if len(order_time_raw) == 7:
#                 order_time = int((int(order_time_raw[0]) + 12)* 3600 + int(order_time_raw[2:4]) * 60 + int(order_time_raw[-2:]))
#                 order_time_list.append(order_time)
#             elif len(order_time_raw) == 8:
#                 order_time = int((int(order_time_raw[:2]) + 12) * 3600 + int(order_time_raw[3:5]) * 60 + int(order_time_raw[-2:]))
#                 order_time_list.append(order_time)
#             else:
#                 print(f"Error! Length is {len(order_time_raw)}! \nExample of error: {order_time_raw}\n")
#                 break
#         elif element[-2:] == "AM":
#             if len(order_time_raw) == 7:
#                 order_time = int(int(order_time_raw[0])* 3600 + int(order_time_raw[2:4]) * 60 + int(order_time_raw[-2:]))
#                 order_time_list.append(order_time)
#             elif len(order_time_raw) == 8:
#                 order_time = int(int(order_time_raw[:2]) * 3600 + int(order_time_raw[3:5]) * 60 + int(order_time_raw[-2:]))
#                 order_time_list.append(order_time)
#             else:
#                 print(f"Error! Length is {len(order_time_raw)}! \nExample of error: {order_time_raw}\n")
#                 break
#
#     return order_date_list, order_time_list


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # myList = ["03/07/2021  3:06:14 PM", "03/07/2021  3:06:14 AM"]
    # x, y = datetimeConvert(myList)
    # print(x)
    # print(y)

    SWITCHER = 0 # 0 for converting sheet into required form, 1 for plotting the sheet data, 3 for data merge of files

    file_name_raw1 = '/Users/anirvin/Downloads/2022_JIP_orderpick_data-2021.xlsx' # 3 sheets
    file_name_raw2 = '/Users/anirvin/Downloads/2022_JIP_orderpick_data-2022.xlsx' # 2 sheets
    file_name_formatted = "/Users/anirvin/Downloads/JIPSheets/orderpick_1_fin.xlsx"

    if SWITCHER == 3:

        fxl1, fxl2 = pd.ExcelFile(file_name_raw1), pd.ExcelFile(file_name_raw2)
        sn1, sn2 = len(fxl1.sheet_names), len(fxl2.sheet_names)
        l_m_df = []

        for xl_iter1 in range(sn1):

            m_df = pd.read_excel(file_name_raw1, sheet_name=xl_iter1)

            l_m_df.append(m_df)

        for xl_iter2 in range(sn2):

            m_df = pd.read_excel(file_name_raw2, sheet_name=xl_iter2)

            l_m_df.append(m_df)

        full_data = pd.concat(l_m_df, ignore_index=True)
        full_data.head(10)

        file_name_full = "/Users/anirvin/Downloads/JIPSheets/orderpick_full.csv"

        full_data.to_csv(file_name_full)

    if SWITCHER == 0:

        max_df = pd.read_csv('/Users/anirvin/Downloads/JIPSheets/orderpick_full.csv')

        pick_order = []
        pick_order_number = []

        bottles_asked_delivered = []
        bottle_iter = 0

        print(len(max_df))

        pd.set_option('display.max_columns', None)

        max_df.drop(columns=max_df.columns[0], axis=1, inplace=True)

        print(max_df.head(10))

        # g_max_df = max_df[:30]
        porder = []
        # for pdrow in range(len(g_max_df)):
        for pdrow in range(len(max_df)):

            # if g_max_df.iat[pdrow, 2] not in pick_order_number:
            if max_df.iat[pdrow, 2] not in pick_order_number:

                if pdrow != 0:
                    bottle_iter += 1
                    porder.append(ordercounterr)

                ordercounterr = 0
                # if pdrow < 5:
                    # print("PickOrderNumber\n\n")
                    # print(max_df.iat[pdrow, 2])

                # bottles_asked_delivered.append([g_max_df.iat[pdrow, 2], g_max_df.iat[pdrow, 10], g_max_df.iat[pdrow, 14]])
                bottles_asked_delivered.append([max_df.iat[pdrow, 2], max_df.iat[pdrow, 10], max_df.iat[pdrow, 14]])

                # if pdrow < 5:
                    # print("Bottles\n\n")
                    # print(bottles_asked_delivered)

                pick_order_number.append(max_df.iat[pdrow, 2])
                pick_order.append([max_df.iat[pdrow, 1], max_df.iat[pdrow, 2], max_df.iat[pdrow, 3], max_df.iat[pdrow, 4], max_df.iat[pdrow, 6]])

            else:

                bottles_asked_delivered[bottle_iter][1] += max_df.iat[pdrow, 10]
                bottles_asked_delivered[bottle_iter][2] += max_df.iat[pdrow, 14]
                ordercounterr +=1

        print("Order (Number)")
        porderdf = pd.DataFrame(porder)
        print(porderdf)
        print(len(porderdf))

        print("PICK ORDER\n\n")
        # print(pick_order)

        podf = pd.DataFrame(pick_order)
        print(podf.head())
        print(len(podf))

        print("BottlesDelivered\n\n")
        # print(bottles_asked_delivered)

        bddf = pd.DataFrame(bottles_asked_delivered)
        print(bddf.head())
        print(len(bddf))

        startdatetime = podf.iloc[:, 2]
        enddatetime = podf.iloc[:, 3]

        print(type(startdatetime[0]))
        print(type(enddatetime[0]))

        start_datetime_object, end_datetime_object = [], []

        # REMOVE BOTH IF INCONSISTENT

        start_ele_list = []

        for start_date_ele in range(len(startdatetime)):
            if not pd.isna(startdatetime[start_date_ele]):
                if not isinstance(startdatetime[start_date_ele], str):
                    startdatetime[start_date_ele] = str(startdatetime[start_date_ele])
                start_datetime_object.append(datetime.strptime(startdatetime[start_date_ele], '%Y-%m-%d %H:%M:%S'))
            else:
                start_datetime_object.append(datetime.now())
        for end_date_ele in range(len(enddatetime)):
            if not pd.isna(enddatetime[end_date_ele]):
                if not isinstance(enddatetime[end_date_ele], str):
                    enddatetime[end_date_ele] = str(enddatetime[end_date_ele])
                end_datetime_object.append(datetime.strptime(enddatetime[end_date_ele], '%Y-%m-%d %H:%M:%S'))
            else:
                end_datetime_object.append(datetime.now())

        print(type(start_datetime_object[0]))
        print(type(end_datetime_object[0]))

        print(start_datetime_object[:10])
        print(end_datetime_object[:10])

        print("\n\nSTART & END TIMES\n")

        t_del = []

        print(len(start_datetime_object))
        print(len(end_datetime_object))

        for td in range(len(start_datetime_object)):
            if not pd.isna(start_datetime_object[td]) and not pd.isna(end_datetime_object[td]):
                t_del.append(end_datetime_object[td] - start_datetime_object[td])
            else:
                tot = datetime.now()
                t_del.append(tot-tot)

        # print(t_del)

        bddf['Pick_time'] = t_del

        print(bddf.head())

        # UNCOMMENT TO SAVE EXCEL

        # file_name = "/Users/anirvin/Downloads/JIPSheets/orderpick_1_1.xlsx"
        #
        # bddf.to_excel(file_name)

        print(bddf.mean(axis=0))

        print("\n\n^mean >avg \n\n")

        ovr_avg = pd.to_timedelta(pd.Series(t_del)).mean()

        print("\n\n Overall Average: " + str(ovr_avg))

        bottles_delivered = []
        for bele in bottles_asked_delivered:
            for bbele in range(len(bele)):
                if bbele == 1:
                    bottles_delivered.append(bele[1])

        # for tt in t_del:
        #     tt = int(round(tt))

        bddf['Pick_time'] = pd.to_numeric(bddf['Pick_time'].dt.seconds, downcast='integer')



        # newL = []
        #
        # for tt in t_del:
        #     newL.append(tt.dt.second)

        print("\n\n Picking Time in Secs")

        print(bddf)

        bottling_eff_L = bddf['Pick_time']/bottles_delivered

        print("\n\nBottling Eff:")
        print(bottling_eff_L)

        # for b_ele_b in bottling_eff_L:
        #     if b_ele_b.isnull():
        #         b_ele_b = 0

        # bddf['Bottling Efficiency'] = bottling_eff_L
        #
        # file_name = "/Users/anirvin/Downloads/JIPSheets/orderpick_1_1.xlsx"

        # bddf.to_excel(file_name)

        bddf['Bottling Efficiency'] = bottling_eff_L

        bsum = float(0)
        for ele in bddf['Bottling Efficiency']:
            if pd.isna(ele):
                pass
            else:
                bsum += ele

        full_len = len(bddf['Bottling Efficiency'])
        print(bsum / full_len)

        BDdf = pd.concat([bddf, podf, porderdf], axis=1)

        pd.set_option('display.max_columns', None)

        print(BDdf.head())

        BDdf.set_axis(['order_no', 'b_asked', 'b_delivered', 'Pick_time', 'Bottling_efficiency', 'del_date', 'orderno', 'pickstart', 'pickend', 'picktype', 'numberoforders'], axis=1, inplace=True)

        print(BDdf.head())

        print(len(BDdf['pickstart']))

        print(BDdf.iloc[7525])
        print(BDdf.iloc[41279])

        #pickend- weekly, monthly, confidence interval

        # print(BDdf.iloc[7525])

        monthlist, weeklist = [], []

        # check_file_name_formatted = "/Users/anirvin/Downloads/JIPSheets/orderpick_check.csv"
        #
        # BDdf.to_csv(check_file_name_formatted)

        nalist = []

        for (i, dele) in enumerate(BDdf['pickend']):
            # if i == 41280:
            #     print(BDdf.iloc[41280])
            #     BDdf.drop(BDdf.index[i], axis=0, inplace=True)
            if pd.isna(dele) or pd.isna(BDdf.at[i, 'pickstart']):

                nalist.append(i)
                print(i)
                print("CHECK THIS BAD BOI OUTLIER")
                continue

            else:
                monthlist.append(datetime.strptime(dele, '%Y-%m-%d %H:%M:%S').strftime('%b'))
                weeklist.append(datetime.strptime(dele, '%Y-%m-%d %H:%M:%S').strftime('%U'))

        for dropper in nalist:
            BDdf.drop(BDdf.index[dropper], axis=0, inplace=True) # if still error, check loop iter (i) and actual row index

        print(len(BDdf['pickend']))
        print(len(weeklist))

        BDdf.drop(['orderno', 'pickend', 'del_date'], axis=1, inplace=True)
        BDdf['Week'] = weeklist
        BDdf['Month'] = monthlist

        print(BDdf.head())

        full_file_name_formatted = "/Users/anirvin/Downloads/JIPSheets/orderpick_full_fin_w_order.csv"

        BDdf.to_csv(full_file_name_formatted)



    #     monthcatDF = BDdf.copy(deep=True)
    #     weekcatDF = BDdf.copy(deep=True)
    #     picktypecatDF = BDdf.copy(deep=True)
    #
    #     # print(monthcatDF.groupby('Month').mean())
    #     #
    #     # print(weekcatDF.groupby('Week').mean())
    #     #
    #     # print(picktypecatDF.groupby('picktype').mean())
    #
    #     monthcatDF.set_index('pickstart', inplace=True)
    #
    #     monthcatDF.groupby([monthcatDF.index.month_name()], sort=False)['Pick_time', "Bottling_efficiency"].mean().plot(kind="bar", figsize=(18, 5),
    #                                                                                stacked=False,
    #                                                                                align='center', width=0.9)
    #
    #     plt.show()
    #
    #     print(monthcatDF.groupby('Month')['Pick_time', "Bottling_efficiency"].mean())
    #
    #
    #     # plt.ylabel('Rainfall (mm)')
    #     # plt.xlabel('Year Wise')
    #
    #     weekcatDF.set_index('Week', inplace=True)
    #     print(weekcatDF.groupby('Week')['Pick_time', "Bottling_efficiency"].mean())
    #
    #     # print(picktypecatDF.groupby('picktype', 'Month')['Pick_time', "Bottling_efficiency"].mean())
    #
    #     print(picktypecatDF.groupby('picktype')['Pick_time', "Bottling_efficiency"].mean())
    #
    #     # print(picktypecatDF.groupby('picktype', 'Week')['Pick_time', "Bottling_efficiency"].mean())
    #
    #     fig, ax = plt.subplots()
    #
    #     # ax.set_xticks(np.arange(0, picktypecatDF["Pick_time"].max() + 1, 5))
    #
    #     BDdf["Pick_time"].plot(kind='hist')
    #
    #     plt.show()
    #
    #     plt.savefig('/Users/anirvin/Downloads/JIPSheets/pick_time_frequency_analysis.png')
    #
    #     figg, axg = plt.subplots()
    #
    #     # axg.set_xticks(set(weeklist))
    #
    #     monthcatDF.groupby('picktype')['Bottling_efficiency'].plot(legend=True)
    #
    #     plt.show()
    #
    #     plt.savefig('/Users/anirvin/Downloads/JIPSheets/pick_type_cat_boteff.png')
    #
    elif SWITCHER == 1:

        full_file_name_formatted = "/Users/anirvin/Downloads/JIPSheets/orderpick_full_fin.csv"

        aplt.plot_my_sheet(full_file_name_formatted)

    elif SWITCHER == 4:

        full_file_name_formatted = "/Users/anirvin/Downloads/JIPSheets/orderpick_full_fin.csv"

        CPT.getConversion(full_file_name_formatted)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
