#! /usr/bin/env python 
#-*- encoding: utf-8 -*- 
#author pythontab.com 
import pandas as pd
import numpy as np
import datetime #存储CSV文件使用


#3、Pandas工具快速入门：数据规整化处理

print(u"**********************************1.1、数据信息查看*********************************************************")

#加载csv文件数据
df_csvload  = pd.read_csv('C:\\Users\\Administrator\\Desktop\\table.csv',parse_dates=True,index_col=0,encoding='gb2312')

print(df_csvload.head())#查看前几行   
print(df_csvload.tail())#查看后几行
print(df_csvload.columns)#查看列名
print(df_csvload.index)#查看索引
print(df_csvload.shape)#查看形状

print(df_csvload.describe())#查看各列数据描述性统计
print(df_csvload.info())#查看缺失及每列数据类型 事先去除数值
print(u"**********************************1.2、缺失值处理*********************************************************")

print(df_csvload.isnull())#判断数据缺失值
print(df_csvload[df_csvload.isnull().T.any().T])#查看NAN值所在行
#只要有一个缺失值就删除该行
#df_csvload = df_csvload.dropna(axis=0,how='any')#NAN值删除 
#print(df_csvload)
df_csvload = df_csvload.dropna(axis=0,how='all')#NAN值删除 所有值都为缺失值时才删除该行
df_csvload.fillna(method='bfill',axis=0,inplace=True)#NAN值填充 列方向前值填充
print(df_csvload[df_csvload.isnull().values==True])#查看NAN值删除填充后值

print(u"**********************************1.3、特殊值处理*********************************************************")

#df_csvload = df_csvload.applymap(lambda x:'%0.2f'%x)#保留2位小数
#print(df_csvload)
#print(df_csvload.info())
df_csvload = df_csvload.round(2)#保留2位小数
print(df_csvload)
print(df_csvload.info())
print(df_csvload[df_csvload.values==0])#查看df_csvload数据中所有0值的元素
df_csvload.loc[df_csvload.loc[:,'Low']==0,'Low'] = df_csvload.Low.median()#
print(df_csvload.loc['2018-01-15'])

print(u"**********************************1.4、数据运算转化*********************************************************")

#数据运算
change = df_csvload.High - df_csvload.Low#最高价-最低价
df_csvload['pct_change'] = (change / df_csvload['Close'].shift(1)) #/昨收
print(df_csvload)
df_csvload['pct_change'].fillna(df_csvload['pct_change'].mean(),inplace=True) #序列第一个值Na
print(df_csvload)

print(u"**********************************1.5、数据合并及连接*********************************************************")

#数据合并
dfv_csvload  = pd.read_csv('C:\\Users\\Administrator\\Desktop\\table-Volume.csv',parse_dates=True,index_col=0,encoding='gb2312')
df_concat =pd.concat([df_csvload, dfv_csvload],axis=1,keys=['Price','amount'])
print(df_concat)

