#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import pyupbit
import datetime

access = "mqE7HSDocW3t6WbxrCS8ybGeaOxHOL9Aw2PXJsKX"
secret = "lEL5u7uMedUNGSmrX1Txu8gfZ3876KrhiYSo8YkP"

def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

def get_average_price(ticker) :
    return upbit.get_avg_buy_price(ticker)

upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

while True:
    try:
        current_price = get_current_price("KRW-ADA")
        average_price = get_average_price("KRW-ADA")

        if current_price < average_price * 0.98:
            krw = get_balance("KRW")
            if krw > 5000:
                upbit.buy_market_order("KRW-ADA", krw*0.3)
                
        elif current_price > average_price * 1.02:
            btc = get_balance("ADA")
            upbit.sell_market_order("KRW-ADA",btc*0.3)
            
        elif current_price < average_price * 0.9:
            btc = get_balance("ADA")
            upbit.sell_market_order("KRW-ADA",btc*0.9995)
            
    except Exception as e:
        print(e)
        time.sleep(1)


# In[ ]:




