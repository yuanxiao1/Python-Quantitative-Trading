#! /usr/bin/env python 
#-*- encoding: utf-8 -*- 
#author pythontab.com 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec#分割子图
import mpl_finance as mpf #替换 import matplotlib.finance as mpf
import pandas as pd
import pandas_datareader.data as web
import datetime
import talib
import csv,os,codecs
import tushare as ts

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

#规整化 测试 #cmd /k C:\Users\Administrator\AppData\Local\Programs\Python\Python37-32\python.exe "$(FULL_CURRENT_PATH)" & PAUSE & EXIT

def plot_trade(stock_df):

    if os.path.isfile('C:\\Users\\Administrator\\Desktop\\ZDWX600797.csv'):
        f=codecs.open('C:\\Users\\Administrator\\Desktop\\ZDWX600797.csv','rb','gb2312')#GB2312编码——>unicode
        #u = f.read()
        #print type(u)#<type 'unicode'>
        reader = csv.DictReader(f)

        for row in reader:
            #print type(row["名称"]),row["名称"].encode('gb2312')#<type 'str'>
            #start = stock_df[stock_df.index == buy_date].key.values[0]#起始时间
            #end = stock_df[stock_df.index == sell_date].key.values[0]#终止时间
            buy_date = row["买入时间"]
            sell_date = row["卖出时间"]
            hands_num =  row["股数"]
            #print len("卖"),len(u"卖"),buy_date,sell_date,hands_num,row #3 / 1
            start = stock_df.index.get_loc(buy_date)#'2017-01-16'
            end = stock_df.index.get_loc(sell_date)#'2017-03-16'

            if stock_df.Close[end] < stock_df.Close[start]:#赔钱显示绿色
                plt.fill_between(stock_df.index[start:end],0,stock_df.Close[start:end],color='green',alpha=0.38)
                is_win = False
            else:#赚钱显示绿色
                plt.fill_between(stock_df.index[start:end],0,stock_df.Close[start:end],color='red',alpha=0.38)
                is_win = True
            plt.annotate('获利\n'+ hands_num+u'手' if is_win else '亏损\n'+hands_num+u'手',xy=(sell_date,stock_df.Close.asof(sell_date)),xytext=(sell_date, stock_df.Close.asof(sell_date)+4),arrowprops=dict(facecolor='yellow',shrink=0.1),horizontalalignment='left',verticalalignment='top')
            #print(buy_date,sell_date)
        f.close()
    plt.plot(stock_df.index,stock_df.Close,color='r')
    
    """整个时间序列填充为底色blue 透明度alpha小于后标注区间颜色"""    
    plt.fill_between(stock_df.index,0,stock_df.Close,color='blue',alpha=.08)

    plt.xlabel('time')
    plt.ylabel('close')
    plt.title(u'浙大网新')
    plt.grid(True)
    plt.ylim(np.min(stock_df.Close)-5,np.max(stock_df.Close)+5)#设置Y轴范围
    plt.legend(['Close'],loc='best')
    plt.show()

def plot_trade_profit(stock_df):

    fig = plt.figure(figsize=(8,6), dpi=100,facecolor="white")#创建fig对象
    gs = gridspec.GridSpec(3, 1, left=0.05, bottom=0.15, right=0.96, top=0.96, wspace=None, hspace=0.2, height_ratios=[4.5,2,2])
    graph_trade = fig.add_subplot(gs[0,:])
    graph_total = fig.add_subplot(gs[1,:])
    graph_profit = fig.add_subplot(gs[2,:])    

    if os.path.isfile('C:\\Users\\Administrator\\Desktop\\ZDWX600797.csv'):
        f=codecs.open('C:\\Users\\Administrator\\Desktop\\ZDWX600797.csv','rb','gb2312')#GB2312编码——>unicode
        reader = csv.DictReader(f)

        for row in reader:
            buy_date = row["买入时间"]
            sell_date = row["卖出时间"]
            hands_num =  row["股数"]
             
            start = stock_df.index.get_loc(buy_date)#'2017-01-16'
            end = stock_df.index.get_loc(sell_date)#'2017-03-16'

            stock_df.loc[buy_date,'signal'] = 1 #买入股票符号
            stock_df.loc[buy_date,'price'] = float(row["买入价格"]) #买入股票价格

            stock_df.loc[sell_date,'signal'] = 0 #卖出股票符号
            stock_df.loc[sell_date,'price'] = float(row["卖出价格"]) #卖出股票价格

            if stock_df.Close[end] < stock_df.Close[start]:#赔钱显示绿色
                graph_trade.fill_between(stock_df.index[start:end],0,stock_df.Close[start:end],color='green',alpha=0.38)
                is_win = False
            else:#赚钱显示绿色
                graph_trade.fill_between(stock_df.index[start:end],0,stock_df.Close[start:end],color='red',alpha=0.38)
                is_win = True
            graph_trade.annotate('获利\n'+ hands_num+u'手' if is_win else '亏损\n'+hands_num+u'手',xy=(sell_date,stock_df.Close.asof(sell_date)),xytext=(sell_date, stock_df.Close.asof(sell_date)+4),arrowprops=dict(facecolor='yellow',shrink=0.1),horizontalalignment='left',verticalalignment='top')
            
        f.close()
    graph_trade.plot(stock_df.index,stock_df.Close,color='r')

    """整个时间序列填充为底色blue 透明度alpha小于后标注区间颜色"""    
    graph_trade.fill_between(stock_df.index,0,stock_df.Close,color='blue',alpha=.08)

    graph_trade.set_ylabel('close')
    graph_trade.set_title(u'浙大网新')
    graph_trade.grid(True)
    graph_trade.set_ylim(np.min(stock_df.Close)-5,np.max(stock_df.Close)+5)#设置Y轴范围
    graph_trade.legend(['Close'],loc='best')

    skip_days = 0
    cash_hold = 100000#初始资金
    posit_num = 0#持股数目
    market_total = 0#持股市值 
    profit_curve = [] 

    stock_df['keep'] = stock_df.signal
    stock_df['keep'].fillna(method = 'ffill',inplace = True)

    """ 计算基准收益 """
    stock_df['benchmark_profit'] = np.log(stock_df.Close/stock_df.Close.shift(1))
    print('benchmark_profit',stock_df['benchmark_profit'])
    """ 计算趋势突破策略收益 """
    stock_df['trend_profit'] = stock_df.keep*stock_df.benchmark_profit        
           
    for kl_index,today in stock_df.iterrows():
        if today.signal == 1:# 买入    
            start = stock_df.index.get_loc(kl_index)
            skip_days = -1
            posit_num = int(cash_hold/today.Close)
            cash_hold = 0 
        elif today.signal == 0:# 卖出 
            if skip_days == -1:#避免未买先卖
                end = stock_df.index.get_loc(kl_index)
                skip_days = 0
                cash_hold = int(posit_num*today.Close)
                market_total = 0
        if skip_days == -1:
            market_total = int(posit_num*today.Close)
            profit_curve.append(market_total)
        else:
            profit_curve.append(cash_hold)
     
    stock_df['total'] = profit_curve
    print(stock_df['total'])
    stock_df.total.plot(grid=True,ax = graph_total)#ax选择图形显示的子图
    graph_total.legend(['total'],loc='best')

    stock_df[['benchmark_profit','trend_profit']].cumsum().plot(grid=True,ax = graph_profit)
    graph_profit.set_xlabel('time')
    graph_profit.legend(['benchmark_profit','trend_profit'],loc='best')
    
    for label in graph_trade.xaxis.get_ticklabels():   
        label.set_visible(False)
        
    for label in graph_total.xaxis.get_ticklabels():   
        label.set_visible(False)

    for label in graph_profit.xaxis.get_ticklabels():   
        label.set_rotation(45)
        label.set_fontsize(10)#设置标签字体

    plt.show()        
"""
stock = web.DataReader("AAPL", "yahoo", datetime.datetime(2017,1,1), datetime.date.today())#苹果公司数据获取
"""
stock = web.DataReader("600797.SS", "yahoo", datetime.datetime(2018,1,1), datetime.date.today())

#plot_trade(stock)
plot_trade_profit(stock)
