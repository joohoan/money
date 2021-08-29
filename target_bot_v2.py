#!/usr/bin/env python
# coding: utf-8

# In[1]:


import telegram
import requests
from bs4 import BeautifulSoup

bot = telegram.Bot(token='1992687161:AAHFBWJgmmPn6nyOQ5aYPxfbv1KqEvqIUv8')
chat_id = 696530999

import time
import pyupbit
import datetime

def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=1)
    start_time = df.index[0]
    return start_time

while True:
    try:
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%M:%S')
        url = "https://www.coingecko.com/ko/거래소/upbit"
        bs = BeautifulSoup(requests.get(url).text,'html.parser')
        interest = []
        ticker_temp = bs.find_all("a", attrs={"rel":"nofollow noopener", "class":"mr-1"})
        
        for i in range(1):
            interest.append('KRW-' + list(ticker_temp[i])[0][1:-5])
            coin=interest[0].lstrip('KRW-')
            coin_l=[coin]
        if nowDatetime == '01:01' :
            target_price = get_target_price(interest, 0.5)
            bot.sendMessage(chat_id=chat_id, text=target_price)
    except Exception as e:
        time.sleep(1)

