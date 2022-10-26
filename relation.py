import pandas as pd
import numpy as np

import time;
from tardis_test import date


BTC_data = pd.read_csv("datasets/ftx-us_book_ticker_{}_BTC-USD.csv".format(date))
ETH_data = pd.read_csv("datasets/ftx-us_book_ticker_{}_ETH-USD.csv".format(date))


BTC_data['timestamp'] = pd.to_datetime(BTC_data['timestamp'], unit='us').dt.ceil(freq='min')  
ETH_data['timestamp'] = pd.to_datetime(ETH_data['timestamp'], unit='us').dt.ceil(freq='min')  
BTC_data['local_timestamp'] = pd.to_datetime(BTC_data['local_timestamp'], unit='us').dt.ceil(freq='min')  
ETH_data['local_timestamp'] = pd.to_datetime(ETH_data['local_timestamp'], unit='us').dt.ceil(freq='min')  

def clean(df):
    prev_stamp = None
    prev_ask = df['ask_price'][0]
    count = 0
    omit = []
    percent_change = []
    for time_stamp, ask_price in zip(df['timestamp'], df['ask_price']):
        if time_stamp != prev_stamp:
            prev_stamp = time_stamp
            percent_change.append((ask_price - prev_ask) / ask_price)
            prev_ask = ask_price
        else:
            omit.append(count)
        count += 1

    df = df.drop(omit).reset_index(drop=True)
    df['local_timestamp'] = pd.Series(percent_change)
    df = df.rename(columns={'local_timestamp':'%_change'})
    return df

BTC_data = clean(BTC_data)
ETH_data = clean(ETH_data)
ETH_data = ETH_data.drop([0])
print(BTC_data.head())
print(ETH_data.head())





BTC_data.to_csv('{}_BTC-USD.csv'.format(date))
ETH_data.to_csv('{}_ETH-USD.csv'.format(date))
