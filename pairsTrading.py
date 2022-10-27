import datetime
from matplotlib.cbook import Stack
import requests
import pandas as pd
import threading
import datetime
import numpy as np
from time import process_time_ns
import math
import window
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

last24hr_ETH = window.Window(ETH_open_n)
last24hr_BTC = window.Window(BTC_open_n)

# Get ratio
# stationary = BTC_open_n / ETH_open_n
# omit = []
# [omit.append(idx) for idx, x in enumerate(stationary) if x == 0 or math.isinf(x)]

# last24Ratio = window.Window(np.delete(stationary, omit))

# mean = np.mean(last24Ratio.arr)

last30m_ETH = window.Window(ETH_open[-30:])
last30m_BTC = window.Window(BTC_open[-30:])



print('Start up run time in ns:', process_time_ns() - start_time)

interval = 5  # Run every 5 seconds (can and should change)
short_BTC_long_ETH = long_BTC_short_ETH = False

def makeOrders(bid: float, bid_size: float, ask: float, ask_size: float) -> None:
    pass
    # use ftx api here

def pullFromMarket() -> None:
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

    # Normalize the data
    # TO DO

    # Update windows
    last24hr_ETH.update(mid_ETH)
    last24hr_BTC.update(mid_BTC)
    last30m_ETH.update(mid_ETH)
    last30m_BTC.update(mid_BTC)

    # Get mean
    stationary = last24hr_BTC.arr / last24hr_ETH
    omit = []
    [omit.append(idx) for idx, x in enumerate(stationary) if x == 0 or math.isinf(x)]
    mean = np.mean(np.delete(stationary, omit))

    last30ratio = last30m_BTC / last30m_ETH
    omit = []
    [omit.append(idx) for idx, x in enumerate(last30ratio) if x == 0 or math.isinf(x)]
    std = np.std(np.delete(last30ratio, omit))


    # MAKE TRADES
    # TO DO, CALC CURR RATIO ACCORDING TO OTHER THINGS ABOVE, IMPLEMENT FUNCTION THAT SENDS IN ORDERS
    if short_BTC_long_ETH:
        if curr_ratio < mean + std * 0.5:
            # CLOSE POSITION
            short_BTC_long_ETH = False
            pass
    elif long_BTC_short_ETH:
        if curr_ratio > mean - std * 0.5:
            # CLOSE POSITION
            long_BTC_short_ETH = False
            pass
    else:
        if curr_ratio > mean + std:
            # short BTC long ETH
            short_BTC_long_ETH = False
            pass
        elif curr_ratio < mean - std:
            # long BTC short ETH
            long_BTC_short_ETH = True
            pass



def startTrading() -> None:
    threading.Timer(interval, startTrading).start()
    pullFromMarket()

startTrading()
