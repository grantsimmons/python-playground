import datetime
from datetime import timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import regex
from statistics import mean

servers = {}
raw_files = ['trace_mfa.go.th.txt', 'trace_government.kz.txt']
date_value = regex.compile('(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2}):(\d{2})', regex.IGNORECASE)
tr_values = regex.compile('([0-9.]+)\s\(([0-9.a-z-]+)\)', regex.IGNORECASE)
ms_values = regex.compile('([0-9.]+)ms')

for file_name in raw_files:
    with open(file_name, 'r') as infile:
        i = 0
        file_len = sum(1 for line in infile)
        infile.seek(0)
        num_hits = 0
        curr_day = 0
        curr_hour = 0
        curr_min = 0
        curr_sec = 0
        for line in infile:
            date_search = date_value.search(line)
            tr_search = tr_values.search(line)
            if date_search:
                ms_search = ms_values.search(line)
                num_hits += 1
                curr_year = date_search.group(1)
                curr_month = date_search.group(2)
                curr_day = date_search.group(3)
                curr_hour = date_search.group(4)
                curr_min = date_search.group(5)
                curr_sec = date_search.group(6)
            if tr_search:
                if (tr_search.group(1), tr_search.group(2)) not in servers:
                    servers[(tr_search.group(1), tr_search.group(2))] = [({'year': curr_year, 'month': curr_month, 'day': curr_day, 'hour': curr_hour, 'min': curr_min}, regex.findall(ms_values, line))]
                else:
                    servers[(tr_search.group(1), tr_search.group(2))].append(({'year': curr_year, 'month': curr_month, 'day': curr_day, 'hour': curr_hour, 'min': curr_min}, regex.findall(ms_values, line)))

        with open(str(file_name[:-3] + ".csv"), 'w') as outfile:
            outfile.write('IP,name,date,hit 1,hit 2,hit 3,avg\n')
            for server in servers:
                print(server)
                for time, ms in servers[server]:
                    print("Time: Feb. {}, {}:{},".format(time['day'], time['hour'], time['min']))
                    #print("ms: ", ms)
                    ms_avg = mean(float(i) for i in ms)
                    print("ms average: ", ms_avg)
                    outfile.write('{},{},{}-{}-{} {}:{},'.format(server[0], server[1], time['year'], time['month'], time['day'], time['hour'], time['min']))
                    for i in range(3):
                        try:
                            outfile.write('{},'.format(ms[i]))
                        except:
                            outfile.write(',')
                    outfile.write('{}\n'.format(ms_avg))


    mydateparser = lambda x: pd.datetime.strptime(x, "%Y-%m-%d %H:%M")
    data = pd.read_csv(str(file_name[:-3] + ".csv"), parse_dates=['date'], date_parser=mydateparser)
    data.head()
    dataframe = pd.DataFrame(data)
    print(dataframe[dataframe.IP == '192.168.1.1'])
    print(type(data.date))

    ip_name_hash = {}

    ip_list = [str(i) for i in np.unique(data['IP'].values)]
    for ip in ip_list:
        ip_name = data[(data.IP == ip)]
        if ip not in ip_name_hash:
            ip_name_hash[ip] = ip_name.iloc[0]['name']
    print(ip_name_hash)

    #print(np.unique(ip))
    left = 0.125
    bottom = 0.11
    right = 0.90
    top = 0.88
    wspace = 0.20
    hspace = 0.40
    #Full trace
    all_values = data[['hit 1', 'hit 2', 'hit 3']].stack().reset_index(drop=True).rename_axis(('value',))
    arr_len = len(all_values.index)
    all_values_sorted = all_values.sort_values().reset_index(drop=True)
    #all_values['cdf'] = 1/arr_len * (all_values.index + 1)
    print(all_values)
    nan_arr = np.isnan(all_values)
    non_nan_arr = ~nan_arr
    #for index, value in enumerate(all_values):
    #    cdf = 1/arr_len * (index + 1)
    #    all_values_cdf.append((value, cdf))
    #print(all_values_cdf)

    #plt.figure(figsize=(15,10))
    #x = i[0] for i in all_values_cdf
    #y = i[1] for i in all_values_cdf
    #plt.scatter(x,y,s=4) #.plot?
    #plt.ylabel('CDF')
    #plt.xlabel('Delay (ms)')
    #plt.title('CDF of {}'.format(file_name[:-3]))
    #plt.show()

    #    if index % 50 == 0:
    #        print('\n')
    #    if np.isnan(value):
    #        print("whoops")
    #    print(value, end=' ')


'''    
    for ip_unique in ip_list: #individual hops
        ip_dataframe = data[data.IP == ip_unique]
        plt.figure(figsize=(15,10))
        plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
        
        ax = plt.subplot(2,1,1)
        x = ip_dataframe['date']
        y = ip_dataframe['avg']
        plt.scatter(x,y,s=4, label=ip_unique) #.plot?
        plt.axis([min(ip_dataframe['date']) - timedelta(hours=1), max(ip_dataframe['date']) + timedelta(hours=1), min(ip_dataframe['avg']) - 1 , max(ip_dataframe['avg']) + 1])
        plt.ylabel('Delay (ms)')
        plt.xlabel('Time')
        ax.xaxis.set_minor_locator(dates.HourLocator())
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))
        ax.xaxis.set_major_locator(dates.DayLocator())
        ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M\n%b\n%d'))
        plt.title('{} ({})'.format(ip_unique, ip_name_hash[ip_unique]))
        #plt.legend()
        
        ip_dataframe_sorted = ip_dataframe.sort_values(by=['avg']).reset_index(drop=True)
        df_len = len(ip_dataframe_sorted.index)
        ip_dataframe_sorted['cdf'] = 1/df_len * (ip_dataframe_sorted.index + 1)
        print(ip_dataframe_sorted)
        print("Length: ", df_len)
        
        plt.subplot(2,1,2) #CDF
        x = ip_dataframe_sorted['avg']
        y = ip_dataframe_sorted['cdf']
        plt.scatter(x,y,s=4, label=ip_unique) #.plot?
        #plt.axis([min(ip_dataframe['date']) - timedelta(hours=1), max(ip_dataframe['date']) + timedelta(hours=1), min(ip_dataframe['avg']) - 1 , max(ip_dataframe['avg']) + 1])
        plt.ylabel('CDF')
        plt.xlabel('Delay (ms)')
        plt.title('CDF function for {} ({})'.format(ip_unique, ip_name_hash[ip_unique]))
        plt.show()
'''
