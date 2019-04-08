import time
from pandas import Series,DataFrame
import pandas as pd
import numpy as np
import cmath
import xlrd
from datetime import datetime


#设置路径
path = 'C:\\Users\\shingsho\\Desktop\\data\\holi.xlsx'
#打开excel
workbook = xlrd.open_workbook(path)
#根据sheet索引获取sheet内容
Data_sheet = workbook.sheets()[0] # 通过索引获取
# Data_sheet = workbook.sheet_by_index(0)  # 通过索引获取
# Data_sheet = workbook.sheet_by_name(u'名称')  # 通过名称获取
print (Data_sheet.name)

rowNum = Data_sheet.nrows
colNum = Data_sheet.ncols

date = pd.read_csv('C:\\Users\\shingsho\\Desktop\\data\\holi.csv')
#print (date)

def holiday(d):
    #七天假期
    holi7day = {"2016/2/7","2016/2/8","2016/2/9","2016/2/10","2016/2/11","2016/2/12","2016/2/13",
            "2016/10/1","2016/10/2","2016/10/3","2016/10/4","2016/10/5","2016/10/6","2016/10/7",
            "2017/1/27","2017/1/28","2017/1/29","2017/1/30","2017/1/31","2017/2/1","2017/2/2",
            "2017/10/1","2017/10/2","2017/10/3","2017/10/4","2017/10/5","2017/10/6","2017/10/7",
            "2018/2/15","2018/2/16","2018/2/17","2018/2/18","2018/2/19","2018/2/20","2018/2/21",
            "2018/10/1","2018/10/2","2018/10/3","2018/10/4","2018/10/5","2018/10/6","2018/10/7",
            "2019/2/4","2019/2/5","2019/2/6","2019/2/7","2019/2/8","2019/2/9","2019/2/10"}

    #三天假期
    holi3day = {"2016/1/1","2016/1/2","2016/1/3","2016/4/2","2016/4/3","2016/4/4",
            "2016/4/30","2016/5/1","2016/5/2","2016/6/9","2016/6/10","2016/6/11",
            "2016/9/15","2016/9/16","2016/9/17","2016/12/31","2017/1/1","2017/1/2",
            "2017/4/2","2017/4/3","2017/4/4","2017/4/29","2017/4/30","2017/5/1",
            "2017/5/28","2017/5/29","2017/5/30","2017/12/30","2017/12/31","2018/1/1",
            "2018/4/5","2018/4/6","2018/4/7","2018/4/29","2018/4/30","2018/5/1",
            "2018/6/16","2018/6/17","2018/6/18","2018/9/22","2018/9/23","2018/9/24",
            "2018/12/30","2018/12/31","2019/1/1"}

    #调休工作日
    work = {"2015/10/10","2016/2/6","2016/2/14","2016/6/12","2016/10/8","2016/10/9",
            "2017/1/22","2017/2/4","2017/4/1","2017/5/27","2017/9/30","2018/2/11","2018/2/24",
            "2018/4/8","2018/4/28","2018/9/29","2018/9/30","2018/12/29","2019/2/2","2019/2/3"}


    if not isinstance(d, str):
        print("Please input string date")
        return -1
    else:
        d1 = datetime.strptime(d, '%Y/%m/%d')
        if d in holi7day:
            return 1
        elif d in holi3day:
            return 2
        elif d in work:
            return 4
        elif d1.weekday() in (5, 6):
            return 3
        else:
            return 4

holiSeries = Series([holiday(str(date.loc[0][0]))])

#读取excel第一列，分别对每个日期求出其类别
for i in range(0,1250):
    #print(date.loc[i][0])
    holiSeries[i] = holiday(date.loc[i][0])
#print (holiSeries)
totalResult = pd.DataFrame({'holiday':holiSeries})
totalResult.to_excel("holi.xlsx")

