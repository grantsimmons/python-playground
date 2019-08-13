import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('lifespans.csv')
data.head()

print(data)
year = data['Year'].values
male = data['M'].values
female = data['F'].values
plt.plot(year, male, label="Male")
plt.plot(year, female, label="Female")
plt.legend()
plt.show()
