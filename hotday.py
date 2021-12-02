import re
import pyupbit
import numpy as np
import pandas as pd
from datetime import datetime, time, date, timedelta  # timedelta : 기간 설정 가능 함수
from calendar import monthrange  #매달 말일을 알려주는 함수
from time import sleep

df = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
now = datetime.now()
def get_upbit_day_ohlcv(now, ticker):
    df = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
    for i in range(1) :
        try:
            df_temp = pyupbit.get_ohlcv(ticker, interval='day', to=now)
            df = df.append(df_temp)
        except Exception as e:
            print('Exception:', e)
        
        now = now - timedelta(days=200)
    df.sort_index(axis=0, inplace=True)

    return df

# # open 대비 high가 50%으로 튄 횟수
# def hotday(hit):
#     num =0
#     for i in range(0, df.shape[0]-1) :
#         if df.iloc[i][1] *hit < df.iloc[i][2] :
#             num +=1
#     return num

# def hotday_after(hit): # 시가 대비 ##종가##가 50% 상승
#     num =0
#     sum =0
#     for i in range(0, df.shape[0]-2) :
#         if df.iloc[i][1] *hit < df.iloc[i][4] :
#             sum += (df.iloc[i+1][4]-df.iloc[i+1][1])/df.iloc[i+1][1]
#             print("\t", (df.iloc[i+1][4]-df.iloc[i+1][1])/df.iloc[i+1][1])
#             num +=1
#     if num ==0:
#         return 0
#     elif num >0: 
#         return sum/num

# 모든 원소를 리스트로
def hotday_after(hit): # 시가 대비 ##종가##가 50% 상승
    num =0
    lst =[]
    for i in range(0, df.shape[0]-2) :
        if df.iloc[i][1] *hit < df.iloc[i][4] :
            lst.append((df.iloc[i+1][4]-df.iloc[i+1][1])/df.iloc[i+1][1]) 
            num +=1
    return lst, num


# def hotday_afterafter(hit): #이틀치 평균
#     num =0
#     sum =0
#     for i in range(0, df.shape[0]-2) :
#         if df.iloc[i][1] *hit < df.iloc[i][4] :
#             sum += (df.iloc[i+2][4]-df.iloc[i+1][1])/df.iloc[i+1][1]
#             num +=1
#     if num ==0:
#         return 0
#     elif num >0: 
#         return sum/num

def hotday_afterafter(hit): # 시가 대비 ##종가##가 50% 상승 : 0일 대비 +2일
    num =0
    lst2 =[]
    for i in range(0, df.shape[0]-2) :
        if df.iloc[i][1] *hit < df.iloc[i][4] :
            lst2.append((df.iloc[i+2][4]-df.iloc[i][1])/df.iloc[i][1]) 
            num +=1

    return lst2, num




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

# for my_ticker in TICKERS :
#     df = pd.DataFrame(columns=range(6)) # 빈 dataframe 생성 like []
#     df.rename(columns={0:'open', 1:'high',2:'low',3:'close',4:'volume',5:'value'}, inplace=True)
#     df = get_upbit_day_ohlcv(now, ticker=my_ticker) 
#     df.reset_index(inplace=True)        # index 재생성, 이름이 부여된 index는 새로운 col이 됨
#     df.drop_duplicates('index', inplace=True, ignore_index=True) # 중복 제거, index 새로
#     df.columns=['date','open', 'high','low','close','volume','value']
#     # print(df.tail(1))
#     # print(df.shape)
#     print(my_ticker,",", hotday_after(1.3),",",hotday_afterafter(1.3))
#     sleep(0.1)
lst=[]
lst2=[]
ROR_total = pd.DataFrame(columns=range(2))
for my_ticker in TICKERS :
    df = pd.DataFrame(columns=range(6)) # 빈 dataframe 생성 like []
    df.rename(columns={0:'open', 1:'high',2:'low',3:'close',4:'volume',5:'value'}, inplace=True)
    df = get_upbit_day_ohlcv(now, ticker=my_ticker) 
    df.reset_index(inplace=True)        # index 재생성, 이름이 부여된 index는 새로운 col이 됨
    df.drop_duplicates('index', inplace=True, ignore_index=True) # 중복 제거, index 새로
    df.columns=['date','open', 'high','low','close','volume','value']
    # print(df.tail(1))
    # print(df.shape)
    if hotday_after(1.3)[1] !=0 :
        lst = hotday_after(1.3)[0]
        lst2 = hotday_afterafter(1.3)[0]
        # print(my_ticker,",", hotday_after(1.3),",",hotday_afterafter(1.3))
        ROR = pd.DataFrame([ x for x in zip(lst, lst2)])
        ROR_total = ROR_total.append(ROR)
        print(ROR.head(1))
    sleep(0.1)
file = open("hotday.csv", "w", encoding="utf-8-sig")  
ROR_total.to_csv('C:/cryptoauto/hotday.csv', index=None)

