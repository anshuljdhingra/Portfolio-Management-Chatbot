# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 12:08:29 2019

@author: Anshul.Dhingra
"""

import pandas as pd
import time
from alpha_vantage.timeseries import TimeSeries

apikey = 'JL9GIGT0KVN581XQ' 
#apikey2 = 'K9HSCD76XIMHD8VJ'
invst = pd.read_excel('Portfolio.xlsx')
df = pd.DataFrame()

parameters = {'given-name': 'Michael', 'number': '11111', 'currentmarketvalue': 'yes'}

ts1 = TimeSeries(key=apikey,output_format='pandas', indexing_type='integer')

fname = parameters['given-name']
currentvalue = parameters['currentmarketvalue']
folio = parameters['number']

invst['Name'] = invst['Name'].astype('category')
invst = invst[(invst['Name'].str.contains(fname, case=False)) & (invst['Folio No'] == int(folio))]
tckr = invst['Ticker'].tolist()
print(tckr)
start = time.time()
data,meta_data = ts1.get_batch_stock_quotes(symbols=tckr)
data.rename({'2. price' : 'Current Market Price (USD)'}, axis=1, inplace=True)
data.rename({'1. symbol' : 'Ticker'}, axis=1, inplace=True)
data.rename({'4. timestamp' : 'Current Date'}, axis=1, inplace=True)

current = pd.merge(invst, data, on='Ticker', how='inner').drop(['date','3. volume'], axis=1)
current['Current Market Price (USD)'] = current['Current Market Price (USD)'].astype('float')
current['Current Investment (USD)'] = current['Current Market Price (USD)'] * current['Stocks']
print(current)
end = time.time()
print(end-start)