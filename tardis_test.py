# requires Python >=3.6
# pip install tardis-dev

from tardis_dev import datasets, get_exchange_details
import logging
import os
import pandas as pd

date = "2022-10-23"

if __name__ == '__main__':
    exchange = 'ftx-us'
    exchange_details = get_exchange_details(exchange)   
    allowed_symbols = ['ETH-USD', 'BTC-USD']


    for symbol in exchange_details["datasets"]["symbols"]:
        
        symbol_id = symbol["id"]
        if symbol_id not in allowed_symbols: continue

        data_types = ['book_ticker'] #symbol["dataTypes"]  
        from_date = "{}T00:00:00.000Z".format(date) #symbol["availableSince"]
        to_date = "{}T00:00:00.000Z".format(date) #symbol["availableTo"]

        print(f"Downloading {exchange} {data_types} for {symbol_id} from {from_date} to {to_date}")

        datasets.download(
            exchange = exchange,
            data_types = data_types,
            from_date =  from_date,
            to_date = to_date,
            symbols = [symbol_id],
            api_key = "pyxqIQxeooyMo-6iWms8xfxOtdkeADrPBa3iHj0_",
            download_dir = "./datasets",
        )

    os.chdir("datasets")
    for filename in os.listdir():
        os.system("gzip -d " + filename)

    os.chdir("../")

    BTC_data = pd.read_csv("datasets/ftx-us_book_ticker_{}_BTC-USD.csv".format(date))
    ETH_data = pd.read_csv("datasets/ftx-us_book_ticker_{}_ETH-USD.csv".format(date))


    BTC_data['timestamp'] = pd.to_datetime(BTC_data['timestamp'], unit='us').dt.ceil(freq='s')  
    ETH_data['timestamp'] = pd.to_datetime(ETH_data['timestamp'], unit='us').dt.ceil(freq='s')  
    BTC_data['local_timestamp'] = pd.to_datetime(BTC_data['local_timestamp'], unit='us').dt.ceil(freq='s')  
    ETH_data['local_timestamp'] = pd.to_datetime(ETH_data['local_timestamp'], unit='us').dt.ceil(freq='s')  

    def clean(df):
        prev_stamp = None
        omit = []
        for num, time_stamp in enumerate(df['timestamp']):
            if time_stamp != prev_stamp:
                prev_stamp = time_stamp
            else:
                omit.append(num)

        return df.drop(omit).reset_index(drop=True)

    BTC_data = clean(BTC_data)
    ETH_data = clean(ETH_data)

    print(BTC_data.head())