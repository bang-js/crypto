# ##########
# # STUDY 1 : MDD
# ##########
# # 이를 spread(credit, rate) 및 이자율(or인상발표시기) 추이와 비교

import pandas as pd

# ETF 선택
etf_ticker = 'IXIC'

# csv 파일 불러오기
df = pd.read_csv('C:/etf/{}.csv'.format(etf_ticker))

# 1:Open, 2:H, 3:L, 4:Close

date = []
dd_list = []

for idx in range(1, df.shape[0]) :
    m = max(df.iloc[0:idx+1, 4])
    dd = df.iloc[idx][4]/m - 1
    dd_list.append(dd)
    date.append(df.iloc[idx][0])

ROR = pd.DataFrame([ x for x in zip(date, dd_list)])
ROR.rename(columns={0:'date', 1:'drawdown'}, inplace=True)

filename = '{}_mkt_study_MDD.csv'.format(etf_ticker)
file = open(filename, "w", encoding="utf-8-sig")  
ROR.to_csv('C:/etf/'+filename, index=None)


##########
# STUDY 2 : MDD return
##########
# MDD -x% 달성 후 추가 하락으로 -(x+h)%에 도달할 확률

import pandas as pd

threshold = [-0.1, -0.15, -0.2, -0.25, -0.3, -0.35, -0.4] # 달성 시 매수; -0.2 등
buffer = [-0.05, -0.1] # threshold에서 추가 달성 시 매도; -0.1 등

# ETF 선택
etf_ticker = 'IXIC'

# csv 파일 불러오기
df = pd.read_csv('C:/etf/{}.csv'.format(etf_ticker))
# 1:Open, 2:H, 3:L, 4:Close

# MDD df 생성
date = []
dd_list = []

for idx in range(1, df.shape[0]) :
    m = max(df.iloc[0:idx+1, 4])
    dd = df.iloc[idx][4]/m - 1
    dd_list.append(dd)
    date.append(df.iloc[idx][0])

MDD = pd.DataFrame([ x for x in zip(date, dd_list)])
MDD.rename(columns={0:'date', 1:'drawdown'}, inplace=True)

# Grid Search for Prob[a->0] and Prob[a->a+b] : 성공확률 측정

MDD_result = pd.DataFrame()
