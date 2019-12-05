# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 10:13:36 2019

@author: Anshul.Dhingra
"""

# import needed libraries
import quandl
import pandas as pd

invst = pd.read_excel('Portfolio.xlsx')

# add quandl API key for unrestricted
quandl.ApiConfig.api_key = 'o7uZ8aYHTAe-ZXazTJ_t'

# get the table for daily stock prices and,
# filter the table for selected tickers, columns within a time range
# set paginate to True because Quandl limits tables API to 10,000 rows per call
data = quandl.get_table('WIKI/PRICES', ticker = ['AAPL'], 
                        qopts = { 'columns': ['ticker', 'date', 'adj_close'] }, 
                        date = { 'gte': '2015-12-30', 'lte': '2015-12-31' }, 
                        paginate=True)
print(data)

# create a new dataframe with 'date' column as index
new = data.set_index('date')

# use pandas pivot function to sort adj_close by tickers
clean_data = new.pivot(columns='ticker')
