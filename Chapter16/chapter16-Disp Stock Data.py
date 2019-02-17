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
import tushare as ts

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

df_stockload = web.DataReader("600797.SS", "yahoo", datetime.datetime(2018,1,1), datetime.date.today())
#print(type(datetime.datetime.now().strftime('%Y-%m-%d')))
#df_stockload = ts.get_hist_data('600797',start='2018-01-01',end=datetime.datetime.now().strftime('%Y-%m-%d'))
#df_stockload = df_stockload.sort_index(ascending=False)#降序排序
#df_stockload = df_stockload.sort_index()#升序排序

#python3.7打印
print (df_stockload.head())#查看前几行 
print (df_stockload.columns)#查看列名
print (df_stockload.index)#查看索引
print (df_stockload.describe())#查看各列数据描述性统计

fig = plt.figure(figsize=(8,6), dpi=100,facecolor="white")#创建fig对象
#fig.subplots_adjust(left=0.09,bottom=0.20, right=0.94,top=0.90, wspace=0.2, hspace=0)
#graph_KAV = fig.add_subplot(1,1,1)#创建子图

gs = gridspec.GridSpec(4, 1, left=0.05, bottom=0.2, right=0.96, top=0.96, wspace=None, hspace=0, height_ratios=[3.5,1,1,1])
graph_KAV = fig.add_subplot(gs[0,:])
graph_VOL = fig.add_subplot(gs[1,:])
graph_MACD = fig.add_subplot(gs[2,:])
graph_KDJ = fig.add_subplot(gs[3,:])


""" 绘制K线图 """
#方法1
ohlc = []
ohlc = list(zip(np.arange(0,len(df_stockload.index)),df_stockload.Open,df_stockload.Close,df_stockload.High,df_stockload.Low))#使用zip方法生成数据列表 
mpf.candlestick_ochl(graph_KAV, ohlc, width=0.2, colorup='r', colordown='g', alpha=1.0)#绘制K线走势
#方法2
#mpf.candlestick2_ochl(graph_KAV, df_stockload.Open,df_stockload.Close,df_stockload.High,df_stockload.Low, width=0.5, colorup='r', colordown='g')#绘制K线走势
""" 绘制K线图 """

""" 绘制移动平均线图 """

df_stockload['Ma20'] = df_stockload.Close.rolling(window=20).mean()#pd.rolling_mean(df_stockload.Close,window=20)
df_stockload['Ma30'] = df_stockload.Close.rolling(window=30).mean()#pd.rolling_mean(df_stockload.Close,window=30)
df_stockload['Ma60'] = df_stockload.Close.rolling(window=60).mean()#pd.rolling_mean(df_stockload.Close,window=60)

numt = np.arange(0, len(df_stockload.index))

#绘制均线走势    
graph_KAV.plot(numt, df_stockload['Ma20'],'black', label='M20',lw=1.0)
graph_KAV.plot(numt, df_stockload['Ma30'],'green',label='M30', lw=1.0)
graph_KAV.plot(numt, df_stockload['Ma60'],'blue',label='M60', lw=1.0)
graph_KAV.legend(loc='best')

""" 绘制移动平均线图 """

#fig.suptitle('600797 浙大网新', fontsize = 14, fontweight='bold')
graph_KAV.set_title(u"600797 浙大网新-日K线")
#graph_KAV.set_xlabel("日期")
graph_KAV.set_ylabel(u"价格")
graph_KAV.set_xlim(0,len(df_stockload.index)) #设置一下x轴的范围
graph_KAV.set_xticks(range(0,len(df_stockload.index),15))#X轴刻度设定 每15天标一个日期
graph_KAV.grid(True,color='k')
#graph_KAV.set_xticklabels([df_stockload.index.strftime('%Y-%m-%d')[index] for index in graph_KAV.get_xticks()])#标签设置为日期


""" 绘制成交量图 """

graph_VOL.bar(numt, df_stockload.Volume,color=['g' if df_stockload.Open[x] > df_stockload.Close[x] else 'r' for x in range(0,len(df_stockload.index))])

graph_VOL.set_ylabel(u"成交量")
#graph_VOL.set_xlabel("日期")
graph_VOL.set_xlim(0,len(df_stockload.index)) #设置一下x轴的范围
graph_VOL.set_xticks(range(0,len(df_stockload.index),15))#X轴刻度设定 每15天标一个日期
#graph_VOL.set_xticklabels([df_stockload.index.strftime('%Y-%m-%d')[index] for index in graph_VOL.get_xticks()])#标签设置为日期

""" 绘制成交量图 """


''' 绘制MACD '''   
         
macd_dif, macd_dea, macd_bar = talib.MACD(df_stockload['Close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
graph_MACD.plot(np.arange(0, len(df_stockload.index)), macd_dif, 'red', label='macd dif') #dif    
graph_MACD.plot(np.arange(0, len(df_stockload.index)), macd_dea, 'blue', label='macd dea') #dea 
#绘制BAR>0 柱状图
bar_red = np.where(macd_bar>0, 2*macd_bar, 0)
#绘制BAR<0 柱状图
bar_green = np.where(macd_bar<0, 2*macd_bar, 0)        
graph_MACD.bar(np.arange(0, len(df_stockload.index)), bar_red, facecolor='red')
graph_MACD.bar(np.arange(0, len(df_stockload.index)), bar_green, facecolor='green')
graph_MACD.legend(loc='best',shadow=True, fontsize ='10')

graph_MACD.set_ylabel(u"MACD")
#graph_MACD.set_xlabel("日期")
graph_MACD.set_xlim(0,len(df_stockload.index)) #设置一下x轴的范围
graph_MACD.set_xticks(range(0,len(df_stockload.index),15))#X轴刻度设定 每15天标一个日期
#graph_MACD.set_xticklabels([df_stockload.index.strftime('%Y-%m-%d')[index] for index in graph_MACD.get_xticks()])#标签设置为日期

''' 绘制MACD ''' 

''' 绘制KDJ '''

xd = 9-1
date = df_stockload.index.to_series()
RSV = pd.Series(np.zeros(len(date)-xd),index=date.index[xd:])
Kvalue = pd.Series(0.0,index=RSV.index)
Dvalue = pd.Series(0.0,index=RSV.index)
Kvalue[0],Dvalue[0] = 50,50

for day_ind in range(xd, len(df_stockload.index)):
	RSV[date[day_ind]] = (df_stockload.Close[day_ind] - df_stockload.Low[day_ind-xd:day_ind+1].min())/(df_stockload.High[day_ind-xd:day_ind+1].max()-df_stockload.Low[day_ind-xd:day_ind+1].min())*100
	if day_ind > xd:
		index = day_ind-xd
		Kvalue[index] = 2.0/3*Kvalue[index-1]+RSV[date[day_ind]]/3
		Dvalue[index] = 2.0/3*Dvalue[index-1]+Kvalue[index]/3
df_stockload['RSV'] = RSV
df_stockload['K'] = Kvalue
df_stockload['D'] = Dvalue
df_stockload['J'] = 3*Kvalue-2*Dvalue   
 
graph_KDJ.plot(np.arange(0, len(df_stockload.index)), df_stockload['K'], 'blue', label='K') #K    
graph_KDJ.plot(np.arange(0, len(df_stockload.index)), df_stockload['D'], 'g--', label='D') #D
graph_KDJ.plot(np.arange(0, len(df_stockload.index)), df_stockload['J'], 'r-', label='J') #J         
graph_KDJ.legend(loc='best',shadow=True, fontsize ='10')

graph_KDJ.set_ylabel(u"KDJ")
graph_KDJ.set_xlabel("日期")
graph_KDJ.set_xlim(0,len(df_stockload.index)) #设置一下x轴的范围
graph_KDJ.set_xticks(range(0,len(df_stockload.index),15))#X轴刻度设定 每15天标一个日期
graph_KDJ.set_xticklabels([df_stockload.index.strftime('%Y-%m-%d')[index] for index in graph_KDJ.get_xticks()])#标签设置为日期

''' 绘制KDJ '''

#X-轴每个ticker标签都向右倾斜45度 

for label in graph_KAV.xaxis.get_ticklabels():   
	#label.set_rotation(45)
	#label.set_fontsize(10)#设置标签字体
	label.set_visible(False)

for label in graph_VOL.xaxis.get_ticklabels():   
	#label.set_rotation(45)
	#label.set_fontsize(10)#设置标签字体
	label.set_visible(False)

for label in graph_MACD.xaxis.get_ticklabels():   
	#label.set_rotation(45)
	#label.set_fontsize(10)#设置标签字体
	label.set_visible(False)
		
for label in graph_KDJ.xaxis.get_ticklabels():   
	label.set_rotation(45)
	label.set_fontsize(10)#设置标签字体

plt.show()
