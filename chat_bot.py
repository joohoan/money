import pyupbit 

def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=6)
    df.index.strftime('%H:%M')
    df.index=df.index.strftime('%H:%M')
    target_price = df.loc['21:00']['close']+(df.loc['21:00']['high']- df.loc['21:00']['low']) * k
    return target_price

def get_target_price_12(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=6)
    df.index.strftime('%H:%M')
    df.index=df.index.strftime('%H:%M')
    target_price = df.loc['09:00']['close']+(df.loc['09:00']['high']- df.loc['09:00']['low']) * k
    return target_price

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=43210): # now가 오전 09시 ~ 저녁 08:59:50 사이
            target_price = get_target_price_12("KRW-BTC", 0.5)
                    
        elif start_time + datetime.timedelta(seconds=43200) < now < endtime - datetime.timedelta(seconds=10) : # now가 저녁 9시 ~ 아침 08:59:50 사이
            target_price = get_target_price("KRW-BTC", 0.5)


tp = target_price.astype(int)
tp = format(tp,',d')

a = '타겟가격은 '
b = '원 입니다.'

tg=a+tp+b
tg

import telegram
import pyupbit 
from telegram.ext import Updater
from telegram.ext import CommandHandler


print(a+tp+b)

telegram_token = '1970363842:AAF8GOVw97fAMNjkf5BqvRkxg1Wbx0eUIds'
telegram_chat_id = 696530999

 
bot = telegram.Bot(token = telegram_token)
updater = Updater(token = telegram_token)
 
def send_message(update, context):
        bot.sendMessage(chat_id = telegram_chat_id, text = tg)
 
def add_handler(cmd, func):
        updater.dispatcher.add_handler(CommandHandler(cmd, func))
 
add_handler('send', send_message)
 
updater.start_polling()
updater.idle()


