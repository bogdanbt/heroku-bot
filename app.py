#from http import server
import json
from statistics import mean
import requests
from flask import Flask, request, jsonify
from binance.client import Client
from binance.enums import *
import telegram
chat_id='425745139'
api_key='5545278299:AAHIqGnUM6mrgB0fe8DWsUMZrrpDU1BQ8jI'
bot = telegram.Bot(token=api_key)


api_keys='MJXjYzcIxaPjYELP5L6DLieRDhtcPkQndqqIy0aILO6b1pCIWcavtTf82RbAoNxx'
api_secret='aDBRznWCHBQCzbALB3B1biPuyfuR9PDO2v9W03pJ8E2psO4fLDkvcBlWxIdB2NZq'

def get_price(symbol):
    price = client.get_symbol_ticker(symbol=symbol)['price']
    return float(price)

def get_info_minsizecoin(symbol):
    #https://stackoverflow.com/questions/71245810/find-tick-size-for-a-symbol-futures-binance//////////////
    data = client.futures_exchange_info()
    found = False
    info = data['symbols']
    for s in range(len(info)):
        if info[s]['symbol'] == symbol:
            filters = info[s]['filters']
            for f in range(len(filters)):
                if filters[f]['filterType'] == 'LOT_SIZE':
                    #print(filters[f])
                    tick_size = float(filters[f]['minQty'])
                    found = True
                    #print(tick_size)
                    break
            break
    return tick_size

def get_info_maxsizecoin(symbol):
    #https://stackoverflow.com/questions/71245810/find-tick-size-for-a-symbol-futures-binance//////////////
    data = client.futures_exchange_info()
    found = False
    info = data['symbols']
    for s in range(len(info)):
        if info[s]['symbol'] == symbol:
            filters = info[s]['filters']
            for f in range(len(filters)):
                if filters[f]['filterType'] == 'LOT_SIZE':
                    #print(filters[f])
                    tick_size = float(filters[f]['maxQty'])
                    found = True
                    #print(tick_size)
                    break
            break
    return tick_size

def value_after_dot(a):
    b=int(a)
    c=a-b
    c=float(round(c,8)) # отсеим излишнюю точность
    if c==0:
        final=0
        return final
    else:
        d=str(c)
        final=len(d)-2
        return final

def get_open_position(dataposition,symbol):    
    for s in range(len(dataposition)):
        if dataposition[s]['symbol'] == symbol:
            print(dataposition[s])
            filters = float(dataposition[s]['initialMargin'])
    return filters  
def get_positionAmt(dataposition,symbol):    
    for s in range(len(dataposition)):
        if dataposition[s]['symbol'] == symbol:
            print(dataposition[s])
            filters = float(dataposition[s]['positionAmt'])
    return filters  
def get_maxNotional(dataposition,symbol):    
    for s in range(len(dataposition)):
        if dataposition[s]['symbol'] == symbol:
            print(dataposition[s])
            filters = float(dataposition[s]['maxNotional'])
    return filters  

client=Client(api_key=api_keys, api_secret=api_secret,testnet=False)





app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
@app.route("/test")
def hello_worldtest():
    return "<p>Hello, World!</p>"

@app.route("/webhook",methods=['POST'])
def webhook():
    dataposition=client.futures_account()['positions']
    data=json.loads(request.data)
    
    
    symbol=data['symbol']
    price=get_price(symbol)
    usdt=float(data['usdt'])
    coin=20*usdt/price
    quantity = float(round(coin,8))
    #print(quantity)
    a=get_info_minsizecoin(symbol)
    b=value_after_dot(a)
    quantity=float(round(quantity,b))
    #print(quantity)
    maxcoin=abs(get_positionAmt(dataposition,symbol))
    
    
   
    

  
        
    
    


    if data['signal']=="CloseShortOpenLong":
        
        stopShort=client.futures_create_order(symbol=symbol,side='BUY',type='MARKET' ,quantity=maxcoin, reduceOnly='true')
        buyorder=client.futures_create_order(symbol=symbol,side='BUY',type='MARKET',quantity=quantity)
        print("long")
        print(quantity)
    if data['signal']=="CloseLongOpenShort":
        stopLong=client.futures_create_order(symbol=symbol,side='SELL',type='MARKET' ,quantity=maxcoin, reduceOnly='true')
        buyorder=client.futures_create_order(symbol=symbol,side='SELL',type='MARKET',quantity=quantity)
        print("short")
        print(quantity)

    if data['signal']=="CloseShort":
        print(maxcoin)
        stopShort=client.futures_create_order(symbol=symbol,side='BUY',type='MARKET' ,quantity=maxcoin, reduceOnly='true')
        print("long")
        print(quantity)
    if data['signal']=="CloseLong":
        print(maxcoin)
        stopLong=client.futures_create_order(symbol=symbol,side='SELL',type='MARKET' ,quantity=maxcoin, reduceOnly='true')
        print("short")
        print(quantity)

    if data['signal']=="OpenLong":
        a=get_open_position(dataposition,symbol)
        if a==0:
            url='https://www.binance.com/futures/data/takerlongshortRatio?symbol='+symbol+'&period=5m&limit=10'
            a2=[]
#url='https://www.binance.com/futures/data/takerlongshortRatio?symbol=EOSUSDT&period=5m&limit=10'
            data2=requests.get(url).json()
            for s in range(10):
                a2.append(round(float(data2[s]['buyVol']),0))
                b3=round(float(data2[s]['buyVol']),0)
            a3 = mean(a2)
            c=b3/a3
            mess="trylong",symbol
            bot.sendMessage(chat_id=chat_id, text=mess)
            if c>1.5:
                mess="long",symbol
                bot.sendMessage(chat_id=chat_id, text=mess)
                price20=1.2*(get_price(symbol))
                quantity20=int(quantity*0.2)
                buyorder=client.futures_create_order(symbol=symbol,side='BUY',type='MARKET',quantity=quantity)
            #takeprofit=client.futures_create_order(symbol=symbol,side='SELL',type='LIMIT', timeInForce='GTC',price=price20 ,quantity=100000)
        #print("long")
        #print(quantity)
    if data['signal']=="OpenShort":
        a=get_open_position(dataposition,symbol)
        if a==0:
            url2='https://www.binance.com/futures/data/takerlongshortRatio?symbol='+symbol+'&period=5m&limit=10'
            a2=[]
#url='https://www.binance.com/futures/data/takerlongshortRatio?symbol=EOSUSDT&period=5m&limit=10'
            data2=requests.get(url2).json()
            for s in range(10):
                a2.append(round(float(data2[s]['sellVol']),0))
                b3=round(float(data2[s]['sellVol']),0)
            a3 = mean(a2)
            c=b3/a3
            mess="tryshort",symbol
            bot.sendMessage(chat_id=chat_id, text=mess)
            if c>1.5:
                mess="short",symbol
                bot.sendMessage(chat_id=chat_id, text=mess)
                buyorder=client.futures_create_order(symbol=symbol,side='SELL',type='MARKET',quantity=quantity)
        #print("short")
        #print(quantity)


    return{"signal":"success"}


if __name__ == 'main':
    app.run()


    
#python -m flask  
#set FLASK_APP=app.py
#$env:FLASK_ENV = "development"  для включения дебаг мод
#flask run

#     https://trxbogdan.herokuapp.com/webhook
#     {"usdt":"5","signal":"short"}
#$env:FLASK_APP = "app"
#$env:FLASK_ENV = "development"
#flask run
#http://localhost:5000/webhook
#https://trxbogdan.herokuapp.com/webhook