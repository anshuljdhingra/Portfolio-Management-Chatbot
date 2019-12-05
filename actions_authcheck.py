    # -*- coding: utf-8 -*-
    """
    Created on Wed Aug 21 14:19:28 2019
    
    @author: Anshul.Dhingra
    """

import pandas as pd
exl = pd.read_excel('Portfolio.xlsx')

parameters = {'given-name': 'Dwight', 'folio': '22222', 'last-name': ''}



exl['Name'] = exl['Name'].astype('category')

exl = exl[(exl['Name'].str.contains(fname, case=False)) & (exl['Folio No'] == int(folio))]
filtered_exl = exl[['Companies', 'Stocks', 'Purchase Date','Purchase Price(INR)', 'Investment']]
total_investment = filtered_exl.Investment.sum()
filtered_exl_dict = filtered_exl.to_dict(orient='records')
print(filtered_exl_dict)
print(type(filtered_exl_dict))
filtered_exl_dict.append({'Total Investments':total_investment})
print(filtered_exl_dict)
# return a fulfillment response
