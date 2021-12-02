import pyupbit
import numpy as np
import pandas as pd
from datetime import datetime, time, date, timedelta  # timedelta : 기간 설정 가능 함수
from calendar import monthrange  #매달 말일을 알려주는 함수
from time import sleep




now = datetime.now() 
def get_upbit_ohlcv(now, ticker, year, month):
    df = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])

    # 해당 년월 1일부터
    from_date = date(year, month, 1)

    # 해당 년월 마지막 일(28일, 30일, 31일)
    end_day = monthrange(year, month)[1]
    to_date = date(year, month, end_day)
    
    # 해당 년월 마지막 일자가 현재 날짜보다 큰 경우
    if to_date >= now.date():
        to_date = now.date()
        end_day = to_date.day
    
    temp_list = []
    # 해당 년월 1일부터 말일(또는 현재 날짜)까지 데이터 수집 실시
    for day in range(1, end_day+1): 
        base_time = datetime(year,month,day)
        # print(base_time)
        
        try:
            df_temp = pyupbit.get_ohlcv(ticker, interval='minute5',count=144, to=base_time)
            # print(i, 'base_time:', base_time, 'shape:', df_temp.shape)
            df = pd.concat([df, df_temp], axis=0)
        except Exception as e:
            print('Exception:', e)
            
        from_date = from_date + timedelta(days=1)
        sleep(0.1)
        
    return df





def ma_ver1_ror(drop,hit) :  # 5 > 20
    BUY_PRICES =[]
    SELL_PRICES =[]
    BUY_TIMES=[]
    SELL_TIMES=[]
    # ma2
    df['ma2'] = df['close'].rolling(window=2).mean()
    # ma10
    df['ma10'] = df['close'].rolling(window=10).mean()
    # ma60
    df['ma60'] = df['close'].rolling(window=60).mean()
    n=0
    j=0
    for idx in range(21,df.shape[0]-1):
        if j >= idx : # 매수 중에서는 추가 매수 없음
            continue
        #매수전략
        # 
        # if df.iloc[idx-1][7] > df.iloc[idx-1][8] and not(df.iloc[idx-2][7] > df.iloc[idx-2][8]):
        if df.iloc[idx-1][4] < df.iloc[idx-2][4] and df.iloc[idx-2][4] < df.iloc[idx-3][4] and  df.iloc[idx-3][4] < df.iloc[idx-4][4] :
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
                    n+=1
                    break
                    
                #매도전략2: 20% (매도전략1과 중복시 매도전략1이 우위)
                elif buy_price*hit <= df.iloc[j][2] and not(buy_price*drop > df.iloc[j][3])  : # 2: high
                    sell_price = buy_price*hit       
                    SELL_PRICES.append(sell_price)
                    sell_time = df.iat[j,0]
                    SELL_TIMES.append(sell_time)
                    n+=1
                    break

                #매도전략3: MA2>MA20 -> MA20>MA2 역전
                elif df.iloc[j][7] < df.iloc[j][8] and df.iloc[j-1][7] > df.iloc[j-1][8] : 
                    sell_price = df.iat[j+1,1]
                    SELL_PRICES.append(sell_price)
                    sell_time = df.iat[j+1,0]
                    SELL_TIMES.append(sell_time)
                    n+=1
                    break
    
    if n!=0 :
        ROR = pd.DataFrame([ x for x in zip(BUY_TIMES,BUY_PRICES,SELL_TIMES,SELL_PRICES)])
        ROR.rename(columns={0:'buy_time', 1:'buy_price',2:'sell_time',3:'sell_price'}, inplace=True)
        ROR['ror'] = ROR['sell_price']/ROR['buy_price']-0.001
        ROR['cumror'] = ROR['ror'].cumprod()
        
        return ROR
    
    else :
        ROR = pd.DataFrame(columns=range(6))
        ROR = df.columns['BUY_TIMES','BUY_PRICES','SELL_TIMES','SELL_PRICES','ror','cumror']
        return ROR

TICKERS = ['KRW-XRP', 'KRW-ETC', 'KRW-ETH' ,'KRW-NEO', 'KRW-MTL',    'KRW-LTC','KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM'
        , 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR',     'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-REP', 'KRW-ADA'\
            ,'KRW-SBD', 'KRW-POWR', 'KRW-BTG','KRW-ICX', 'KRW-EOS',      'KRW-TRX', 'KRW-SC', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLY', \
                'KRW-ZRX', 'KRW-LOOM', 'KRW-BCH', 'KRW-BAT', 'KRW-IOST',     'KRW-RFR', 'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'KRW-MFT']

# TICKERS = ['KRW-XRP', 'KRW-ETC', 'KRW-ETH' ,'KRW-NEO', 'KRW-MTL',    'KRW-LTC','KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM' \
#         , 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR',     'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-REP', 'KRW-ADA'\
#             ,'KRW-SBD', 'KRW-POWR', 'KRW-BTG','KRW-ICX', 'KRW-EOS',      'KRW-TRX', 'KRW-SC', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLY', \
#                 'KRW-ZRX', 'KRW-LOOM', 'KRW-BCH', 'KRW-BAT', 'KRW-IOST',     'KRW-RFR', 'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'KRW-MFT'\
#                      ,'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 'KRW-ELF', 'KRW-KNC',     'KRW-BSV', 'KRW-THETA', 'KRW-QKC', 'KRW-BTT', 'KRW-MOC',\
#                           'KRW-ENJ', 'KRW-TFUEL', 'KRW-MANA','KRW-ANKR', 'KRW-AERGO',   'KRW-ATOM', 'KRW-TT', 'KRW-CRE', 'KRW-MBL', 'KRW-WAXP',\
#                                'KRW-HBAR', 'KRW-MED','KRW-MLK', 'KRW-STPT', 'KRW-ORBS',      'KRW-VET', 'KRW-CHZ', 'KRW-STMX', 'KRW-DKA', 'KRW-HIVE'\
#                                    , 'KRW-KAVA', 'KRW-AHT', 'KRW-LINK', 'KRW-XTZ', 'KRW-BORA',       'KRW-JST' , 'KRW-CRO', 'KRW-TON', 'KRW-SXP', 'KRW-HUNT', \
#                                         'KRW-PLA', 'KRW-DOT', 'KRW-SRM', 'KRW-MVL', 'KRW-STRAX',       'KRW-AQT', 'KRW-GLM', 'KRW-SSX', 'KRW-META', 'KRW-FCT2', \
#                                             'KRW-CBK', 'KRW-SAND', 'KRW-HUM', 'KRW-DOGE', 'KRW-STRK',     'KRW-PUNDIX', 'KRW-FLOW',  'KRW-DAWN', 'KRW-AXS', 'KRW-STX' \
#                                                  , 'KRW-XEC', 'KRW-SOL', 'KRW-MATIC', 'KRW-NU',       'KRW-1INCH']
#  'KRW-AAVE', ,  'KRW-ALGO'

for my_ticker in TICKERS :
    df = pd.DataFrame(columns=range(6)) # 빈 dataframe 생성 like []
    df.rename(columns={0:'open', 1:'high',2:'low',3:'close',4:'volume',5:'value'}, inplace=True)
    # for year in range(2020,2022) :
    #     if year !=2021 :
    #         for month in range(1,13) :
    #     else :
    #         for month in range(1,12) :
    year = 2021
    month = 11
    df = get_upbit_ohlcv(now, ticker=my_ticker,year=year,month=month) 
    df.reset_index(inplace=True)        # index 재생성, 이름이 부여된 index는 새로운 col이 됨
    df.drop_duplicates('index', inplace=True, ignore_index=True) # 중복 제거, index 새로
    df.columns=['date','open', 'high','low','close','volume','value']
    
    ROR = ma_ver1_ror(0.99,1.05)
    
    ROR['ticker'] = my_ticker
    print(ROR.tail(1))

    fileName = '{}_{}_rebound.csv'.format('5min', my_ticker)
    file = open(fileName, "w", encoding="utf-8-sig")  
    ROR.to_csv('C:/cryptoauto/'+fileName, index=None)
    sleep(0.1)

df = pd.DataFrame(columns=['buy_time','buy_price','sell_time','sell_price', 'ror','cumror','ticker'])
for my_ticker in TICKERS :
    fileName = '{}_{}_rebound.csv'.format('5min', my_ticker)
    df_temp = pd.read_csv('C:/cryptoauto/'+fileName)
    df = df.append(df_temp, ignore_index=True)
# print(df.head())
df.sort_values(by=['buy_time'], inplace=True, ignore_index=True)
df['cumror'] = df['ror'].cumprod() 
file = open('Tot_5min_rebound.csv', "w", encoding="utf-8-sig")  
df.to_csv('C:/cryptoauto/'+'Tot_5min_rebound.csv', index=None)
