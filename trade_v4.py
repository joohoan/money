import time
import pyupbit
import datetime
import requests
import upbit
from bs4 import BeautifulSoup


access = "mqE7HSDocW3t6WbxrCS8ybGeaOxHOL9Aw2PXJsKX"
secret = "lEL5u7uMedUNGSmrX1Txu8gfZ3876KrhiYSo8YkP"

def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
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

upbit = pyupbit.Upbit(access, secret)
print("autotrade start")


while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)

        url = "https://coinmarketcap.com/ko/exchanges/upbit/"
        bs = BeautifulSoup(requests.get(url).text,'html.parser')
        interest = []
        coin = []
        ticker_temp = bs.find_all("a", attrs={"rel":"noopener nofollow noreferrer", "class":"sc-130rhjl-0 kLuYhf cmc-link"})        
        ticker_temp1 = bs.find_all("a", attrs={"rel":"noopener nofollow noreferrer", "class":"sc-130rhjl-0 kLuYhf cmc-link"})        

        for i in range(20):
            interest.append('KRW-' + list(ticker_temp[i])[0][:-4])
            coin.append(list(ticker_temp[i])[0][:-4])
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            for i in range(20) :
                target_price = get_target_price(interest[i], 0.5)
                time.sleep(0.3)
                current_price = get_current_price(interest[i])
                time.sleep(0.3)
                if target_price < current_price:
                    krw = get_balance("KRW")
                    if krw > 5000:
                        upbit.buy_market_order(interest[i], krw*0.9995)
                elif target_price*0.97 > current_price :
                    btc = upbit.get_balance(interest[i])
                    upbit.sell_market_order(interest[i], btc*0.9995)
        else:
            for i in range(20):
                interest.append('KRW-' + list(ticker_temp[i])[0][:-4])
                coin.append(list(ticker_temp[i])[0][:-4])
                btc = upbit.get_balance(interest[i])
                if btc > 0.00008:
                    upbit.sell_market_order(interest[i], btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)