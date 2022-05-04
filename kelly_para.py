
#######################
# Kelly parameterization
# a, b, p 찾기
#######################
import pandas as pd
import numpy as np
# ETF 선택
etf_ticker = 'SQQQ_2022'

# csv 파일 불러오기
df = pd.read_csv('C:/etf/{}.csv'.format(etf_ticker))

# 당일 시가(open, t)에 매수 후 다음날 시가(open, t+1)에 매도 : 깨어있는 시각이 시작시간이기 때문
# 시가 기준 변동률 계산
df['ror'] = df['open']/df['open'].shift(1) - 1

is_posi = df['ror'] > 0
n_posi = is_posi.value_counts().values[0] # True N
n_nega = is_posi.value_counts().values[1] # False M
print("승률 :", n_posi/(n_posi+n_nega))
