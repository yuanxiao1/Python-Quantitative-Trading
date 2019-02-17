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
#cmd /k C:\Users\Administrator\AppData\Local\Programs\Python\Python37-32\python.exe "$(FULL_CURRENT_PATH)" & PAUSE & EXIT
class QuantAverBreak:
    def __init__(self):
        self.skip_days = 0
        self.cash_hold = 100000#初始资金
        self.posit_num = 0#持股数目
        self.market_total = 0#持股市值 
        self.profit_curve = [] 
        plt.figure(figsize=(25,12), dpi=80, facecolor="white")
        
        
    def run_factor_plot(self, stock_df):

        stock_df['Ma20'] = stock_df.Close.rolling(window=20).mean()#增加M60移动平均线       
        list_diff = np.sign(stock_df.Close-stock_df.Ma20)
        stock_df['signal'] = np.sign(list_diff-list_diff.shift(1))

        p1 = plt.subplot(2,1,1)
        plt.title(u'浙大网新')
        plt.ylim(np.min(stock_df.Close)-5,np.max(stock_df.Close)+5)#设置Y轴范围
        stock_df.Close.plot()
        stock_df.Ma20.plot(c='black')
        plt.legend(['Close','20ave'],loc='best')
      
        for kl_index,today in stock_df.iterrows():
            #print "kl_index",kl_index
            #print "today",today
            if today.signal > 0:# 买入    
                print("buy",kl_index)
                start = stock_df.index.get_loc(kl_index)
                self.skip_days = -1
                self.posit_num = int(self.cash_hold/today.Close)
                self.cash_hold = 0 
            elif today.signal < 0:# 卖出 
                if self.skip_days == -1:#避免未买先卖
                    print("sell",kl_index)
                    end = stock_df.index.get_loc(kl_index)
                    self.skip_days = 0
                    self.cash_hold = int(self.posit_num*today.Close)
                    self.market_total = 0
                    if stock_df.Close[end] < stock_df.Close[start]:#赔钱显示绿色
                        plt.fill_between(stock_df.index[start:end],0,stock_df.Close[start:end],color='green',alpha=0.38)
                        is_win = False
                    else:#赚钱显示红色
                        plt.fill_between(stock_df.index[start:end],0,stock_df.Close[start:end],color='red',alpha=0.38)
                        is_win = True
            if self.skip_days == -1:
                self.market_total = int(self.posit_num*today.Close)
                self.profit_curve.append(self.market_total)
            else:
                self.profit_curve.append(self.cash_hold)
        p1 = plt.subplot(2,1,2)        
        stock_df['profit'] = self.profit_curve
        stock_df.profit.plot()
        plt.legend(['profit'],loc='best')

        #plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0, hspace=0.25)
        plt.subplots_adjust(left=0.09,bottom=0.20, right=0.94,top=0.95, wspace=0.2, hspace=0)
        plt.show()

        
stock = web.DataReader("600797.SS", "yahoo", datetime.datetime(2017,1,1), datetime.date.today())
examp_trade = QuantAverBreak()
examp_trade.run_factor_plot(stock)
        
