# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 15:25:29 2019

@author: Anshul.Dhingra
"""

import pandas as pd
import time
from alpha_vantage.timeseries import TimeSeries

apikey1 = 'JL9GIGT0KVN581XQ' 
apikey2 = 'K9HSCD76XIMHD8VJ'
invst = pd.read_excel('Portfolio.xlsx')
df = pd.DataFrame()

parameters = {'given-name': 'Michael', 'number': '11111', 'currentmarketvalue': 'yes'}

ts1 = TimeSeries(key=apikey1,output_format='pandas', indexing_type='integer')
ts2 = TimeSeries(key=apikey2,output_format='pandas', indexing_type='integer')

fname = parameters['given-name']
currentvalue = parameters['currentmarketvalue']
folio = parameters['number']

invst['Name'] = invst['Name'].astype('category')
invst = invst[(invst['Name'].str.contains(fname, case=False)) & (invst['Folio No'] == int(folio))]
tckr = invst['Ticker'].tolist()
print(tckr)
start = time.time()
for t in tckr[:2]:
    #data,meta_data = ts1.get_intraday(symbol=t,interval='60min', outputsize='compact')
    data,meta_data = ts1.get_daily(symbol=t, outputsize='compact')
    data = data.iloc[-1,:]
    data['Ticker'] = t
    df = df.append(data, ignore_index=True)
for t in tckr[2:]:
    #data,meta_data = ts1.get_intraday(symbol=t,interval='60min', outputsize='compact')
    data,meta_data = ts2.get_daily(symbol=t, outputsize='compact')
    data = data.iloc[-1,:]
    data['Ticker'] = t
    df = df.append(data, ignore_index=True)
end = time.time()
print(end-start)
df.rename({'4. close' : 'Current Market Price (USD)'}, axis=1, inplace=True)
df.rename({'date' : 'Current Date'}, axis=1, inplace=True)
current = pd.merge(invst, df, on='Ticker', how='inner').drop(['SNo', '1. open', '2. high', '3. low', '5. volume'], axis=1)
current['Current Investment'] = current['Current Market Price (USD)'] * current['Stocks']
