
import pyupbit
import numpy as np
import pandas as pd
from datetime import datetime, time, date, timedelta  # timedelta : 기간 설정 가능 함수
from calendar import monthrange  #매달 말일을 알려주는 함수
from time import sleep

access = ""
secret = ""
upbit = pyupbit.Upbit(access, secret)

# 보유 크립토 리스트 생성
Cryptos = upbit.get_balances()
Cryptolist = []
for i in range(len(Cryptos)):
    crypto = Cryptos[i].get('currency') 
    crypto = 'KRW-' + crypto
    Cryptolist.append(crypto)
print("보유 코인수(원화 제외) :", len(Cryptos)-1)

df = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
now = datetime.now()
def get_upbit_day_ohlcv(now, ticker):
    df = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
    try:
        df = pyupbit.get_ohlcv(ticker, interval='day',count=22, to=now)    #9시기준
        # ma5
    except Exception as e:
        print('Exception:', e)
    return df

#매수 (MA2: 7)
def ma_ver1_day_buy2(my_ticker) :  
    if df.iloc[-2][7] > df.iloc[-2][8]  and \
    not(df.iloc[-3][7] > df.iloc[-3][8]) : 
        print("buy(MA2):", my_ticker)
        # print(df.iloc[-2])
        print("손절:", df.iloc[-1][4]*0.9)

#매수 (MA5: 9)
def ma_ver1_day_buy5(my_ticker) :  
    if df.iloc[-2][9] > df.iloc[-2][8]  and \
    not(df.iloc[-3][9] > df.iloc[-3][8]) : 
        print("buy(MA5):", my_ticker)
        # print(df.iloc[-2])
        print("손절:", df.iloc[-1][4]*0.9)

#(MA5 > MA20 인 상태)
def ma_ver1_day_state(my_ticker) :  
    if df.iloc[-2][7] > df.iloc[-2][8]  :
        print("\tMA5>MA20:", my_ticker)
        # print(df.iloc[-2])

#매도 (MA2: 7)
def ma_ver1_day_sell2(my_ticker) :  
    if not(df.iloc[-2][7] > df.iloc[-2][8] )  and \
    df.iloc[-3][7] > df.iloc[-3][8]  : 
        print("\t\t sell:",my_ticker)
        # print(df.iloc[-2])

def ma_ver1_day_sell_state(my_ticker) :  
    if df.iloc[-2][7] < df.iloc[-2][8]  : 
        print("\t\t sell state:",my_ticker)
        # print(df.iloc[-2])

def ma_ver1_day_hotday(hit) :
    if df.iloc[-1][1]*hit < df.iloc[-1][2]  :  # 오늘 기준 시가 대비 고점이 30% 넘은 경우
        print("\t\t\t\t",my_ticker,": today is hot")
    if df.iloc[-2][1]*hit < df.iloc[-2][3]  : # 어제 기준 시가 대비 종가가 30% 넘은 경우
        print("\t\t\t\t",my_ticker,": yesterday is hot")

# #매도 (MA5: 9)
# def ma_ver1_day_sell5(my_ticker) :  
#     if not(df.iloc[-2][9] > df.iloc[-2][8] )  and \
#     df.iloc[-3][9] > df.iloc[-3][8]  : 
#         print("\t\t sell:",my_ticker)
#         # print(df.iloc[-2])

# -1 -> -2, -2 -> -3 으로 바꿔야
# def ma_ver1_day_danger(my_ticker) :
#     # 전전날 상승캔들의 시가가 MA5 위에 있다가 전날 low가 MA5을 뚫어버린 경우 매도 주시 알람
#     if df.iloc[-2][4] > df.iloc[-2][1] and df.iloc[-2][1] > df.iloc[-2][7] and \
#         df.iloc[-1][3] < df.iloc[-1][7] :
#         print("\t\t\t danger(급등후급락):",  my_ticker)
#         print(df.iloc[-1])
#     # 하루만에 -10% 이상 하락 시  : 고점대비가 중요한데 일단 데이터 확보를 위해 추가
#     if (df.iloc[-1][4] - df.iloc[-1][1] ) / df.iloc[-1][1] < -0.1 :
#         print("\t\t\t danger(10%급락):",  my_ticker)
#         print(df.iloc[-1])
#     # 저점이 ma20을 뚫어버린 경우
#     if df.iloc[-1][3] < df.iloc[-1][8] :
#         print("\t\t\t\t\t\t\t danger(ma20돌파):",  my_ticker)
#         print(df.iloc[-1])
# 0 date / 1 open / 2 high / 3 low / 4 close / 7 ma5 / 8 ma20

# def ma_ver1_day_drop(my_ticker) :
#     for i in range(len(Cryptolist)):
#         if my_ticker == Cryptolist[i] :
#             if df.iloc[-1][4] < float(Cryptos[i].get('avg_buy_price'))*0.9 : 
#                 print("\t\t -10drop:",my_ticker)
#                 # print(df.iloc[-1])

TICKERS = ['KRW-XRP', 'KRW-ETC', 'KRW-ETH' ,'KRW-NEO', 'KRW-MTL',    'KRW-LTC','KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM' \
        , 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR',     'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-REP', 'KRW-ADA'\
            ,'KRW-SBD', 'KRW-POWR', 'KRW-BTG','KRW-ICX', 'KRW-EOS',      'KRW-TRX', 'KRW-SC', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLY', \
                'KRW-ZRX', 'KRW-LOOM', 'KRW-BCH', 'KRW-BAT', 'KRW-IOST',     'KRW-RFR', 'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'KRW-MFT',\
                     'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 'KRW-ELF', 'KRW-KNC',     'KRW-BSV', 'KRW-THETA', 'KRW-QKC', 'KRW-BTT', 'KRW-MOC',\
                          'KRW-ENJ', 'KRW-TFUEL', 'KRW-MANA','KRW-ANKR', 'KRW-AERGO',   'KRW-ATOM', 'KRW-TT', 'KRW-CRE', 'KRW-MBL', 'KRW-WAXP',\
                               'KRW-HBAR', 'KRW-MED','KRW-MLK', 'KRW-STPT', 'KRW-ORBS',      'KRW-VET', 'KRW-CHZ', 'KRW-STMX', 'KRW-DKA', 'KRW-HIVE'\
                                   , 'KRW-KAVA', 'KRW-AHT', 'KRW-LINK', 'KRW-XTZ', 'KRW-BORA',       'KRW-JST' , 'KRW-CRO', 'KRW-TON', 'KRW-SXP', 'KRW-HUNT', \
                                        'KRW-PLA', 'KRW-DOT', 'KRW-SRM', 'KRW-MVL', 'KRW-STRAX',       'KRW-AQT', 'KRW-GLM', 'KRW-SSX', 'KRW-META', 'KRW-FCT2', \
                                            'KRW-CBK', 'KRW-SAND', 'KRW-HUM', 'KRW-DOGE', 'KRW-STRK',     'KRW-PUNDIX', 'KRW-FLOW',  'KRW-DAWN', 'KRW-AXS', 'KRW-STX' \
                                                 , 'KRW-XEC', 'KRW-SOL', 'KRW-MATIC', 'KRW-NU', 'KRW-AAVE',       'KRW-1INCH',  'KRW-ALGO']


i=0
for my_ticker in TICKERS :
    df = pd.DataFrame(columns=range(6)) # 빈 dataframe 생성 like []
    df.rename(columns={0:'open', 1:'high',2:'low',3:'close',4:'volume',5:'value'}, inplace=True)
    df = get_upbit_day_ohlcv(now, ticker=my_ticker) 
    df.reset_index(inplace=True)        # index 재생성, 이름이 부여된 index는 새로운 col이 됨
    df.drop_duplicates('index', inplace=True, ignore_index=True) # 중복 제거, index 새로
    df.columns=['date','open', 'high','low','close','volume','value']
    
    # ma2
    df['ma2'] = df['close'].rolling(window=2).mean()
    # ma20
    df['ma20'] = df['close'].rolling(window=20).mean()
    # ma5
    df['ma5'] = df['close'].rolling(window=5).mean()

    # print(i)
    # print(df.tail(1))
    # print(df.shape)
    ma_ver1_day_buy2(my_ticker)
    ma_ver1_day_buy5(my_ticker)
    ma_ver1_day_hotday(1.3)
    if my_ticker in Cryptolist : 
        ma_ver1_day_sell2(my_ticker)
        # ma_ver1_day_sell5(my_ticker)
        ma_ver1_day_sell_state(my_ticker)
    else : 
        ma_ver1_day_state(my_ticker)
    #     ma_ver1_day_danger(my_ticker)
    # ma_ver1_day_drop(my_ticker)

    # 보유 코인 수 조회
    # print(my_ticker,":", upbit.get_balance(ticker=my_ticker))
    
    i+=1
    sleep(0.1)




