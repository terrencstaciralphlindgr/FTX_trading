import pandas as pd
import numpy as np
import math
import statsmodels.tsa.stattools as tools
from tardis_test import date
import matplotlib.pyplot as plt

step = 1

ETH_data = pd.read_csv("{}_ETH-USD.csv".format(date))[::step]
BTC_data = pd.read_csv("{}_BTC-USD.csv".format(date))[::step]

ETH_ask = ETH_data["ask_price"]
BTC_ask = BTC_data["ask_price"]


ETH_ask = (ETH_ask - ETH_ask.min()) / (ETH_ask.max() - ETH_ask.min())
BTC_ask = (BTC_ask - BTC_ask.min()) / (BTC_ask.max() - BTC_ask.min())

stationary = pd.Series(ETH_ask/BTC_ask)
omit = []
for num, x in enumerate(stationary):
    if (x == 0 or math.isinf(x)): omit.append(num)
stationary = stationary.drop(stationary.index[omit]).reset_index(drop=True)
mean = stationary.mean()

print((mean_ - min)/(max-min))
print(mean)

date_ = "2022-10-24"

ETH_data = pd.read_csv("{}_ETH-USD.csv".format(date_))[::step].reset_index(drop=True)
BTC_data = pd.read_csv("{}_BTC-USD.csv".format(date_))[::step].reset_index(drop=True)


ETH_ask = ETH_data["ask_price"]
BTC_ask = BTC_data["ask_price"]

ETH_ask = (ETH_ask - ETH_ask.min()) / (ETH_ask.max() - ETH_ask.min())
BTC_ask = (BTC_ask - BTC_ask.min()) / (BTC_ask.max() - BTC_ask.min())


ratio = pd.Series(ETH_ask/BTC_ask)
omit = []
for num, x in enumerate(ratio):
    if (x == 0 or math.isinf(x)): omit.append(num)
ratio = ratio.drop(ratio.index[omit]).reset_index(drop=True)

stds = ratio.rolling(30).std()


lower_line = mean - stds
upper_line = mean + stds



for num, std in enumerate(stds):
    if ratio[num] > mean + std: 
        print("Greater {}".format(num))
    elif ratio[num] < mean - std: 
        print("Less {}".format(num))
    else: 
        print("Return {}".format(num))

x = [x + 1 for x in range(len(ratio))]

print(lower_line[-5:])
print(upper_line[-5:])

plt.plot(x, ratio, label = "line 1")
plt.plot(x, lower_line, label = "line 2")
plt.plot(x, upper_line, label = "line 3")
plt.legend()
plt.show()



# print(stationary.rolling(30).std().mean())
# print(tools.adfuller(ETH_ask))
# print(tools.adfuller(BTC_ask))
# print(tools.coint(ETH_ask, BTC_ask))
# print(tools.adfuller(ETH_ask/BTC_ask))

