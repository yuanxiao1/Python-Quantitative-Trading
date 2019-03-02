#! /usr/bin/env python 
#-*- encoding: utf-8 -*- 
#author pythontab.com 

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
import datetime

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

class QuantNdaysBreak:
    def __init__(self):
        self.skip_days = 0
        self.cash_hold = 100000#初始资金
        self.posit_num = 0#持股数目
        self.market_total = 0#持股市值 
        self.profit_curve = [] 
        plt.figure(figsize=(25,12), dpi=80, facecolor="white")
        #plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0, hspace=0.25)
        plt.subplots_adjust(left=0.09,bottom=0.20, right=0.94,top=0.95, wspace=0.2, hspace=0)
        
    def run_factor_plot(self, stock_df):
        N1 = 22
        N2 = 11
        stock_df['N1_High'] = stock_df.High.rolling(window=N1).max()#计算最近N1个交易日最高价      
        expan_max = stock_df.Close.expanding().max()
        stock_df['N1_High'].fillna(value=expan_max,inplace=True)#目前出现过的最大值填充前N1个nan

        stock_df['N2_Low'] = stock_df.Low.rolling(window=N2).min()#计算最近N2个交易日最低价
        expan_min = stock_df.Close.expanding().min()
        stock_df['N2_Low'].fillna(value=expan_min,inplace=True)#目前出现过的最小值填充前N2个nan
        
        """ 收盘价超过N1最高价 买入股票持有"""
        buy_index = stock_df[stock_df.Close > stock_df.N1_High.shift(1)].index #报错 TypeError: '<' not supported between instances of 'float' and 'method'
        #print("buy_index",buy_index)
        stock_df.loc[buy_index,'signal'] = 1
        
        """ 收盘价超过N2最低价 卖出股票持有"""
        sell_index = stock_df[stock_df.Close < stock_df.N2_Low.shift(1)].index #报错 TypeError: '<' not supported between instances of 'float' and 'method'
        stock_df.loc[sell_index,'signal'] = 0
 
        stock_df['keep'] = stock_df.signal.shift(1)
        stock_df['keep'].fillna(method = 'ffill',inplace = True)

        """ 计算基准收益 """
        stock_df['benchmark_profit'] = np.log(stock_df.Close/stock_df.Close.shift(1))
        #stock_df['benchmark_profit'] = (stock_df.Close-stock_df.Close.shift(1))/stock_df.Close.shift(1)
        print('benchmark_profit',stock_df['benchmark_profit']) 
        
        """ 计算趋势突破策略收益 """
        stock_df['trend_profit'] = stock_df.keep*stock_df.benchmark_profit        
       
         
        """ 可视化收益情况对比 """       
        p1 = plt.subplot(2,1,1)
        plt.title(u'浙大网新')
        plt.ylim(np.min(stock_df.Close)-5,np.max(stock_df.Close)+5)#设置Y轴范围
        stock_df.Close.plot(ax = p1)
        plt.legend(['Close'],loc='best')
        
        stock_df['watsignal'] = np.sign(stock_df['keep']-stock_df['keep'].shift(1))

        for kl_index,today in stock_df.iterrows():
            if today.watsignal == 1:# 买入  
                self.skip_days = -1             
                start = stock_df.index.get_loc(kl_index)
            elif today.watsignal == -1:# 卖出
                if self.skip_days == -1: 
                    self.skip_days = 0
                    end = stock_df.index.get_loc(kl_index)
                    if stock_df.Close[end] < stock_df.Close[start]:#赔钱显示绿色
                        plt.fill_between(stock_df.index[start:end],0,stock_df.Close[start:end],color='green',alpha=0.38)
                    else:#赚钱显示绿色
                        plt.fill_between(stock_df.index[start:end],0,stock_df.Close[start:end],color='red',alpha=0.38)
                       
        p2 = plt.subplot(2,1,2)
        stock_df[['benchmark_profit','trend_profit']].cumsum().plot(grid=True,ax = p2)
        plt.legend(['benchmark_profit','trend_profit'],loc='best')

        plt.show()

        
stock = web.DataReader("000851.SZ", "yahoo", datetime.datetime(2017,1,1), datetime.date.today())
examp_trade= QuantNdaysBreak()
examp_trade.run_factor_plot(stock)
        
