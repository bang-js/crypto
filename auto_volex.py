import pyupbit
import numpy as np
import pandas as pd
import datetime   # timedelta : 기간 설정 가능 함수
from calendar import monthrange  #매달 말일을 알려주는 함수
import time

### 로그인
access = ""
secret = ""
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=1)
    start_time = df.index[0]
    return start_time

TICKERS = ['KRW-XRP', 'KRW-ETC', 'KRW-ETH' ,'KRW-NEO', 'KRW-MTL',    'KRW-LTC','KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM' \
        , 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR',     'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-REP', 'KRW-ADA'\
            ,'KRW-SBD', 'KRW-POWR', 'KRW-BTG','KRW-ICX', 'KRW-EOS',      'KRW-TRX', 'KRW-SC', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLY', \
                'KRW-ZRX', 'KRW-LOOM', 'KRW-BCH', 'KRW-BAT', 'KRW-IOST',     'KRW-RFR', 'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'KRW-MFT'\
                     ,'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 'KRW-ELF', 'KRW-KNC',     'KRW-BSV', 'KRW-THETA', 'KRW-QKC', 'KRW-BTT', 'KRW-MOC',\
                          'KRW-ENJ', 'KRW-TFUEL', 'KRW-MANA','KRW-ANKR', 'KRW-AERGO',   'KRW-ATOM', 'KRW-TT', 'KRW-CRE', 'KRW-MBL', 'KRW-WAXP',\
                               'KRW-HBAR', 'KRW-MED','KRW-MLK', 'KRW-STPT', 'KRW-ORBS',      'KRW-VET', 'KRW-CHZ', 'KRW-STMX', 'KRW-DKA', 'KRW-HIVE'\
                                   , 'KRW-KAVA', 'KRW-AHT', 'KRW-LINK', 'KRW-XTZ', 'KRW-BORA',       'KRW-JST' , 'KRW-CRO', 'KRW-TON', 'KRW-SXP', 'KRW-HUNT', \
                                        'KRW-PLA', 'KRW-DOT', 'KRW-SRM', 'KRW-MVL', 'KRW-STRAX',       'KRW-AQT', 'KRW-GLM', 'KRW-SSX', 'KRW-META', 'KRW-FCT2', \
                                            'KRW-CBK', 'KRW-SAND', 'KRW-HUM', 'KRW-DOGE', 'KRW-STRK',     'KRW-PUNDIX', 'KRW-FLOW',  'KRW-DAWN', 'KRW-AXS', 'KRW-STX' \
                                                 , 'KRW-XEC', 'KRW-SOL', 'KRW-MATIC', 'KRW-NU',       'KRW-1INCH', 'KRW-AAVE', 'KRW-ALGO']



# 자동매매 시작
start =0 # 매수 성공 시 start=1로 루프문(모니터링) 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC") # end_time = start_time + datetime.timedelta(hours=1)
        end_time = start_time + datetime.timedelta(minutes=60)

        # 보유 원화
        krw = int(upbit.get_balance("KRW")) # print(start_time,now,end_time)
        
        # 매수 진행
        if start_time < now < end_time - datetime.timedelta(seconds=10):

            for ticker in TICKERS : 
                # 주어진 ticker의 현재호가 조회
                current_price = pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
                
                # 조건을 충족하는 ticker에 대해 전액(krw) 매수 (0.01, 1)
                df = pyupbit.get_ohlcv(ticker, interval="minute60", count=2)
                if  (df.iloc[-2]['high'] - df.iloc[-2]['low'])*1.1 >= (current_price - df.iloc[-1]['open']) >= (df.iloc[-2]['high'] - df.iloc[-2]['low']) \
                    and df.iloc[-2]['open'] < df.iloc[-2]['close'] \
                         and 0.01 < (df.iloc[-2]['high'] - df.iloc[-2]['low'])/df.iloc[-2]['low'] \
                             and (current_price > 2500 or 1000 > current_price >= 250 or 100 > current_price >= 25) :
                                upbit.buy_market_order(ticker, krw/1.01)
                                print(ticker, "매수", current_price)
                                print(upbit.get_balances())
                                buy_price = current_price
                                start = 1
                                break

                # ticker 1회 돌리면 1초 휴식
                time.sleep(1)

            #### 이익매, 손절매 #####
            while start == 1 and start_time < now < end_time - datetime.timedelta(seconds=11) :
                now = datetime.datetime.now()
                current_price = pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
                bal = float(upbit.get_balance(ticker=ticker))

                # 2.5% 넘어가면 전량 매도
                if buy_price * 1.025 < current_price :
                    upbit.sell_market_order(ticker, bal)
                    print(ticker, "2.5% 이익 매도", current_price)
                    start = 0
                    break
                
                # -2.5% 떨어지면 전량 매도 (손절)
                elif buy_price * 0.975 > current_price :
                    upbit.sell_market_order(ticker, bal)
                    print(ticker, "-2.5% 손절 매도", current_price)
                    start = 0
                    break
                
                # while 1회 돌리면 1초 휴식
                time.sleep(1)

            # 1시간 뒤 매도 진행
        elif end_time - datetime.timedelta(seconds=10) < now < end_time - datetime.timedelta(seconds=1) and start == 1 :
            print(ticker, now, end_time, start)
            bal = float(upbit.get_balance(ticker=ticker))
            current_price = pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
            upbit.sell_market_order(ticker, bal)
            print(ticker, "매도", current_price)
            print(krw)
            start =0

        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)
