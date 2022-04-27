import pandas as pd
import numpy as np

# ETF 선택
etf_ticker = 'TQQQ_1981_2022'

# csv 파일 불러오기
df = pd.read_csv('C:/etf/{}.csv'.format(etf_ticker))

# 필요한 column 생성
df['MA60'] = df['close'].rolling(60).mean()
df['MA60'] = df['close'].rolling(60).mean()
df['MA5'] = df['close'].rolling(5).mean()
df['60>5'] = np.where(df['MA5']<df['MA60'],True,False)

# 매수가 계산
buy_price_tot = []
buy_time_tot = []
sell_price_tot = []
sell_time_tot = []
for i in range(60,df.shape[0]):
    if df.iloc[i]['60>5'] == False and df.iloc[i-1]['60>5'] == True : # MA5 > MA60 -> MA5 < MA60 역전
        buy_price_tot.append(df.iloc[i]['close'])
        buy_time_tot.append(df.iloc[i+1]['date'])
        for j in range(i+1,df.shape[0]-1):
            if df.iloc[j]['60>5']== True and df.iloc[j-1]['60>5']== False :
                sell_price_tot.append(df.iloc[j]['close'])
                sell_time_tot.append(df.iloc[j+1]['date'])
                break

# 매도가 계산

for i in range(60,df.shape[0]-1):
     # MA5 < MA60 -> MA5 > MA60 역전
        if df.iloc[i+1]['date'] < buy_time_tot[0] : 
            continue
        sell_price_tot.append(df.iloc[i]['close'])
        sell_time_tot.append(df.iloc[i+1]['date'])

# 데이터 결과 저장하기
ROR = pd.DataFrame([ x for x in zip(buy_time_tot,buy_price_tot,sell_time_tot,sell_price_tot)])
ROR.rename(columns={0:'buy_time', 1:'buy_price',2:'sell_time',3:'sell_price'}, inplace=True)
ROR['ror'] = ROR['sell_price']/ROR['buy_price']
ROR['cumror'] = ROR['ror'].cumprod()

print(ROR)
filename = '{}_simple.csv'.format(etf_ticker)
file = open(filename, "w", encoding="utf-8-sig")  
ROR.to_csv('C:/etf/'+filename, index=None)
