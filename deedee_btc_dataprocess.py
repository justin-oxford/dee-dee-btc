#
#
#
#
#

# IMPORT LIST
import numpy as np
import pandas as pd
from sklearn import preprocessing
import matplotlib.pyplot as plt

# CONSTANTS
PRICE_DELTA = 5  # in dollars, what amount triggers a buy/sell


# This function finds the difference between two numbers... open and close
def process_find_price_delta(start, end):
    return end - start


# This function runs through the Data CSV and denotes whether a buy or a sell should occur
# Then it place the corresponding value for buy/sell in the column
def process_buy_sell():
    data_raw = pd.read_csv("data/btc_data.csv", header=0)
    data_raw['BUY'] = 0
    data_raw['SELL'] = 0
    print(data_raw)
    mask_buy = (data_raw['BTC OPEN'] < (data_raw['BTC CLOSE'] - PRICE_DELTA))
    mask_sell = (data_raw['BTC OPEN'] > (data_raw['BTC CLOSE'] + PRICE_DELTA))
    data_raw.loc[mask_buy, 'BUY'] = 1
    data_raw.loc[mask_sell, 'SELL'] = 1
    data_raw["BTC OC DELTA"] = process_find_price_delta(data_raw["BTC OPEN"], data_raw["BTC CLOSE"])
    data_raw["BTC OH DELTA"] = process_find_price_delta(data_raw["BTC OPEN"], data_raw["BTC HIGH"])
    data_raw["BTC OL DELTA"] = process_find_price_delta(data_raw["BTC OPEN"], data_raw["BTC LOW"])
    data_raw["ETH OC DELTA"] = process_find_price_delta(data_raw["ETH OPEN"], data_raw["ETH CLOSE"])
    data_raw["ETH OH DELTA"] = process_find_price_delta(data_raw["ETH OPEN"], data_raw["ETH HIGH"])
    data_raw["ETH OL DELTA"] = process_find_price_delta(data_raw["ETH OPEN"], data_raw["ETH LOW"])
    data_raw["LTC OC DELTA"] = process_find_price_delta(data_raw["LTC OPEN"], data_raw["LTC CLOSE"])
    data_raw["LTC OH DELTA"] = process_find_price_delta(data_raw["LTC OPEN"], data_raw["LTC HIGH"])
    data_raw["LTC OL DELTA"] = process_find_price_delta(data_raw["LTC OPEN"], data_raw["LTC LOW"])

    cols_to_norm = ['BTC OC DELTA', 'BTC OH DELTA', 'BTC OL DELTA',
                    'ETH OC DELTA', 'ETH OH DELTA', 'ETH OL DELTA',
                    'LTC OC DELTA', 'LTC OH DELTA', 'LTC OL DELTA',
                    'BTC VOL USD', 'ETH VOL USD', 'LTC VOL USD']
    data_raw[cols_to_norm] = data_raw[cols_to_norm].apply(lambda x: ((x - x.min()) / (x.max() - x.min())))

    old_cols = ["BTC OPEN", "BTC HIGH", "BTC LOW", "BTC CLOSE", "BTC VOL",
                "ETH OPEN", "ETH HIGH", "ETH LOW", "ETH CLOSE", "ETH VOL",
                "LTC OPEN", "LTC HIGH", "LTC LOW", "LTC CLOSE", "LTC VOL",
                "UNIX"]
    data_final = data_raw.drop(old_cols, axis=1)
    print(data_final)
    data_final.to_csv("data/btc_data_processed.csv")
