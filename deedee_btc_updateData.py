# Needs Documentation
#
#
#
#

# IMPORTS
# -------------------------------------------------------------------------------------------------
from imports import *
# -------------------------------------------------------------------------------------------------

# CONSTANTS
# -------------------------------------------------------------------------------------------------

# -- data from the internet for BTC, ETH, and LTC
# -- set this to wherever you're pulling the date, be it web or local
BTC_DATA_HREF = "https://www.cryptodatadownload.com/cdd/Coinbase_BTCUSD_1h.csv"
ETH_DATA_HREF = "https://www.cryptodatadownload.com/cdd/Coinbase_ETHUSD_1h.csv"
LTC_DATA_HREF = "https://www.cryptodatadownload.com/cdd/Coinbase_LTCUSD_1h.csv"

# -- save address(es) for data files
PROCESSED_DATA_FILE_ADDRESS = "data/btc_eth_ltc_data_normalized.csv"

# the price delta required to initial a BUY or SELL in USD, tinker with this to affect model aggression
# higher values are more conservative, lower values are more aggressive, DO NOT set negative
PRICE_DELTA_REQ = 10.0
# -------------------------------------------------------------------------------------------------

# FUNCTIONS
# -------------------------------------------------------------------------------------------------


# Pull Data from the links above and return all 3 CSV's
def get_data():
    # NOTE: skiprows=1 is necessary because it removed the 'watermark' that throws off the format
    # get BTC data
    btc_data_raw = pd.read_csv(BTC_DATA_HREF, skiprows=1)
    # get ETH data
    eth_data_raw = pd.read_csv(ETH_DATA_HREF, skiprows=1)
    # get LTC data
    ltc_data_raw = pd.read_csv(LTC_DATA_HREF, skiprows=1)
    # check to see if the most recent dates match
    # right now it's just a check, later will return a bool that will halt if there's a mismatch
    if btc_data_raw['Date'][0] == eth_data_raw['Date'][0] == ltc_data_raw['Date'][0]:
        print("Date/Time MATCH, Data Valid")
    else:
        print("ERR: Data/Time MIS-MATCH. This data is not aligned by date.")
    # send it back
    return btc_data_raw, eth_data_raw, ltc_data_raw


# Clean and Combine
def clean_and_combine_data(data):
    combined_sheet = pd.DataFrame()
    combined_sheet["DATE"] = data[0]["Date"]
    for sheet in data:
        sheet_coin = sheet["Symbol"][0][0:3]
        column_names = [sheet_coin + ' OC DELTA',
                        sheet_coin + ' PRICE',
                        sheet_coin + ' VOL USD']
        combined_sheet[column_names[0]] = sheet['Close'] - sheet['Open']
        combined_sheet[column_names[1]] = sheet['Open']
        combined_sheet[column_names[2]] = sheet['Volume USD']
    return combined_sheet


# This function runs through the sheet and notes buys and sells for the learning algorithm
def define_buy_and_sell(sheet):
    sheet['BUY'] = 0.0
    sheet['SELL'] = 0.0
    mask_buy = (PRICE_DELTA_REQ <= sheet['BTC OC DELTA'])
    mask_sell = (sheet['BTC OC DELTA'] <= ((-1) * PRICE_DELTA_REQ))
    sheet.loc[mask_buy, 'BUY'] = 1.0
    sheet.loc[mask_sell, 'SELL'] = 1.0
    sheet['BUY'] = sheet['BUY'].shift(1)
    sheet['SELL'] = sheet['SELL'].shift(1)

    # drop the first row since buy/sell were shifted down
    sheet = sheet.drop([0])

    # print out the data
    total_buys = sheet['BUY'].sum()
    buy_perc = round(100.0 * (total_buys / 29540.0), 2)
    total_sell = sheet['SELL'].sum()
    sel_perc = round(100.0 * (total_sell / 29540.0), 2)
    print("Total Buys: " + str(total_buys) + "  ~ " + str(buy_perc) + "%")
    print("Total Sell: " + str(total_sell) + "  ~ " + str(sel_perc) + "%")
    print("\n\n")
    return sheet


# Normalize all of the numeric data between [0,1]
def normalize_data(sheet):
    cols_to_norm = ['BTC PRICE', 'BTC VOL USD',
                    'ETH PRICE', 'ETH VOL USD',
                    'LTC PRICE', 'LTC VOL USD']
    sheet[cols_to_norm] = sheet[cols_to_norm].apply(lambda x: ((x - x.min()) / (x.max() - x.min())))
    return sheet


# THIS FUNCTION IS NOT CURRENTLY USED -- DO NOT CALL
# This function deletes the last row until the buys = sells
# This will keep the model from being biased to thing buys/sells are more/less common
def equalize_buys_and_sells(sheet):
    num_rows_deleted = 0
    while sheet['BUY'].sum() != sheet['SELL'].sum():
        sheet = sheet[:-1]
        num_rows_deleted += 1
    print(num_rows_deleted)
    return sheet


# Save the data to CSV -- not sure this needs to be its own function, but it keeps things clean
def save_final_data(processed_sheet):
    # save final_data to the desired location which will be accessed by the ML Training and Prediction files
    try:
        processed_sheet.to_csv(PROCESSED_DATA_FILE_ADDRESS)
        print("---> File Saved Successfully! ---> View at: " + PROCESSED_DATA_FILE_ADDRESS)
        print("\n\n\n")
    except Exception as e:
        # if it fails just say it failed, I will work out what to do in the rest of the program later in this event
        # probably a bool returned to let the program know it can continue with prediction
        # this bool is only needed for prediction, since learning won't really be affected
        # the bool should be something to halt prediction and any paper trading until the issue is resolved
        print("!-->There was an error saving the processed file.")
        print(e)
        print("\n\n\n")


# Data Processing Main Function
def main_data_processor():
    print("Processing...")
    data = [0, 0, 0]                                          # define a blank array
    data[0], data[1], data[2] = get_data()                    # get the data and return it to the data array
    combined_sheet = clean_and_combine_data(data)             # combine and return the pre-normal data frame
    buy_sell_def_sheet = define_buy_and_sell(combined_sheet)  # define buys and sells in the sheet
    normal_sheet = normalize_data(buy_sell_def_sheet)         # normalize the numbers in the sheet
    save_final_data(normal_sheet)                         # send the final version of the dataframe to be saved
