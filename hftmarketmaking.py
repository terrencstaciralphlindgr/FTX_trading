ftx = {
	'apy_key':'',
	'api_secret':''
}

import datetime
import requests
import pandas as pd
import threading
import avellaneda as av
# from client import FtxClient
# from local_settings import ftx as settings



# GET /markets
api_url = 'https://ftx.us/api'

# GET /markets/{market_name}
market_name = 'BTC/USD'
path = f'/markets/{market_name}/orderbook?depth=1'
url = api_url + path

# res = requests.get(url).json()
# df = pd.DataFrame(res)['result']
# bid = df['bid']
# print(bid, type(bid))
# ask = df['ask']
# print(ask, type(ask))

interval = 0.1
t = 0
MAX_TIME = 36000

def pullFromMarket():
    res = requests.get(url).json()
    df = pd.DataFrame(res)['result']
    bid = df['bids'][0][0]
    print('Bid', bid)
    ask = df['asks'][0][0]
    print('Ask', ask)

    mid_price = (bid + ask) / 2

    reserveB, reserveA = av.getOptimalOrder(mid_price, sigma, t/MAX_TIME, gamma, q) 

    t += 1
    if t > MAX_TIME:
        t = 0





def startTimer():
    threading.Timer(interval, startTimer).start()
    pullFromMarket()

startTimer()
