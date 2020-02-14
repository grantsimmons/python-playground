import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

servers = {}
tr_values = re.compile('\s*\d+\s*([0-9.]*)\s\(([0-9.a-z-]*)\)\s+([0-9.]*)ms\s+([0-9.]*)ms\s+([0-9.]*)ms', re.IGNORECASE)
with open("tracert_output.txt", 'r') as infile:
    i = 0
    file_len = sum(1 for line in infile)
    infile.seek(0)
    for line in infile:
        tr_search = tr_values.search(line)
        try:
            if (tr_search.group(1), tr_search.group(2)) not in servers:
                servers[(tr_search.group(1), tr_search.group(2))] = tuple(tr_search.group(i) for i in range(3,6))
            else:
                servers[(tr_search.group(1), tr_search.group(2))] += (tuple(tr_search.group(i) for i in range(3,6)))
        except:
            print("None value exception")
    print(servers)
                
#val = int(line.strip('\n'))
#outfile.write(str(val) + ',' + str(i) + '\n')
#i += float(1/file_len)

    '''
data = pd.read_csv('cdf.csv')
data.head()

print(data)
ping = data['Ping'].values
values = data['Val'].values
plt.plot(ping, values, label="Ping")
plt.ylabel('CDF of ping values')
plt.xlabel('Ping')
plt.title('CDF of ping to settlers.org.za between 4 and 7pm')
plt.legend()
plt.show()
    '''
