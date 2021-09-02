import pyupbit 

df = pyupbit.get_ohlcv("KRW-BTC", interval="day", count=2)
target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * 0.5


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


