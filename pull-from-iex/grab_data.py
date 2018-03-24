#!/usr/bin/env python
"---
Author: A Dunning
Date: March 2018
Description: Code for pulling financial instrument data from IEX API, for instruments tradeable on Plus500. Uses pandas datareader to pull data and pickle to condense.
---"
import pandas as pd
import pandas_datareader as wb
import matplotlib.pyplot as plt
import datetime
import pickle

"set start and end date for data pull"
start = datetime.datetime(2015,1,1)
end = datetime.datetime(2018,1,1)

"function to get a list of all financial instruments on Plus500, using the downloaded .html file from https://www.plus500.com/Instruments"
def get_instruments():
    inst = pd.read_html("Plus500Instruments.html")
    df_i = pd.DataFrame()
    for data in inst:
        if df_i.empty:
            df_i = pd.DataFrame(data)
        else:
            df_i = df_i.append(data)
    df_i.reset_index(inplace=True)
    df_i.to_pickle('Instruments.pickle')

"function to get a list of available symbols on iex from their webpage, downloaded to local as .html from https://iextrading.com/trading/eligible-symbols/"
def get_iex_symbols():
    sym = pd.read_html("IEXSymbols_complete.html")
    sym = pd.DataFrame(sym[0])
    sym.to_pickle('Symbols.pickle')

"function to get data from iex for a given symbol"
def get_iex_data(s):
    df_data = wb.DataReader(str(s),'iex',start,end)
    return df_data

"function to generate the full set of instrument data where available on iex. Only grabs 'open' from ohlcv"
def generate_full():
    df_full = pd.DataFrame()
    for symbol in df_overlap['Symbol']:
        "try to get the data; if there is an error, skip to the next symbol"
        try: 
            df_d = get_iex_data(str(symbol))['open']
        except:
            continue
        df_d = pd.DataFrame(df_d)
        df_d.columns = [str(symbol)]
        if df_full.empty:
            df_full = df_d
        else:
            df_full[str(symbol)] = df_d[str(symbol)]
    df_full.to_pickle('data_output.pickle') 

"run the get_instruments and get_symbols methods once to read and pickle data"
#get_instruments()
df_inst = pd.read_pickle('Instruments.pickle')
#get_iex_symbols()
df_sym = pd.read_pickle('Symbols.pickle')

"get symbols that are in both instruments and iex symbols"
df_overlap = df_inst[df_inst['Symbol'].isin(df_sym['Symbol'])]

"grab existing instrument data from iex. Takes some time!"
#generate_full()
df_all = pd.read_pickle('data_output.pickle')


