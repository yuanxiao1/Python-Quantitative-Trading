#! /usr/bin/env python 
#-*- encoding: utf-8 -*- 
#author pythontab.com 
import pandas as pd
import numpy as np
import datetime #存储CSV文件使用

print(u"**********************************1.1加载CSV文件*********************************************************")

#read_csv 测试
#加载csv文件数据
df_csvload  = pd.read_csv('C:\\Users\\Administrator\\Desktop\\table.csv',parse_dates=True,index_col=0,encoding='gb2312')
print(df_csvload)

#参数header=1
df_csvload  = pd.read_csv('C:\\Users\\Administrator\\Desktop\\table.csv',header=1,parse_dates=True,index_col=0,encoding='gb2312')
print(df_csvload)
print(df_csvload.index)
#参数parse_dates=False
df_csvload  = pd.read_csv('C:\\Users\\Administrator\\Desktop\\table.csv',parse_dates=False,index_col=0,encoding='gb2312')
print(df_csvload.index)

print(u"**********************************1.2存储CSV文件*********************************************************")

#to_csv 测试
#加载csv文件数据
df_csvload  = pd.read_csv('C:\\Users\\Administrator\\Desktop\\table.csv',parse_dates=True,index_col=0,encoding='gb2312')
#扩充2个交易日的股票数据
df_adddat = pd.DataFrame([{u'Open':1.1, u'High':1.2, u'Low':1.3, u'Close':1.4}, {u'Open':2.1, u'High':2.2, u'Low':2.3, u'Close':2.4}],index=[datetime.datetime.strptime("2016-06-25 00:00:00", "%Y-%m-%d %H:%M:%S"),datetime.datetime.strptime("2016-06-26 00:00:00", "%Y-%m-%d %H:%M:%S")])
df_csvload = df_csvload.append(df_adddat)  
print(df_csvload) 
#存储csv文件数据
df_csvload.to_csv('C:\\Users\\Administrator\\Desktop\\table-add.csv',columns=df_csvload.columns,index=True) 
print(u"*********************************************************************************************************")
print(u"*********************************************************************************************************")

