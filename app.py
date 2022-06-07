import json
from flask import Flask, request
from binance.client import Client
api_keys='MJXjYzcIxaPjYELP5L6DLieRDhtcPkQndqqIy0aILO6b1pCIWcavtTf82RbAoNxx'
api_secret='aDBRznWCHBQCzbALB3B1biPuyfuR9PDO2v9W03pJ8E2psO4fLDkvcBlWxIdB2NZq'
def get_price(symbol):
    price = client.get_avg_price(symbol=symbol)['price']
    return float(price)

client=Client(api_key=api_keys, api_secret=api_secret,testnet=False)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/webhook",methods=['POST'])
def webhook():
    symbol='TRXUSDT'
    data=json.loads(request.data)
    price=get_price('TRXUSDT')
    usdt=int(data['usdt'])
    coin=20*usdt/price
    quantity=int(coin)
    if data['signal']=="long":
        stopShort=client.futures_create_order(symbol=symbol,side='BUY',type='MARKET' ,quantity=123456, reduceOnly='true')
        buyorder=client.futures_create_order(symbol=symbol,side='BUY',type='MARKET',quantity=quantity)
        print("long")
        print(quantity)
    if data['signal']=="short":
        stopLong=client.futures_create_order(symbol=symbol,side='SELL',type='MARKET' ,quantity=123456, reduceOnly='true')
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

#     https://trxbogdan.herokuapp.com/
#     {"usdt":"5","signal":"short"}