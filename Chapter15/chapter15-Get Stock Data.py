#! /usr/bin/env python 
#-*- encoding: utf-8 -*- 
#author pythontab.com 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import datetime
#import tushare as ts

df_stockload = web.DataReader("000001.SS", "yahoo", datetime.datetime(2017,1,1), datetime.date.today())
#print(type(datetime.datetime.now().strftime('%Y-%m-%d')))
#df_stockload = ts.get_hist_data('sh',start='2017-01-01',end=datetime.datetime.now().strftime('%Y-%m-%d'))
print (df_stockload.columns)#查看列名
print (df_stockload.index)#查看索引
print (df_stockload.describe())#查看各列数据描述性统计

#绘制移动平均线
df_stockload.Close.plot(c='b')
df_stockload.Close.rolling(window=30).mean().plot(c='r') #pd.rolling_mean(df_stockload.Close,window=30).plot(c='r')
df_stockload.Close.rolling(window=60).mean().plot(c='g') #pd.rolling_mean(df_stockload.Close,window=60).plot(c='g')
plt.legend(['Close','30ave','60ave'],loc='best')
plt.show()
"""
df_concept = ts.get_concept_classified()#概念分类
print (df_concept.head(20))
"""
