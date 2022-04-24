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
