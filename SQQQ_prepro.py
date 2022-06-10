# return rate 계산 -> quantile 기준으로 labeling(0,1,2,3 등) 
# additional inde. var. : TQQQ 기준 MA5>MA60 / BB1.3U

import pandas as pd
import numpy as np

# ETF 선택
etf_ticker = 'SQQQ'

# csv 파일 불러오기
df = pd.read_csv('C:/etf/SQQQ/{}.csv'.format(etf_ticker))
df['MA20'] = df['close'].rolling(20).mean()
# date	open	high	low	close	BB23	BB23U	BB23L	BB13	BB13U	BB13L	MA5	MA60
df_tq = pd.read_csv('C:/etf/TQQQ_220607.csv')
df_tq['MA60'] = df_tq['close'].rolling(60).mean()
# df_tq['MA20'] = df_tq['close'].rolling(20).mean()
df_tq['MA5'] = df_tq['close'].rolling(5).mean()
df_tq['60>5'] = np.where(df_tq['MA5']<df_tq['MA60'],True,False)

# ['60>5']를 df에 합치기
df = pd.concat([df, df_tq['60>5']],axis=1)

# return rate 생성
df['ror_d'] = df['close']/df['close'].shift(1) - 1      # daily return

# quantile 계산
ror_d_ma =  df['ror_d'][df['60>5']==True]    # MA60 > MA5 일때의 ror_d
print(ror_d_ma, ror_d_ma.shape)

q_num = 5       # quantile 수
q_lst = [i/q_num for i in range(0, q_num)]
r_lst = [] # quantile 대응값 저장 리스트
for f in q_lst :
    r_lst.append(ror_d_ma.quantile(q=f, interpolation='linear'))
    print(ror_d_ma.quantile(q=f, interpolation='linear'))
# -0.2835450883173226(무쓸모) -0.040907263807365375 -0.015166845520977024 0.00688077892102359 0.03323721407755027
# 기준에 +6.6% 추가
r_lst.append(0.066)
# 이를 기준으로 quantile column 생성
cond = [
    (df['ror_d'] <= r_lst[1]), # 0~0.2분위
    (r_lst[1] < df['ror_d']) & (df['ror_d'] <= r_lst[2]), # 0.2~0.4
    (r_lst[2] < df['ror_d']) & (df['ror_d'] <= r_lst[3]), # 0.4~0.6
    (r_lst[3] < df['ror_d']) & (df['ror_d'] <= r_lst[4]),    # 0.6~0.8
    (r_lst[4] < df['ror_d']) & (df['ror_d'] <= 6.6),    # 0.8~ +6.6%
    (6.6 < df['ror_d'])    # +6.6% ~
]
choice = [0,1,2,3,4,5]
df['ror_q'] = np.select(cond, choice, default='Not Specified')
print(df['ror_q'].shape)

###
# 전처리
# day(-5) ... day(-1) 전날의(BB1.3U/MA20)-1 | day(0)=label
# 이때 (BB1.3U/MA20)-1 은 BB1.3 upper line과 MA20 사이의 이격률을 의미 -> 일종의 normalize
###

# 이격률 col 생성
df['dif_BB'] = df['BB13U']/df['MA20'] -1
print(df['dif_BB'].head(5))

day_5 = []
day_4 = []
day_3 = []
day_2 = []
day_1 = []
dif_BB = []
label = []
for i in range(60, df.shape[0]) :
    if df.iloc[i]['60>5'] == True :
        day_5.append(df.iloc[i-5]['ror_q'])
        day_4.append(df.iloc[i-4]['ror_q'])
        day_3.append(df.iloc[i-3]['ror_q'])
        day_2.append(df.iloc[i-2]['ror_q'])
        day_1.append(df.iloc[i-1]['ror_q'])
        dif_BB.append(df.iloc[i-1]['dif_BB'])
        label.append(df.iloc[i]['ror_q'])

print(day_5, day_4, day_3, day_2, day_1, dif_BB, label)

# # 데이터 결과 저장하기
PREPRO = pd.DataFrame([ x for x in zip(day_5, day_4, day_3, day_2, day_1, dif_BB, label)])
PREPRO.rename(columns={0:'day_5', 1:'day_4',2:'day_3',3:'day_2',4:'day_1',5:'dif_BB',6:'label'}, inplace=True)
filename = '{}_prepro.csv'.format(etf_ticker)
file = open(filename, "w", encoding="utf-8-sig")  
PREPRO.to_csv('C:/etf/SQQQ/'+filename, index=None)


