import datetime
from matplotlib.cbook import Stack
import requests
import pandas as pd
import threading
import datetime
import numpy as np
from time import process_time_ns
import math
# from client import FtxClient
# from local_settings import ftx as settings


# Put key up here when we have it
ftx = {
	'apy_key':'',
	'api_secret':''
}


# Performance calculations
start_time = process_time_ns() 


# GET /markets
api_url = 'https://ftx.us/api'
resolution = 60  # 60 seconds = 1 min resolution


# BTC
market_name = 'BTC/USD'
path = f'/markets/{market_name}/orderbook?depth=1'
startTime = datetime.datetime.now() - datetime.timedelta(days=1)
last24path = f'/markets/{market_name}/candles?resolution={resolution}&start={startTime.timestamp()}'
url = api_url + last24path
urlBTC = api_url + path
res = requests.get(url).json()
df = pd.DataFrame(res['result'])
df = df.drop(df.index[list(range(60))]).reset_index(drop=True)
BTC_open = df['open'].to_numpy()

# ETH
market_name = 'ETH/USD'
path = f'/markets/{market_name}/orderbook?depth=1'
startTime = datetime.datetime.now() - datetime.timedelta(days=1)
last24path = f'/markets/{market_name}/candles?resolution={resolution}&start={startTime.timestamp()}'
url = api_url + last24path
urlETH = api_url + path
res = requests.get(url).json()
df = pd.DataFrame(res['result'])
df = df.drop(df.index[list(range(60))]).reset_index(drop=True)
ETH_open = df['open'].to_numpy()


# NORMALIZE

# Normalize ETH and BTC for last 24 hours and get rid of any 0 entries from both
omit = []
ETH_open_n = (ETH_open - np.min(ETH_open)) / (np.max(ETH_open) - np.min(ETH_open))
[omit.append(idx) for idx, x in enumerate(ETH_open_n) if x == 0]
BTC_open_n = (BTC_open - np.min(BTC_open)) / (np.max(BTC_open) - np.min(BTC_open))
[omit.append(idx) for idx, x in enumerate(BTC_open_n) if x == 0 and idx not in omit]
ETH_open_n = np.delete(ETH_open_n, omit)
BTC_open_n = np.delete(BTC_open_n, omit)

# Get
stationary = BTC_open_n / ETH_open_n
omit = []
[omit.append(idx) for idx, x in enumerate(stationary) if x == 0 or math.isinf(x)]
stationary = np.delete(stationary, omit)

mean = np.mean(stationary)
print(mean)


last30_ETH = ETH_open[-30:]
last30_BTC = BTC_open[-30:]



print('Run time in ns:', process_time_ns() - start_time)
exit()

ETH_ask = (ETH_ask - ETH_ask.min()) / (ETH_ask.max() - ETH_ask.min())
BTC_ask = (BTC_ask - BTC_ask.min()) / (BTC_ask.max() - BTC_ask.min())

TH_ask = (ETH_ask - ETH_ask.min()) / (ETH_ask.max() - ETH_ask.min())
BTC_ask = (BTC_ask - BTC_ask.min()) / (BTC_ask.max() - BTC_ask.min())

print(process_time_ns() - t)

exit()
# Normalize
min_ = pd.Series(ETH_open/BTC_open).min()
max_ = pd.Series(ETH_open/BTC_open).max()
mean_ = pd.Series(ETH_open/BTC_open).mean()


ETH_open = (ETH_open - ETH_open.min()) / (ETH_open.max() - ETH_open.min())
BTC_open = (BTC_open - BTC_open.min()) / (BTC_open.max() - BTC_open.min())

print(df)

urlBTC = api_url + path

market_name = 'ETH/USD'
path = f'/markets/{market_name}/orderbook?depth=1'
urlETH = api_url + path


interval = 1



def pullFromMarket():
    res = requests.get(urlBTC).json()
    df = pd.DataFrame(res)['result']
    BTC_bid = df['bids'][0][0]
    BTC_ask = df['asks'][0][0]
    mid_BTC = (BTC_ask + BTC_bid) / 2

    res = requests.get(urlETH).json()
    df = pd.DataFrame(res)['result']
    ETH_bid = df['bids'][0][0]
    ETH_ask = df['asks'][0][0]
    mid_ETH = (ETH_ask + ETH_bid) / 2





def startTrading():
    threading.Timer(interval, startTrading).start()
    pullFromMarket()

# startTrading()
