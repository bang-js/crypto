import pyupbit
import numpy as np
import pandas as pd
import datetime
from calendar import monthrange  #매달 말일을 알려주는 함수
import time

### 로그인
access = ""
secret = ""
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=1)
    start_time = df.index[0]
    return start_time


def past(ticker) :
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=6) # 최근 6개 데이터
    change = 0
    for k in range(2,12):
        change += (df.iloc[-k]['close']-df.iloc[-k]['open'])/df.iloc[-k]['open'] # 이전 10분부터 100분까지의 총변화율
    return change



TICKERS = ['KRW-XRP', 'KRW-ETC', 'KRW-ETH' ,'KRW-NEO', 'KRW-MTL',    'KRW-LTC','KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM' \
        , 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR',     'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-REP', 'KRW-ADA'\
            ,'KRW-SBD', 'KRW-POWR', 'KRW-BTG','KRW-ICX', 'KRW-EOS',      'KRW-TRX', 'KRW-SC', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLY', \
                'KRW-ZRX', 'KRW-LOOM', 'KRW-BCH', 'KRW-BAT', 'KRW-IOST',     'KRW-RFR', 'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'KRW-MFT'\
                     ,'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 'KRW-ELF', 'KRW-KNC',     'KRW-BSV', 'KRW-THETA', 'KRW-QKC', 'KRW-BTT', 'KRW-MOC',\
                          'KRW-ENJ', 'KRW-TFUEL', 'KRW-MANA','KRW-ANKR', 'KRW-AERGO',   'KRW-ATOM', 'KRW-TT',  'KRW-MBL', 'KRW-WAXP',\
                               'KRW-HBAR', 'KRW-MED','KRW-MLK', 'KRW-STPT', 'KRW-ORBS',      'KRW-VET', 'KRW-CHZ', 'KRW-STMX', 'KRW-DKA', 'KRW-HIVE'\
                                   , 'KRW-KAVA', 'KRW-AHT', 'KRW-LINK', 'KRW-XTZ', 'KRW-BORA',       'KRW-JST' , 'KRW-CRO', 'KRW-TON', 'KRW-SXP', 'KRW-HUNT', \
                                        'KRW-PLA', 'KRW-DOT', 'KRW-SRM', 'KRW-MVL', 'KRW-STRAX',       'KRW-AQT', 'KRW-GLM', 'KRW-SSX', 'KRW-META', 'KRW-FCT2', \
                                            'KRW-CBK', 'KRW-SAND', 'KRW-HUM', 'KRW-DOGE', 'KRW-STRK',     'KRW-PUNDIX', 'KRW-FLOW',  'KRW-DAWN', 'KRW-AXS', 'KRW-STX' \
                                                 , 'KRW-XEC', 'KRW-SOL', 'KRW-MATIC', 'KRW-NU', 'KRW-CRE',       'KRW-1INCH', 'KRW-AAVE', 'KRW-ALGO']



# 자동매매 시작
start =0 # 매수 성공 시 start=1로 루프문(모니터링) 시작
while True:
    try:
        now = datetime.datetime.now()
        if start == 0 :
            start_time = get_start_time("KRW-BTC")                  # start time은 30분마다 갱신    
        elif start == 1:
            start_time = buy_time

        # 보유 원화
        krw = int(upbit.get_balance("KRW")) 
        print(start_time,now, start)
        
        # 매수 진행 : 시작시간-1초~시작시간+10분-10초
        if start ==0 and start_time < now < start_time + datetime.timedelta(minutes=10) - datetime.timedelta(seconds=30) :
            for ticker in TICKERS : 
                # 주어진 ticker의 현재호가 조회
                current_price = pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
                
                # 조건을 충족하는 ticker에 대해 전액(krw) 매수
                change = past(ticker)  
                if  change < -0.1  :                           # 총변화율 -0.075 이하면 매수
                    upbit.buy_market_order(ticker, krw/3.01)   # 수수료 고려해서 1.01로 나눠줌 # 연습용 21.01
                    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=1)
                    buy_time = df.index[0]
                    print(ticker, "매수", current_price, change)
                    buy_price = current_price                   # 현재가를 매수가에 저장
                    start = 1 
                    ticker = ticker                                  # 1 : 현재 매수 상태 / 0 : 현재 비매수 상태 
                    print(upbit.get_balances(),"\n",start, now)
                    break                                       # ticker for문 탈출

                # ticker 1회 돌리면 .1초 휴식
                time.sleep(0.1)
        #### 이익매, 손절매 #####
        elif start == 1 and start_time < now < start_time + datetime.timedelta(minutes=30) - datetime.timedelta(seconds=30) :
            while start_time < now < start_time + datetime.timedelta(minutes=30) - datetime.timedelta(seconds=30) :

                now = datetime.datetime.now()
                current_price = pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
                bal = float(upbit.get_balance(ticker=ticker))       # ticker는 buy에서 저장

                # 7.5% 넘어가면 전량 매도
                if buy_price * 1.1 < current_price :
                    upbit.sell_market_order(ticker, bal)
                    print(ticker, "10% 이익매도", current_price)
                    start = 0
                    break
                
                # -3% 떨어지면 전량 매도 (손절)
                elif buy_price * 0.97 > current_price :
                    upbit.sell_market_order(ticker, bal)
                    print(ticker, "-3% 손절매도", current_price)
                    start = 0
                    break
                
                # while 1회 돌리면 1초 휴식
                time.sleep(1)

        # 30분 뒤 매도 진행
        elif start_time + datetime.timedelta(minutes=30) - datetime.timedelta(seconds=30) < now < start_time + datetime.timedelta(minutes=30) - datetime.timedelta(seconds=1) and start == 1 :
            bal = float(upbit.get_balance(ticker=ticker))
            upbit.sell_market_order(ticker, bal)
            current_price = pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
            print(ticker, "매도", current_price)
            print(krw)
            start =0

        # print(ticker, current_price, krw)
        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)
