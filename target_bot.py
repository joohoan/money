#!/usr/bin/env python
# coding: utf-8

import telegram

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
        nowDatetime = now.strftime('%M')
        if nowDatetime == '1' :
            target_price = get_target_price("KRW-BTC", 0.5)
            bot.sendMessage(chat_id=chat_id, text=target_price)
    except Exception as e:
        time.sleep(1)



