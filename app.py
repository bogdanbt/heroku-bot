import json
from flask import Flask, request
from binance.client import Client
api_keys='MJXjYzcIxaPjYELP5L6DLieRDhtcPkQndqqIy0aILO6b1pCIWcavtTf82RbAoNxx'
api_secret='aDBRznWCHBQCzbALB3B1biPuyfuR9PDO2v9W03pJ8E2psO4fLDkvcBlWxIdB2NZq'
def get_price(symbol):
    price = client.get_avg_price(symbol=symbol)['price']
    return float(price)

def get_coin(data):
    symbol=data['symbol']
    price=get_price(symbol)
    usdt=int(data['usdt'])
    coin=20*usdt/price

    if data['value']=="int":
        coin=int(coin)
    if data['value']=="float":
        coin=float(coin)
    return coin


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
    quantity=get_coin(data)


    
    

    
    


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
        buyorder=client.futures_create_order(symbol=symbol,side='BUY',type='MARKET',quantity=quantity)
        print("long")
        print(quantity)
    if data['signal']=="OpenShort":
        buyorder=client.futures_create_order(symbol=symbol,side='SELL',type='MARKET',quantity=quantity)
        print("short")
        print(quantity)


    return{"signal":"success"}






    
    
#export для линукса или мака set для винді
# terminal ==     $ export FLASK_APP=hello
#                   $ flask run
#terminal ==     export FLASK_APP=app.py

# for debug mode 
# set FLASK_ENV=development
#flask run

#     https://trxbogdan.herokuapp.com/webhook
#     {"usdt":"5","signal":"short"}