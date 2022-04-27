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

for a in threshold : # 7종
    for b in buffer : # 2종
        # 이제 여기서 threshold는 a, buffer는 b
        date_list = []         
        mdd_check =[]
        num_thres = 0
        num_zero = 0
        num_drop = 0
        idx=0
        j=0
        while idx < MDD.shape[0] :
            if MDD.iloc[idx][1] < a and (j<idx or j == 0) :
                date_list.append(MDD.iloc[idx][0])
                mdd_check.append(MDD.iloc[idx][1])
                num_thres += 1

                for j in range(idx+1,MDD.shape[0]) :
                    if MDD.iloc[j][1] <= a+b : # a+b로 추락하는 횟수 (탈출)
                        date_list.append(MDD.iloc[j][0])
                        mdd_check.append(MDD.iloc[j][1])
                        num_drop += 1
                        for k in range(j,MDD.shape[0]) :  # j를 a 이상으로 올라가는 시점으로 변경 -> 시점 조절
                            if MDD.iloc[k][1] > a :
                                break
                        j = k 
                        break

                    elif MDD.iloc[j][1] >= -0.01 : # 0에 도달하는 횟수
                        date_list.append(MDD.iloc[j][0])
                        mdd_check.append(MDD.iloc[j][1])
                        num_zero += 1
                        break
                    
                    # else : # a 달성 후 0과 a+b 둘 다 없어서 끊기는 경우
                    #     date_list.append(MDD.iloc[MDD.shape[0]][0])
                    #     mdd_check.append(MDD.iloc[MDD.shape[0]][1])
                    #     num_thres -= 1 # thres 수 보정
                idx += 1
            else :
                idx += 1
        for p in ['thres','zero','drop', 'zero/thres', 'drop/thres'] : 
            date_list.append(p)
        for q in [num_drop+num_zero, num_zero, num_drop, num_zero/(num_drop+num_zero), num_drop/(num_drop+num_zero)] :
            mdd_check.append(q)

        MDD_temp = pd.DataFrame([ x for x in zip(date_list, mdd_check)])
        MDD_temp.rename(columns={0:'date', 1:'drawdown'}, inplace=True)
        MDD_result = pd.concat([MDD_result, MDD_temp], axis=1)
        print("num_thres",num_thres, "num_zero", num_zero, "num_drop", num_drop)
        # print(MDD_temp)

# print(MDD_result)

filename = '{}_mkt_study_MDD_return.csv'.format(etf_ticker)
file = open(filename, "w", encoding="utf-8-sig")  
MDD_result.to_csv('C:/etf/'+filename, index=None)
