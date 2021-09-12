import time
import pyupbit
import datetime
from pyupbit.exchange_api import Upbit
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
print("자동매매를 시작합니다.")
interest=pyupbit.get_tickers(fiat="KRW")
print(len(interest))

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)
        url = "https://coinmarketcap.com/ko/exchanges/upbit/"
        bs = BeautifulSoup(requests.get(url).text,'html.parser')
        interest = []
        ticker_temp = bs.find_all("a", attrs={"rel":"noopener nofollow noreferrer", "class":"sc-130rhjl-0 kLuYhf cmc-link"})        

        for i in range(30):
            interest.append('KRW-' + list(ticker_temp[i])[0][:-4])
        print(interest)
        if start_time < now < end_time - datetime.timedelta(minutes=10):
            print("매수를 명령합니다.")
            for i in range(30) :
                target_price = get_target_price(interest[i], 0.5)
                current_price = get_current_price(interest[i])
                upper_price = target_price * 1.01
                lower_price = target_price * 0.98
                ikjul_price = target_price * 1.08
                print(interest[i])
                if target_price < current_price < upper_price:
                    print("조건에 맞는 종목이 있습니다. 매수합니다.")
                    krw = get_balance("KRW")
                    if krw > 5000:
                        upbit.buy_market_order(interest[i], krw*0.9995)
                elif current_price > ikjul_price : 
                    print("익절 합니다! 요시!")
                    btc = upbit.get_balance(interest[i])
                    if btc > 0.00008 : 
                        upbit.sell_market_order(interest[i], btc * 0.9995)
                elif target_price < lower_price :
                    print("손절 합니다.")
                    btc = upbit.get_balance(interest[i])
                    if btc > 0.00008 :
                        upbit.sell_market_order(interest[i], btc*0.9995)
                
            print("끝까지 검토했습니다")
        else:
            print("매도를 명령합니다.")
            for i in range(30) :
                btc = upbit.get_balance(interest[i])
                if btc > 0.00008:
                    upbit.sell_market_order(interest[i], btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)