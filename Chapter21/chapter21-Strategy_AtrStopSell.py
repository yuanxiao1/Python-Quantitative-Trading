#! /usr/bin/env python 
#-*- encoding: utf-8 -*- 
#author pythontab.com 

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web
import datetime
import copy
import talib

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

class FactorBuyAverBreak:
    def __init__(self,**kwargs):
        self.xd = kwargs['xd']
    
    def make_buy_order(self):
        buy_signal = True
        return buy_signal
    
    def fit_day(self,kl_index, stock_df):
    
        today = stock_df.ix[kl_index]#获取当天数据  
        day_ind = stock_df.index.get_loc(kl_index)

        if day_ind < self.xd - 1 or day_ind >= stock_df.shape[0] - 1:
            return False 

        if today.Close > stock_df.Close[day_ind-self.xd+1:day_ind+1].mean():
            #print 'FactorBuyAverBreak for info',kl_index,today.Close,stock_df.Close[day_ind-self.xd+1:day_ind+1].mean()
            return self.make_buy_order()
        return False
        
class FactorSellAverBreak:
    def __init__(self,**kwargs):
        self.xd = kwargs['xd']
        
    def fit_sell_order(self):
        sell_signal = True
        return sell_signal

    def fit_day(self,kl_index, stock_df, *args):
    
        today = stock_df.ix[kl_index]#获取当天数据  
        day_ind = stock_df.index.get_loc(kl_index)

        if day_ind < self.xd - 1 or day_ind >= stock_df.shape[0] - 1:
            return False 
       
        if today.Close < stock_df.Close[day_ind-self.xd+1:day_ind+1].mean():
            #print 'FactorSellAverBreak for info',kl_index,today.Close,stock_df.Close[day_ind-self.xd+1:day_ind+1].mean()
            #print 'FactorSellAverBreak for data',stock_df.Close[day_ind-self.xd+1:day_ind+1]
            return self.fit_sell_order()
        return False   
        
class FactorBuyNdayBreak:
    def __init__(self,**kwargs):
        self.xd = kwargs['xd']
    
    def make_buy_order(self):
        buy_signal = True
        return buy_signal
    
    def fit_day(self,kl_index, stock_df):
    
        today = stock_df.ix[kl_index]#获取当天数据  
        day_ind = stock_df.index.get_loc(kl_index)

        if day_ind < self.xd - 1 or day_ind >= stock_df.shape[0] - 1:
            return False 
            
        if today.Close == stock_df.Close[day_ind-self.xd+1:day_ind+1].max():
            #print 'FactorBuyNdayBreak for info',kl_index,today.Close,stock_df.Close[day_ind-self.xd+1:day_ind+1].max()
            return self.make_buy_order()
        return False
        
class FactorSellNdayBreak:
    def __init__(self,**kwargs):
        self.xd = kwargs['xd']
        
    def fit_sell_order(self):
        sell_signal = True
        return sell_signal

    def fit_day(self,kl_index, stock_df, *args):
    
        today = stock_df.ix[kl_index]#获取当天数据  
        day_ind = stock_df.index.get_loc(kl_index)

        if day_ind < self.xd - 1 or day_ind >= stock_df.shape[0] - 1:
            return False 
       
        if today.Close == stock_df.Close[day_ind-self.xd+1:day_ind+1].min():
            #print 'FactorSellNdayBreak for info',kl_index,today.Close,stock_df.Close[day_ind-self.xd+1:day_ind+1].min()
            return self.fit_sell_order()
        return False  
        
class FactorSellAtrStop:
    def __init__(self,**kwargs):
        if 'stop_loss_n' in kwargs:
            #设置止损ATR倍数
            self.stop_loss_n = kwargs['stop_loss_n']
            
        if 'stop_win_n' in kwargs:
            #设置止盈ATR倍数
            self.stop_win_n = kwargs['stop_win_n']
                    
    def fit_sell_order(self):
        sell_signal = True
        return sell_signal

    def fit_day(self,kl_index, stock_df, Buy_Price):
        
        today = stock_df.ix[kl_index]#获取当天数据  
        
        if Buy_Price == 0:#无成交价格
            return False 
            
        if (Buy_Price > today.Close) and ((Buy_Price - today.Close) > self.stop_loss_n * today.atr14):
            print('stop_loss_n',kl_index,today.Close,Buy_Price)
            return self.fit_sell_order()
            
        elif (Buy_Price < today.Close) and ((today.Close - Buy_Price) > self.stop_win_n * today.atr14):            
            print('stop_win_n',kl_index,today.Close,Buy_Price)
            return self.fit_sell_order()
        else:
            return False  
 
class QuantPickTimeSys:
    def __init__(self, kl_pd, buy_factors, sell_factors):
        """
        :param cap: 初始资金
        :param kl_pd: 择时时间段交易数据
        :param buy_factors: 买入因子序列，序列中的对象为dict，每一个dict针对一个具体因子
        :param sell_factors: 卖出因子序列，序列中的对象为dict，每一个dict针对一个具体因子
        """
        
        # 回测阶段kl
        self.kl_pd = kl_pd
        
        # 初始化买入因子列表
        self.init_buy_factors(buy_factors)
        # 初始化卖出因子列表
        self.init_sell_factors(sell_factors)
        self.buy_price = 0#买入价格
        self.cash_hold = 100000#初始资金
        self.posit_num = 0#持股数目
        self.market_total = 0#持股市值 
        self.profit_curve = [] 
        plt.figure(figsize=(25,12), dpi=80, facecolor="white")


    def init_buy_factors(self, buy_factors):

        """
        通过buy_factors实例化各个买入因子
        :param buy_factors: list中元素为dict，每个dict为因子的构造元素，如class，构造参数等
        :return:
        """
        self.buy_factors = list()

        if buy_factors is None:
            return

        for factor_class in buy_factors:
            if factor_class is None:
                continue #执行下个循环
            if 'class' not in factor_class:
                raise ValueError('factor class key must name class!!')
            #print "before copy",id(factor_class)
            factor_class = copy.deepcopy(factor_class)
            #print "after copy",id(factor_class)
            class_fac = copy.deepcopy(factor_class['class'])
            del factor_class['class']
            #print "del",id(factor_class)
            
            '''实例化买入因子'''
            factor = class_fac(**factor_class)
            
            if not isinstance(factor, FactorBuyAverBreak) and not isinstance(factor, FactorBuyNdayBreak): #判断factor为基于FactorBuyBreak实例
                raise TypeError('factor must base FactorBuyBreak!!')
            self.buy_factors.append(factor)

    def init_sell_factors(self, sell_factors):
        """
        通过sell_factors实例化各个卖出因子
        :param sell_factors: list中元素为dict，每个dict为因子的构造元素，如class，构造参数等
        :return:
        """
        self.sell_factors = list()

        if sell_factors is None:
            return
        
        for factor_class in sell_factors:
            if factor_class is None:
                continue #执行下个循环
            if 'class' not in factor_class:
                raise ValueError('factor class key must name class!!')
            factor_class = copy.deepcopy(factor_class)
            class_fac = copy.deepcopy(factor_class['class'])
            del factor_class['class']
            
            '''实例化卖出因子'''
            factor = class_fac(**factor_class)
            
            if not isinstance(factor, FactorSellAverBreak) and not isinstance(factor, FactorSellNdayBreak) and not isinstance(factor, FactorSellAtrStop):#判断factor为基于FactorBuyBreak实例
                raise TypeError('factor must base FactorSellBreak!!')
            self.sell_factors.append(factor)

            
    def _day_task(self, kl_index, Buy_Price):
        
        fact_buy,fact_sell,sell_buf,buy_buf = 0,0,0,0
        
        for index, buy_factor in enumerate(self.buy_factors):
            #遍历所有买入因子
            buy_buf += buy_factor.fit_day(kl_index, self.kl_pd)

        fact_buy = 1 if (buy_buf == (index+1)) else 0
            
        for index, sell_factor in enumerate(self.sell_factors):
            #遍历所有卖出因子
            sell_buf += sell_factor.fit_day(kl_index, self.kl_pd, Buy_Price)

        fact_sell = -1 if (sell_buf > 0) else 0

        return fact_buy or fact_sell
        
    def run_factor_plot(self):

        list_signal = []
        is_win = False
        self.kl_pd['Ma30'] = self.kl_pd.Close.rolling(window=30).mean()#pd.rolling_mean(self.kl_pd.Close,window=30)#增加M30移动平均线 

        #print self.kl_pd.loc['2017-12-27':'2018-02-09'].filter(['Close','Ma30'])
        
        #self.kl_pd.apply(self._day_task, axis=1)
        
        self.kl_pd['atr14'] = talib.ATR(self.kl_pd.High.values,self.kl_pd.Low.values,self.kl_pd.Close.values,timeperiod=14)#计算ATR14 
        self.kl_pd['atr21'] = talib.ATR(self.kl_pd.High.values,self.kl_pd.Low.values,self.kl_pd.Close.values,timeperiod=21)#计算ATR21 
        
        #pd.DataFrame({'close':self.kl_pd.Close, 'atr14':self.kl_pd.atr14,'art21':self.kl_pd.art21,})
        self.kl_pd['artwin'] = self.kl_pd.Close - self.kl_pd['atr14']*3#止盈对应的买入价位
        self.kl_pd['artloss'] = self.kl_pd.Close + self.kl_pd['atr14']*1#止损对应的买入价位
        
        p1 = plt.subplot(3,1,1)
        self.kl_pd.Close.plot()
        self.kl_pd.Ma30.plot(c='black')
        self.kl_pd.artwin.plot()
        self.kl_pd.artloss.plot()

        plt.title(u'浙大网新')
        plt.ylim(np.min(self.kl_pd.Close)-5,np.max(self.kl_pd.Close)+5)#设置Y轴范围
        plt.xticks([])  #去掉纵坐标值
        plt.legend(['Close','30ave','atrwin','artloss'],loc='best')

        
        for kl_index,today in self.kl_pd.iterrows():

            signal = self._day_task(kl_index, self.buy_price)
            
            if signal > 0:# 买入    
                if is_win == False:#空仓则买
                    start = self.kl_pd.index.get_loc(kl_index)
                    is_win = True
                    self.buy_price = today.Close
                    self.posit_num = int(self.cash_hold/today.Close)
                    self.cash_hold = 0 
                    print("Start order",kl_index,today.Close)
                    plt.annotate('B',xy=(kl_index,self.kl_pd.Close.asof(kl_index)),xytext=(kl_index, self.kl_pd.Close.asof(kl_index)+4),arrowprops=dict(facecolor='yellow',shrink=0.1),horizontalalignment='left',verticalalignment='top')

            elif signal < 0:# 卖出 
                if is_win == True:#避免未买先卖
                    end = self.kl_pd.index.get_loc(kl_index)
                    is_win = False
                    self.buy_price = 0
                    print("End order",kl_index,today.Close)
                    self.cash_hold = int(self.posit_num*today.Close)
                    self.market_total = 0

                    if self.kl_pd.Close[end] < self.kl_pd.Close[start]:#赔钱显示绿色
                        plt.fill_between(self.kl_pd.index[start:end],0,self.kl_pd.Close[start:end],color='green',alpha=0.38)
                        
                    else:#赚钱显示绿色
                        plt.fill_between(self.kl_pd.index[start:end],0,self.kl_pd.Close[start:end],color='red',alpha=0.38)
            list_signal.append(is_win) 
            
            if is_win == True:
                self.market_total = int(self.posit_num*today.Close)
                self.profit_curve.append(self.market_total)
            else:
                self.profit_curve.append(self.cash_hold)

        self.kl_pd['keep'] = list_signal
        self.kl_pd['keep'].fillna(method = 'ffill',inplace = True)

        """ 计算基准收益 """
        self.kl_pd['benchmark_profit'] = np.log(self.kl_pd.Close/self.kl_pd.Close.shift(1))
        """ 计算趋势突破策略收益 """
        self.kl_pd['trend_profit'] = self.kl_pd.keep*self.kl_pd.benchmark_profit  
        """ 可视化收益情况对比 """       
        p2 = plt.subplot(3,1,2)  
        self.kl_pd[['benchmark_profit','trend_profit']].cumsum().plot(grid=True,ax = p2)
        plt.xticks([])  #去掉纵坐标值
        plt.legend(['benchmark_profit','trend_profit'],loc='best')
                
        p3 = plt.subplot(3,1,3)       
        p3.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(1),interval=1))
        p3.xaxis.set_minor_formatter(mdates.DateFormatter('%d\n%a'))                
        self.kl_pd['profit'] = self.profit_curve
        self.kl_pd.profit.plot()
        plt.legend(['profit'],loc='best')
        plt.xticks([])  #去掉纵坐标值
        #plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0, hspace=0.25)
        plt.subplots_adjust(left=0.09,bottom=0.20, right=0.94,top=0.95, wspace=0, hspace=0.25)
        plt.show()

""" 多因子策略测试 """
buy_factors = [{'xd': 20,'class': FactorBuyNdayBreak},
               {'xd': 30,'class': FactorBuyAverBreak}]

sell_factors = [{'xd': 5,'class': FactorSellNdayBreak},
                {'xd': 30,'class': FactorSellAverBreak}]
                {'stop_loss_n': 0.8,'stop_win_n': 2,'class': FactorSellAtrStop}]

stock = web.DataReader("600797.SS", "yahoo", datetime.datetime(2018,1,1), datetime.date.today())
examp_trade= QuantPickTimeSys(stock,buy_factors,sell_factors)
examp_trade.run_factor_plot()

        
