#!/usr/bin/env python
# coding: utf-8

# In[1]:


import telegram
import time
import pyupbit
import datetime

bot = telegram.Bot(token='1992687161:AAHFBWJgmmPn6nyOQ5aYPxfbv1KqEvqIUv8')
chat_id = 696530999


# In[3]:


def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price


# In[4]:


def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=1)
    start_time = df.index[0]
    return start_time


# In[5]:


while True:
    try:
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%M:%S')
        if nowDatetime == '01:00' :
            target_price = get_target_price("KRW-BCHA", 0.5)
            target_price=target_price.astype(int)
            tp = format(target_price,',d')
            a = '매수 기준가는'
            b = '원 입니다.'
            bot.sendMessage(chat_id=chat_id, text=a+tp+b)
    except Exception as e:
        time.sleep(1)


# In[ ]:




