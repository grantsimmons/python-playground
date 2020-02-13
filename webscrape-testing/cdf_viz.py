import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

with open("ping_results_sorted.txt", 'r') as infile:
    with open("cdf.csv", 'w') as outfile:
        outfile.write("Ping,Val\n")
        i = 0
        file_len = sum(1 for line in infile)
        infile.seek(0)
        for line in infile:
            #print(line + ' ' + str(i))
            val = int(line.strip('\n'))
            outfile.write(str(val) + ',' + str(i) + '\n')
            i += float(1/file_len)

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
