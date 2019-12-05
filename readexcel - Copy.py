# import flask dependencies
from flask import Flask, request, make_response, jsonify
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time,json
# initialize the flask app
app = Flask(__name__)

# default route
@app.route('/')
def index():
    return 'Hello World!'

# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)
    print('input request',req)
    # fetch action from json
    action = req.get('queryResult').get('action')
    #print('action',action)
    if action == 'read_excel' :
        parameters = req['queryResult']['parameters']
        print('action',action)
        print('parameters', parameters)
        exl = pd.read_excel('Portfolio.xlsx')
    
        fname = parameters['given-name']
        lname = parameters['last-name']
        folio = parameters['number']
    
        exl['Name'] = exl['Name'].astype('category')
        exl['Purchase Date'] = exl['Purchase Date'].astype('str')
    
        exl = exl[(exl['Name'].str.contains(fname, case=False)) & (exl['Folio No'] == int(folio))]
        filtered_exl = exl[['Companies', 'Stocks', 'Purchase Date','Purchase Price(USD)', 'Purchase Investment (USD)']]
        total_investment = round(filtered_exl['Purchase Investment (USD)'].sum(),2)
        filtered_exl_dict = filtered_exl.to_dict(orient='records')
        filtered_exl_dict.append({'Total Purchase Investments (USD)':round(total_investment,2)})
        filtered_exl_dict.append({'These are your investmets.Would you like to know current Market Value of your Investments or your best/worst performing stocks, ':fname})
        filtered_exl_dict = json.dumps(filtered_exl_dict) 
        print((filtered_exl_dict))
        print(type(filtered_exl_dict))
        #filtered_exl_dict.append({'Total Purchase Investments (USD)':round(total_investment,2)})
        #print(filtered_exl_dict)
        #filtered_exl_dict = '.'.join(str(x) for x in filtered_exl_dict)
     
        #filtered_exl_dict = filtered_exl_dict.replace('}.{', '},{')
        #filtered_exl_dict = filtered_exl_dict.replace('\'', '"')
        # return a fulfillment response
        if len(filtered_exl) != 0:
            print(filtered_exl_dict)
            return {'fulfillmentText': filtered_exl_dict}
            #return filtered_exl_dict
        else:
            return {'fulfillmentText':'User Authetication Error.We are not able to authenticate your details. Please  enter correct Name & Folio Number. Thanks.'}
        
        
    elif action == 'marketvalueaction':
        
        parameters = req['queryResult']['parameters']
        print('action',action)
        print('parameters', parameters)
        
        apikey = 'JL9GIGT0KVN581XQ' 
        invst = pd.read_excel('Portfolio.xlsx')
               
        ts1 = TimeSeries(key=apikey,output_format='pandas', indexing_type='integer')
        fname = parameters['given-name']
        currentvalue = parameters['currentmarketvalue'].lower()
        folio = parameters['number']
        
        if ((currentvalue == 'current market value')): #or (currentvalue == 'sure') or (currentvalue == 'ok') or (currentvalue == 'okay')) :
            
            invst['Name'] = invst['Name'].astype('category')
            invst = invst[(invst['Name'].str.contains(fname, case=False)) & (invst['Folio No'] == int(folio))]
            tckr = invst['Ticker'].tolist()
            start = time.time()        
            data,meta_data = ts1.get_batch_stock_quotes(symbols=tckr)
            data.rename({'2. price' : 'Current Market Price (USD)'}, axis=1, inplace=True)
            data.rename({'1. symbol' : 'Ticker'}, axis=1, inplace=True)
            data.rename({'4. timestamp' : 'Current Date'}, axis=1, inplace=True)
            
            current = pd.merge(invst, data, on='Ticker', how='inner').drop(['date','3. volume'], axis=1)
            current['Current Market Price (USD)'] = current['Current Market Price (USD)'].astype('float')
            current['Current Investment (USD)'] = current['Current Market Price (USD)'] * current['Stocks']
    
            filtered_current = current[['Companies','Stocks', 'Purchase Price(USD)','Purchase Investment (USD)','Current Market Price (USD)','Current Investment (USD)']]
            current_total = filtered_current['Current Investment (USD)'].sum()
            filtered_current_dict = filtered_current.to_dict(orient='records')
            filtered_current_dict.append({'Total Purchase Investments (USD)':round(current_total,2)})
            filtered_current_dict.append({'These are current market valuations of your investments.Is there anything else i can help you with?,':fname})
            filtered_current_dict = json.dumps(filtered_current_dict) 
            print((filtered_current_dict))
            print(type(filtered_current_dict))
            
            end = time.time()
            print('API time ', end-start)
            # return a fulfillment response
            if len(filtered_current) != 0:
                return {'fulfillmentText': filtered_current_dict}
            else:
                return {'fulfillmentText':'Please enter whether you would like to see current market value of your investments or not.Thanks.'}
        elif ((currentvalue == 'no') or (currentvalue == 'nope') or (currentvalue == 'not')):
            return {'fulfillmentText':'Alright.'}
 
    elif action == 'performeractions':
        
        parameters = req['queryResult']['parameters']
        print('action',action)
        print('parameters', parameters)
        
        apikey = 'K9HSCD76XIMHD8VJ' 
        invst = pd.read_excel('Portfolio.xlsx')
               
        ts1 = TimeSeries(key=apikey,output_format='pandas', indexing_type='integer')
        fname = parameters['given-name']
        performer = parameters['performerentity'].lower()
        folio = parameters['number']
                            
        invst['Name'] = invst['Name'].astype('category')
        invst = invst[(invst['Name'].str.contains(fname, case=False)) & (invst['Folio No'] == int(folio))]
        tckr = invst['Ticker'].tolist()
        start = time.time()        
        data,meta_data = ts1.get_batch_stock_quotes(symbols=tckr)
        data.rename({'2. price' : 'Current Market Price (USD)'}, axis=1, inplace=True)
        data.rename({'1. symbol' : 'Ticker'}, axis=1, inplace=True)
        data.rename({'4. timestamp' : 'Current Date'}, axis=1, inplace=True)
        
        current = pd.merge(invst, data, on='Ticker', how='inner').drop(['date','3. volume'], axis=1)
        current['Current Market Price (USD)'] = current['Current Market Price (USD)'].astype('float')
        current['Current Investment (USD)'] = current['Current Market Price (USD)'] * current['Stocks']
        
        filtered_current = current[['Companies','Stocks', 'Purchase Price(USD)','Purchase Investment (USD)','Current Market Price (USD)','Current Investment (USD)']]
        current_total = filtered_current['Current Investment (USD)'].sum()
        
        filtered_current['Stock Profit/Loss (USD)'] = filtered_current['Current Investment (USD)'] - filtered_current['Purchase Investment (USD)']
        filtered_current['Stock Profit/Loss (USD)'] = round(filtered_current['Stock Profit/Loss (USD)'],2)
        best = filtered_current[filtered_current['Stock Profit/Loss (USD)'] == filtered_current['Stock Profit/Loss (USD)'].max()]
        worst = filtered_current[filtered_current['Stock Profit/Loss (USD)'] == filtered_current['Stock Profit/Loss (USD)'].min()]
        end = time.time()
        print('API time ', end-start)
        
        if performer == 'good':
            best = best[['Companies','Stocks','Stock Profit/Loss (USD)']]
            filtered_current_dict = best.to_dict(orient='records')
            filtered_current_dict.append({'This is your best performing stock.Is there anything else i can help you with?,':fname})
            filtered_current_dict = json.dumps(filtered_current_dict) 
            print(filtered_current_dict)
            return {'fulfillmentText': filtered_current_dict}
        elif performer == 'bad':
            worst = worst[['Companies','Stocks','Stock Profit/Loss (USD)']]
            filtered_current_dict = worst.to_dict(orient='records')
            filtered_current_dict.append({'This is your worst performing stock.Is there anything else i can help you with?,':fname})
            filtered_current_dict = json.dumps(filtered_current_dict) 
            print(filtered_current_dict)
            return {'fulfillmentText': filtered_current_dict}
            
        #print(filtered_current_dict)
        #print(type(filtered_current_dict))
        #filtered_current_dict.append({'Current Market Value of All Investments (USD)':round(current_total,2)})
        
        else:
            return {'fulfillmentText':'Please provide input for either a best or worst performing stock.Thanks.'}

           
    elif action == 'goodbyeaction':
        
        parameters = req['queryResult']['parameters']
        print('action',action)
        print('parameters', parameters)       
        goodbye = parameters['goodbyeentity'].lower()
        if ((goodbye == 'yes')): #or (currentvalue == 'sure') or (currentvalue == 'ok') or (currentvalue == 'okay')) :
            return {'fulfillmentText':'Alright sure, I can help you with your investment history, current market value of your investments or your best/worst performing stocks.'}
        elif ((goodbye == 'no')): #or (currentvalue == 'nope') or (currentvalue == 'not')):
            return {'fulfillmentText':'Thanks for using Portfolio Bot.Have a good day!.'}
        
    else:
        return {'fulfillmentText':'Sorry,i am not able to understand this.'}

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    #return make_response(jsonify(results()))
    return make_response((results()))
# run the app
if __name__ == '__main__':
   app.run(host='172.18.51.197',port='5000')