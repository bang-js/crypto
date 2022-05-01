
# 필요한 column 생성
df['MA60'] = df['close'].rolling(60).mean()
df['MA5'] = df['close'].rolling(5).mean()
df['60>5'] = np.where(df['MA5']<df['MA60'],True,False)

buy_price_tot = []
buy_time_tot = []
sell_price_tot = []
sell_time_tot = []

# -1% 발생
c = 0
for i in range(60,df.shape[0]-11):
    if df.iloc[i]['ror'] < threshold and (c==0 or c<i) : 
        sell_price_tot.append(df.iloc[i]['close'])
        sell_time_tot.append(df.iloc[i]['date'])

        if df.iloc[i+10]['60>5'] == False :
            buy_price_tot.append(df.iloc[i+10]['close'])
            buy_time_tot.append(df.iloc[i+10]['date'])
            c = i+10

        else :
            for j in range(i+11,df.shape[0]-1):
                if df.iloc[j]['60>5']== False and df.iloc[j-1]['60>5']== True : 
                    buy_price_tot.append(df.iloc[j]['close'])
                    buy_time_tot.append(df.iloc[j]['date'])
                    c = j
                    break

sell_d = sell_time_tot[-1].replace("-","")
buy_d = buy_time_tot[-1].replace("-","")
if int(sell_d) < int(buy_d) : # sell을 기준으로 설계했기에 매수-매도가 역전된 상태, 이를 교정하는 과정
    for k in range(c+1,df.shape[0]): # 11일 전에서 끝냈기 때문에 추가로 탐색
        if df.iloc[k]['close'] < threshold : # 밑으로 내려가면서 1%risk 체크
            sell_price_tot.append(df.iloc[k]['close'])
            sell_time_tot.append(df.iloc[k]['date'])
            break
        else : # 없으면 마지막날 가격으로 매도
            sell_price_tot.append(df.iloc[-1]['close'])
            sell_time_tot.append(df.iloc[-1]['date'])
                 
# sell을 기준으로 설계했기에 처음 sell은 기준일 뿐 의미 없으므로 제거
del sell_time_tot[0]  
del sell_price_tot[0]

# 데이터 결과 저장하기
ROR = pd.DataFrame([ x for x in zip(buy_time_tot,buy_price_tot,sell_time_tot,sell_price_tot)])
ROR.rename(columns={0:'buy_time', 1:'buy_price',2:'sell_time',3:'sell_price'}, inplace=True)

ROR['ror'] = ROR['sell_price']/ROR['buy_price']
ROR['cumror'] = ROR['ror'].cumprod()

print(ROR)
filename = '{}_1per_{}_rule.csv'.format(etf_ticker, threshold)
file = open(filename, "w", encoding="utf-8-sig")  
ROR.to_csv('C:/etf/'+filename, index=None)

print(pow(ROR.iloc[-1][-1],1/(2022-1986+1)))

# 분석결과 simple보다 (1거래) MDD가 더 큰 반면 수익률에서 차이가 없음

#########################
# bakcktest : 1%와 simple 결합
#########################

df['MA60'] = df['close'].rolling(60).mean()
df['MA5'] = df['close'].rolling(5).mean()
df['60>5'] = np.where(df['MA5']<df['MA60'],True,False)

buy_price_tot = []
buy_time_tot = []
sell_price_tot = []
sell_time_tot = []

# -1% 발생
c = 0
for i in range(60,df.shape[0]-11):
    if (df.iloc[i]['ror'] < threshold and (c==0 or c<i)) or (df.iloc[i]['60>5']== True and df.iloc[i-1]['60>5']== False and (c==0 or c<i)) : 
        sell_price_tot.append(df.iloc[i]['close'])
        sell_time_tot.append(df.iloc[i]['date'])

        if (df.iloc[i]['ror'] < threshold and (c==0 or c<i)) and df.iloc[i+10]['60>5'] == False :
            buy_price_tot.append(df.iloc[i+10]['close'])
            buy_time_tot.append(df.iloc[i+10]['date'])
            c = i+10

        else :
            for j in range(i+11,df.shape[0]-1):
                if df.iloc[j]['60>5']== False and df.iloc[j-1]['60>5']== True : 
                    buy_price_tot.append(df.iloc[j]['close'])
                    buy_time_tot.append(df.iloc[j]['date'])
                    c = j
                    break

sell_d = sell_time_tot[-1].replace("-","")
buy_d = buy_time_tot[-1].replace("-","")
if int(sell_d) < int(buy_d) : # sell을 기준으로 설계했기에 매수-매도가 역전된 상태, 이를 교정하는 과정
    for k in range(c+1,df.shape[0]): # 11일 전에서 끝냈기 때문에 추가로 탐색
        if df.iloc[k]['close'] < threshold : # 밑으로 내려가면서 1%risk 체크
            sell_price_tot.append(df.iloc[k]['close'])
            sell_time_tot.append(df.iloc[k]['date'])
            break
        else : # 없으면 마지막날 가격으로 매도
            sell_price_tot.append(df.iloc[-1]['close'])
            sell_time_tot.append(df.iloc[-1]['date'])
                 
# sell을 기준으로 설계했기에 처음 sell은 기준일 뿐 의미 없으므로 제거
del sell_time_tot[0]  
del sell_price_tot[0]

# 데이터 결과 저장하기
ROR = pd.DataFrame([ x for x in zip(buy_time_tot,buy_price_tot,sell_time_tot,sell_price_tot)])
ROR.rename(columns={0:'buy_time', 1:'buy_price',2:'sell_time',3:'sell_price'}, inplace=True)

ROR['ror'] = ROR['sell_price']/ROR['buy_price']
ROR['cumror'] = ROR['ror'].cumprod()

print(ROR)
filename = '{}_mix_{}_1per_and_simple.csv'.format(etf_ticker, threshold)
file = open(filename, "w", encoding="utf-8-sig")  
ROR.to_csv('C:/etf/'+filename, index=None)


