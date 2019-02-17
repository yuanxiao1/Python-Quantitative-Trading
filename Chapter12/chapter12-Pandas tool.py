#! /usr/bin/env python 
#-*- encoding: utf-8 -*- 
#author pythontab.com 
import pandas as pd
import numpy as np
import datetime #存储CSV文件使用


#4、Pandas工具快速入门：数据遍历的方法

print(u"**********************************1.for..in循环迭代方式*********************************************************")

 
"""
#迭代循环测试
x = [1,2,3]
its = x.__iter__() #列表是可迭代对象，否则会提示不是迭代对象
print(its)
#<list_iterator object at 0x100f32198>
print(next(its)) # its包含此方法，说明its是迭代器
#1
print(next(its)) 
#2
print(next(its)) 
#3
print(next(its)) 
"""
""" 
#生成器测试
def gensquares(N):
	for i in range(N):
		yield i**2 
print(gensquares(5))
for i in gensquares(5):
	print(i) 

print(x**2 for x in range(5))
print(list(x**2 for x in range(5)))

#<generator object <genexpr> at 0xb3d31fa4>
#[0, 1, 4, 9, 16]
"""
 
from timeit import timeit 
def iterator_looping(df):
    disftance_list = []
    for i in range(0,len(df)):
        disftance_list.append(df.iloc[i]['Open']-df.iloc[i]['Close'])
    return disftance_list

print(iterator_looping(df_csvload))

disftance_list = [(df_csvload.iloc[i]['Open']-df_csvload.iloc[i]['Close']) for i in range(0,len(df_csvload))]
print(disftance_list)

def iterrows_loopiter(df):
    disftance_list = []
    for index,row in df.iterrows():
        disftance_list.append(row['Open']-row['Close'])
    return disftance_list
print(iterrows_loopiter(df_csvload))    
    
    
disftance_list = df_csvload.apply(lambda row: (row['Open']-row['Close']), axis =1)
print(disftance_list)

df_csvload['rate'] = df_csvload['Open']-df_csvload['Close']
print(df_csvload['rate'])

df_csvload['rate'] = df_csvload['Open'].values-df_csvload['Close'].values 
print(df_csvload['rate'])

def test1():
    iterator_looping(df_csvload)
def test2():
    iterrows_loopiter(df_csvload)   
def test3():
    disftance_list = df_csvload.apply(lambda row: (row['Open']-row['Close']), axis =1)
def test4():
    df_csvload['rate'] = df_csvload['Open']-df_csvload['Close']
def test5():
    df_csvload['rate'] = df_csvload['Open'].values-df_csvload['Close'].values 

#for..in循环迭代方式
t1 = timeit('test1()', 'from __main__ import test1', number=1000)
#iterrows()遍历方式
t2 = timeit('test2()', 'from __main__ import test2', number=1000)
#apply()方法循环方式
t3 = timeit('test3()', 'from __main__ import test3', number=1000)
#Pandas series 的矢量化方式
t4 = timeit('test4()', 'from __main__ import test4', number=1000)
#Numpy arrays的矢量化方式：
t5 = timeit('test5()', 'from __main__ import test5', number=1000)

print(t1,t2,t3,t4,t5)
