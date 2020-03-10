#   Author: Grant Simmons (gsimmons@stevens.edu)
#   Instructions: Run tester.sh for a few hours before following up with this script
#   Dependencies: inetutils-traceroute (apt), numpy, pandas, matplotlib (python3)

import datetime
from datetime import timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import re
from statistics import mean

servers = {}
raw_files = ['mfa.go.th/trace_mfa.go.th.txt', 'government.kz/trace_government.kz.txt']
date_value = re.compile('(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2}):(\d{2})', re.IGNORECASE)
tr_values = re.compile('([0-9.]+)\s\(([0-9.a-z-]+)\)', re.IGNORECASE)
ms_values = re.compile('([0-9.]+)ms')

for file_name in raw_files:
    with open(file_name, 'r') as infile:
        i = 0
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
                    servers[(tr_search.group(1), tr_search.group(2))] = [({'year': curr_year, 'month': curr_month, 'day': curr_day, 'hour': curr_hour, 'min': curr_min}, re.findall(ms_values, line))]
                else:
                    servers[(tr_search.group(1), tr_search.group(2))].append(({'year': curr_year, 'month': curr_month, 'day': curr_day, 'hour': curr_hour, 'min': curr_min}, re.findall(ms_values, line)))

        with open(str(file_name[:-4] + ".csv"), 'w') as outfile:
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
    data = pd.read_csv(str(file_name[:-4] + ".csv"), parse_dates=['date'], date_parser=mydateparser)
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
    hspace = 0.60
    #Full trace
    all_values = data[['hit 1', 'hit 2', 'hit 3']].stack().reset_index(drop=True).to_frame()#.reset_index(inplace=True, drop=True)
    arr_len = len(all_values.index)
    all_values_sorted = all_values.sort_values(by=[0], na_position='first').reset_index(drop=True)
    all_values_sorted['cdf'] = 1/arr_len * (all_values.index + 1)

    ranges = [i for i in range(500)]

    plt.figure(figsize=(15,10))
    ax = plt.subplot(1,1,1)
    #x = test.index
    y = all_values_sorted[0]
    plt.hist(y,bins=ranges,color='silver') #.plot?
    ax.set(xlim=(-5,475))
    plt.ylabel('Number of occurrences (log)')
    plt.yscale('log')
    plt.xlabel('Delay (ms)')
    plt.title('Distribution and CDF of delays for {}'.format(file_name[:-4]))

    bx = ax.twinx()
    x = all_values_sorted[0]
    y = all_values_sorted['cdf']
    plt.scatter(x,y,s=4,color='navy') #.plot?
    bx.set_ylabel('CDF')
    bx.set_xlabel('Delay (ms)')
    #plt.show()
    plt.savefig(str(file_name[:-4] + '_cumulative.png'), format='png')

    for ip_unique in ip_list: #individual hops
        #ip_unique = '192.168.1.1'
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
        
        ip_dataframe_sorted = ip_dataframe.sort_values(by=['avg']).reset_index(drop=True)
        df_len = len(ip_dataframe_sorted.index)
        ip_dataframe_sorted['cdf'] = 1/df_len * (ip_dataframe_sorted.index + 1)
        print(ip_dataframe_sorted)
        print("Length: ", df_len)
        
        bx = plt.subplot(2,1,2) #CDF
        bx2 = bx.twinx()
        x = ip_dataframe_sorted['avg']
        y = ip_dataframe_sorted['cdf']
        bx2.scatter(x,y,s=4, label=ip_unique, color='navy') #.plot?
        bx.set(xlim=(min(ip_dataframe_sorted['avg']) - 2, max(ip_dataframe_sorted['avg']) + 2))
        bx2.set_ylabel('CDF', color='black')
        plt.xlabel('Delay (ms)')
        plt.title('Distribution and CDF of delays for {} ({})'.format(ip_unique, ip_name_hash[ip_unique]))

        print(ip_dataframe_sorted)
        y = ip_dataframe_sorted['avg']
        bx.hist(y,bins=ranges, color='silver') #.plot?
        bx.set_ylabel('Number of occurrences (log)', color='black')
        bx.set_yscale('log')
        plt.savefig(str(file_name[:-4] + '_{}.png'.format(ip_unique)), format='png')
        #plt.show()
