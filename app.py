from http import server
import json
from flask import Flask, request
from binance.client import Client
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
            filters = float(dataposition[s]['initialMargin'])
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
    
    
   
    dataposition=client.futures_account()['positions']

  
        
    
    


    if data['signal']=="CloseShortOpenLong":
        
        stopShort=client.futures_create_order(symbol=symbol,side='BUY',type='MARKET' ,quantity=123456, reduceOnly='true')
        buyorder=client.futures_create_order(symbol=symbol,side='BUY',type='MARKET',quantity=quantity)
        print("long")
        print(quantity)
    if data['signal']=="CloseLongOpenShort":
        stopLong=client.futures_create_order(symbol=symbol,side='SELL',type='MARKET' ,quantity=123456, reduceOnly='true')
        buyorder=client.futures_create_order(symbol=symbol,side='SELL',type='MARKET',quantity=quantity)
        print("short")
        print(quantity)

    if data['signal']=="CloseShort":
        stopShort=client.futures_create_order(symbol=symbol,side='BUY',type='MARKET' ,quantity=123456, reduceOnly='true')
        print("long")
        print(quantity)
    if data['signal']=="CloseLong":
        stopLong=client.futures_create_order(symbol=symbol,side='SELL',type='MARKET' ,quantity=123456, reduceOnly='true')
        print("short")
        print(quantity)

    if data['signal']=="OpenLong":
        a=get_open_position(dataposition,symbol)
        if a==0:
            price20=1.2*(get_price(symbol))
            quantity20=int(quantity*0.2)
            buyorder=client.futures_create_order(symbol=symbol,side='BUY',type='MARKET',quantity=quantity)
            takeprofit=client.futures_create_order(symbol=symbol,side='SELL',type='LIMIT',price=price20 ,quantity=100000)
        print("long")
        print(quantity)
    if data['signal']=="OpenShort":
        a=get_open_position(dataposition,symbol)
        if a==0:
            buyorder=client.futures_create_order(symbol=symbol,side='SELL',type='MARKET',quantity=quantity)
        print("short")
        print(quantity)


    return{"signal":"success"}


if __name__ == 'main':
    server.run()

'''

try:        
    stopShort=client.futures_create_order(symbol=symbol,side='BUY',type='MARKET' ,quantity=123456, reduceOnly='true')
    print("nice")
except:
    print("bad")
buyorder=client.futures_create_order(symbol=symbol,side='BUY',type='MARKET',quantity=quantity)
print("nice")
       '''

    
    
#export для линукса или мака set для винді
# terminal ==     $ export FLASK_APP=hello
#                   $ flask run
#terminal ==     export FLASK_APP=app.py

# for debug mode 
# set FLASK_ENV=development
#flask run

#     https://trxbogdan.herokuapp.com/webhook
#     {"usdt":"5","signal":"short"}
#$env:FLASK_APP = "app"
 #$env:FLASK_ENV = "development"
 #flask run
 #http://localhost:5000/webhook
 #https://trxbogdan.herokuapp.com/webhook