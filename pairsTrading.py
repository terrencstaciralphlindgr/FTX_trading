ftx = {
	'apy_key':'',
	'api_secret':''
}

import datetime
from matplotlib.cbook import Stack
import requests
import pandas as pd
import threading
import datetime
# from client import FtxClient
# from local_settings import ftx as settings


# GET /markets
api_url = 'https://ftx.us/api'

# INDIVIDUAL MARKETS
market_name = 'BTC/USD'
path = f'/markets/{market_name}/orderbook?depth=1'
startTime = datetime.datetime.now() - datetime.timedelta(days=1)
# print(startTime.timestamp())
# print(datetime.datetime.fromtimestamp(startTime.timestamp()))
last24path = f'/markets/{market_name}/candles?resolution={60}&start={startTime.timestamp()}'
url = api_url + last24path

res = requests.get(url).json()
df = pd.DataFrame(res['result'])
df['date'] = pd.to_datetime(df['startTime'])
df = df.set_index('date')
df = df.drop(columns=['startTime', 'time'])
df = df.drop(df.index[list(range(60))]).reset_index(drop=True)

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
