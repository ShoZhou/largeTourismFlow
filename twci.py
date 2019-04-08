from pandas import Series,DataFrame
import pandas as pd
import numpy as np
import cmath

#tData获取csv文件
tData = pd.read_csv('C:\\Users\\shingsho\\Desktop\\data\\tourismnew.csv')
tData.describe()

#温湿指数计算函数，hmture为结果，temp为温度，humi为湿度0-100间的数字
def humiditure(temp,humi):
    hmture = (1.8*temp+32)-0.55*(1-humi/100)*(1.8*temp-26)
    return hmture

#风寒指数计算函数，temp为摄气温，windspeed为风速，单位0.1m/s，iso为日照时间
def windCold(temp,windspeed,iso):
    windCold = -(33-temp)*(10*cmath.sqrt(windspeed)+10.45-windspeed)+8.55*iso/10
    return float(windCold)

#穿衣指数计算函数temp为温度，v为风速，小金纬度102.14，角度90-102.14弧度
#1春天 2夏天 3秋天 4冬天
def ICL(temp,v,season):
    if season == 1:
        a=-0.2118
    elif season == 2:
        a=0.1941
    elif season == 3:
        a=-0.2118
    else:
        a=-0.6178
    icl=(33-temp)/(0.155*87)-(87+0.06*1385*cmath.cos(a))/(0.62+19.0*cmath.sqrt(v))/87
    return float(icl)
#综合舒适度计算函数，thi,wci,icl
def cIndex(thi,wci,icl):
    cid = 0.6*thi+0.3*wci+0.1*icl
    return float(cid)

#对thi分级
def thiLev(thi):
    if thi>80:
        thilv = 1
    elif thi>75:
        thilv = 3
    elif thi>70:
        thilv = 5
    elif thi>65:
        thilv = 7
    elif thi>60:
        thilv = 9
    elif thi>55:
        thilv = 7
    elif thi>45:
        thilv = 5
    elif thi>40:
        thilv = 3
    else:
        thilv = 1
    return thilv
#对wci分级
def wciLev(wci):
    if wci>=160:
        wcilv = 1
    elif wci>80:
        wcilv = 3
    elif wci>-50:
        wcilv = 5
    elif wci>-200:
        wcilv = 7
    elif wci>-300:
        wcilv = 9
    elif wci>-600:
        wcilv = 7
    elif wci>-800:
        wcilv = 5
    elif wci>-1000:
        wcilv = 3
    else:
        wcilv = 1
    return wcilv

#icl分级
def iclLev(icl):
    if icl>2.5:
        icllv = 1
    elif icl>1.8:
        icllv = 3
    elif icl>1.5:
        icllv = 5
    elif icl>1.3:
        icllv = 7
    elif icl>0.7:
        icllv = 9
    elif icl>0.5:
        icllv = 7
    elif icl>0.3:
        icllv = 5
    elif icl>0.1:
        icllv = 3
    else:
        icllv = 1
    return icllv

#对cid分级
def cidLev(cid):
    if cid>7:
        cidlv = 'CLV1'
    elif cid>5:
        cidlv = 'CLV2'
    elif cid>3:
        cidlv = 'CLV3'
    else:
        cidlv = 'CLV4'
    return cidlv

#tData[i][j]i为行索引，j为列索引 
#thiSeries用于存储温湿指数，wciSeries存放风寒指数，iclSeries存储穿衣指数
thiSeries = Series([humiditure(tData.loc[0][5],tData.loc[0][2])])
wciSeries = Series([windCold(tData.loc[0][5],tData.loc[0][6],tData.loc[0][8])])
iclSeries = Series([ICL(tData.loc[0][5],tData.loc[0][6],tData.loc[0][7])])
cIdSeries = Series([thiLev(thiSeries[0]),wciLev(wciSeries[0]),iclLev(iclSeries[0])])

#循环体，分别计算每一天的温湿指数，风寒指数，存放在Series中
for i in range(1,1250):
    result1 = humiditure(tData.loc[i][5],tData.loc[i][2])
    result2 = windCold(tData.loc[i][5],tData.loc[i][6],tData.loc[i][8])
    result3 = ICL(tData.loc[i][5],tData.loc[i][6],tData.loc[i][7])
    
    thiSeries[i] = result1
    wciSeries[i] = result2
    iclSeries[i] = result3

    result4 = cIndex(thiLev(thiSeries[i]),wciLev(wciSeries[i]),iclLev(iclSeries[i]))
    cIdSeries[i] = result4

#thi等级wci等级icl等级
thiLv = Series([thiLev(thiSeries[0])])
wciLv = Series([wciLev(wciSeries[0])])
iclLv = Series([iclLev(iclSeries[0])])
cidLv = Series([cidLev(cIdSeries[0])])
dateSeries = Series(tData.loc[0][0])
#创建三个Series分别存储thi wci icl的对应等级
for i in range(1,1250):
    thiLv[i] = thiLev(thiSeries[i])
    wciLv[i] = wciLev(wciSeries[i])
    iclLv[i] = iclLev(iclSeries[i])
    cidLv[i] = cidLev(cIdSeries[i])
    dateSeries[i] = tData.loc[i][0]



#totalResult将温湿指数thi，风寒指数wci，穿衣指数icl，综合舒适度cid4个series存储到一个dataframe中
totalResult = pd.DataFrame({'date':dateSeries,'thi':thiSeries,'wci':wciSeries,'icl':iclSeries,'cid':cIdSeries})
totalResult.to_excel("twicResult.xlsx")
#levelResult存储对应等级
levelResult = pd.DataFrame({'date':dateSeries,'thiLV':thiLv,'wciLV':wciLv,'iclLV':iclLv,'comfortLV':cIdSeries,'CLV':cidLv})
levelResult.to_excel("lvResult.xlsx")

#print (tData.ix[10:20,0:7])
#print(tData)
print (tData.columns)
#print (tData['Date'])
#print (humiditureSeries)
#print (windColdIndexSeries)
#print (SSeries)
#print (tData.loc[0][5])
print (totalResult)