import time
import pyupbit
import datetime

### 로그인
access = ""
secret = ""
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

### 전체 보유 코인 및 잔고를 dict 형태로 반환
Cryptos = upbit.get_balances()
Cryptolist = []
Cryptolist_wo_krw = []
for i in range(len(Cryptos)):
    crypto = Cryptos[i].get('currency') 
    Cryptolist_wo_krw.append(crypto)
    crypto = 'KRW-' + crypto
    Cryptolist.append(crypto)
print(Cryptolist)

# 자동매매 시작
while True:
    try:
        for ticker in Cryptolist_wo_krw : # Cryptolist는 KRW가 붙은 얘, Cryptos[i].get('currency')는 KRW가 없는 얘 
            for i in range(len(Cryptos)) :
                if Cryptos[i].get('currency') == ticker :
                    buy_price = float(Cryptos[i].get('avg_buy_price'))
            if ticker != 'KRW' :
                ticker =  'KRW-' + ticker
            
                current_price = pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
                #fiftyhit(ticker)
                df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
                target_price = df.iloc[0]['open'] * 1.5
                if target_price < current_price :
                    bal = upbit.get_balance(ticker=ticker)
                    upbit.sell_market_order(ticker, bal)
                    print(ticker, "50%매도", current_price)

                # sonjeol(ticker, buy_price)
                target_price =  buy_price* 0.8
                if target_price > current_price :
                    bal = upbit.get_balance(ticker=ticker)
                    upbit.sell_market_order(ticker, bal)
                    print(ticker, "손절매도", current_price)
        time.sleep(10)

    except Exception as e:
        print(e)
        time.sleep(10)
