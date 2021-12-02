
import pyupbit
import numpy as np
import pandas as pd
from datetime import datetime, time, date, timedelta  # timedelta : 기간 설정 가능 함수
from calendar import monthrange  #매달 말일을 알려주는 함수
from time import sleep

from backtest import TICKERS

df = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
now = datetime.now()
def get_upbit_day_ohlcv(now, ticker):
    df = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
    for i in range(2) :
        try:
            df_temp = pyupbit.get_ohlcv(ticker, interval='day', to=now)
            df = df.append(df_temp)
        except Exception as e:
            print('Exception:', e)
        
        now = now - timedelta(days=200)
    df.sort_index(axis=0, inplace=True)

    return df


def ma_ver1_ror(drop,hit) :  # 2 > 20
    BUY_PRICES =[]
    SELL_PRICES =[]
    BUY_TIMES=[]
    SELL_TIMES=[]
    # ma2
    df['ma2'] = df['close'].rolling(window=2).mean()
    # ma20
    df['ma20'] = df['close'].rolling(window=20).mean()
    j=0
    for idx in range(21,df.shape[0]-1):
        if j >= idx : # 매수 중에서는 추가 매수 없음
            continue
        #매수전략
        if df.iloc[idx-1][7] > df.iloc[idx-1][8]  : #MA2 > MA20인 상태면 매수
            buy_price = df.iat[idx,1]                   # 1: 시가
            BUY_PRICES.append(df.iat[idx,1])
            buy_time = df.iat[idx,0]                    # 0 : 시간
            BUY_TIMES.append(buy_time)

            for j in range(idx, df.shape[0]-1) :
                #매도전략1: -10%
                if buy_price*drop > df.iloc[j][3] :  # 3:저점low
                    sell_price = buy_price*drop       
                    SELL_PRICES.append(sell_price)
                    sell_time = df.iat[j,0]
                    SELL_TIMES.append(sell_time)
                    break
                #매도전략2: 20% (매도전략1과 중복시 매도전략1이 우위)
                elif buy_price*hit <= df.iloc[j][2] and not(buy_price*drop > df.iloc[j][3])  : # 2: high
                    sell_price = buy_price*hit       
                    SELL_PRICES.append(sell_price)
                    sell_time = df.iat[j,0]
                    SELL_TIMES.append(sell_time)
                    break
                #매도전략3: MA2>MA20 -> MA20>MA2 역전
                elif df.iloc[j][7] < df.iloc[j][8] and df.iloc[j-1][7] > df.iloc[j-1][8] : 
                    sell_price = df.iat[j+1,1]
                    SELL_PRICES.append(sell_price)
                    sell_time = df.iat[j+1,0]
                    SELL_TIMES.append(sell_time)
                    break
    ROR = pd.DataFrame([ x for x in zip(BUY_TIMES,BUY_PRICES,SELL_TIMES,SELL_PRICES)])
    ROR.rename(columns={0:'buy_time', 1:'buy_price',2:'sell_time',3:'sell_price'}, inplace=True)
    ROR['ror'] = ROR['sell_price']/ROR['buy_price']
    ROR['cumror'] = ROR['ror'].cumprod()
    
    return ROR


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
                                                 , 'KRW-XEC', 'KRW-SOL', 'KRW-MATIC', 'KRW-NU',       'KRW-1INCH']
#  'KRW-AAVE', ,  'KRW-ALGO'


for my_ticker in TICKERS :
    df = pd.DataFrame(columns=range(6)) # 빈 dataframe 생성 like []
    df.rename(columns={0:'open', 1:'high',2:'low',3:'close',4:'volume',5:'value'}, inplace=True)
    df = get_upbit_day_ohlcv(now, ticker=my_ticker) 
    df.reset_index(inplace=True)        # index 재생성, 이름이 부여된 index는 새로운 col이 됨
    df.drop_duplicates('index', inplace=True, ignore_index=True) # 중복 제거, index 새로
    df.columns=['date','open', 'high','low','close','volume','value']
    
    ROR = ma_ver1_ror(0.9,1.1)
    
    ROR['ticker'] = my_ticker
    print(df.tail(1))
    print(ROR.tail(1))

    fileName = '{}_{}_MA1_v2.csv'.format('400_Days', my_ticker)
    file = open(fileName, "w", encoding="utf-8-sig")  
    ROR.to_csv('C:/cryptoauto/'+fileName, index=None)
    sleep(0.2)

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
                                                 , 'KRW-XEC' , 'KRW-SOL', 'KRW-MATIC', 'KRW-NU',        'KRW-1INCH']
                                                #  'KRW-AAVE', 'KRW-ALGO',
# # 복수 코인 누적수익률 계산 : 중복 발생 시 어떻게 처리할 것인지가 관건


df = pd.DataFrame(columns=['buy_time','buy_price','sell_time','sell_price', 'ror','cumror','ticker'])
for my_ticker in TICKERS :
    fileName = '{}_{}_MA1_v2.csv'.format('400_Days', my_ticker)
    df_temp = pd.read_csv('C:/cryptoauto/'+fileName)
    df = df.append(df_temp, ignore_index=True)
# print(df.head())
df.sort_values(by=['buy_time'], inplace=True, ignore_index=True)
df['cumror'] = df['ror'].cumprod() 
print(df.shape)


# 중복 횟수 계산
OLS = []
for i in range(0, df.shape[0]) :
    ol = 0 
    if i < 150 :
        for j in range(0, i) :   
            if df.iloc[i][0] <= df.iloc[j][2] : 
                ol += 1
    else:
        for j in range(i-150, i) :   
            if df.iloc[i][0] <= df.iloc[j][2] : 
                ol += 1

    OLS.append(ol)
    if i%100 == 0 :
        print(i)

OLS = pd.Series(OLS)
print(OLS)
df['overlap'] = OLS
print(df.tail(10))
# 가중평균된 누적수익률 계산


file = open('Tot_400_Days_MA1_v2.csv', "w", encoding="utf-8-sig")  
df.to_csv('C:/cryptoauto/'+'Tot_400_Days_MA1_v2.csv', index=None)

# df = pd.DataFrame(columns=['buy_time','buy_price','sell_time','sell_price', 'ror','cumror','ticker','overlap'])
# # fileName = 'Tot_400_Days_MA1_v2.csv'
# # df = pd.read_csv('C:/cryptoauto/'+fileName)
# # print(df.head())
# for i in range(0,9) :
#     df_temp = df.iloc[i*200:i*200+200]
#     print(df_temp.head(1))
#     print(df_temp.tail(1))
#     CUM = []
#     K =[]
#     # for j in range(0, len(TICKERS)):
#     for j in range(0,30):
#         cumror = 1
#         k=0
#         for i in range(0, df_temp.shape[0]):
#             if df_temp.iloc[i][7] == j :
#                 cumror = cumror * df_temp.iloc[i][4] 
#                 k +=1
#         CUM.append(k*cumror)
#         K.append(k)
#     TOT_ror = sum(CUM) / sum(K)
#     # print(CUM, K)
#     print(TOT_ror)
#     file = open('Tot_400_Days_MA1.csv', "w", encoding="utf-8-sig")  
#     df.to_csv('C:/cryptoauto/'+'Tot_400_Days_MA2.csv', index=None)





