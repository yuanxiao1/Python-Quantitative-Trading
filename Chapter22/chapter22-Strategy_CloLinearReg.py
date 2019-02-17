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
import statsmodels.api as sm 
from statsmodels import regression

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

class FactorPickStockAng:        
    def __init__(self,**kwargs):            
        self.threshold_ang_min = -np.inf
        if 'threshold_ang_min' in kwargs:
            #设置最小角度阈值
            self.threshold_ang_min = kwargs['threshold_ang_min']
            
        self.threshold_ang_max = np.inf
        if 'threshold_ang_max' in kwargs:
            #设置最大角度阈值
            self.threshold_ang_max = kwargs['threshold_ang_max']
            
        plt.figure(figsize=(25,12), dpi=80, facecolor="white")
        
    def calc_regress_deg(self, y_arr):
        x= np.arange(0, len(y_arr))
        #y值缩放到与x一个级别
        #zoom_factor =x.max()/y_arr.max()
        #y_arr = zoom_factor * y_arr

        x = sm.add_constant(x)#添加常数列1
        
        model = regression.linear_model.OLS(y_arr, x).fit()#使用OLS做拟合
        rad = model.params[1]#y = kx + b :params[1] = k 
        deg = np.rad2deg(rad)#弧度转换为角度

        intercept = model.params[0]##y = kx + b :params[0] = b 
        reg_y_fit = x * rad + intercept
        
        return deg, x, reg_y_fit, y_arr  
            
    def fit_pick(self, symbols,show=True):
        
        for index, stockName in enumerate(symbols.keys()) :
            plt.subplot(len(symbols),1,index+1)  
            #print "stockName",stockName,symbols[stockName]
            kl_pd = web.DataReader(symbols[stockName], "yahoo", datetime.datetime(2018,6,1), datetime.date.today())
            kl_pd.fillna(method='bfill',inplace=True)#后一个数据填充NAN1
            print(kl_pd.head())
            
            ang, x, reg_y_fit, y_arr = self.calc_regress_deg(kl_pd.Close)#计算走势角度
            
            if self.threshold_ang_min < ang < self.threshold_ang_max:
                if show:
                    plt.plot(x, y_arr)
                    plt.plot(x, reg_y_fit,'r')
                    plt.xticks([])  #去掉纵坐标值
                    plt.title(stockName + 'deg = ' + str(ang))
                    plt.legend(['close','linear'],loc='best')
        plt.show()

""" 选股策略测试 """
pick_stocks = {u"浙大网新": "600797.SS",u"高鸿股份": "000851.SZ",u"开山股份": "300257.SZ",u"水晶光电": "002273.SZ"}
        
examp_trade= FactorPickStockAng()
examp_trade.fit_pick(pick_stocks)
""" 选股策略测试 """

        
