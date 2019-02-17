#! /usr/bin/env python 
#-*- encoding: utf-8 -*- 
#author pythontab.com 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec#分割子图
#import mpl_finance as mpf #替换 import matplotlib.finance as mpf
import matplotlib.finance as mpf
import pandas as pd
import pandas_datareader.data as web
import datetime
import talib
#import tushare as ts#cmd /k C:\Python27.15\python.exe "$(FULL_CURRENT_PATH)" & PAUSE & EXIT 更改为2.7.15下运行

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
fig.subplots_adjust(left=0.09,bottom=0.20, right=0.94,top=0.90, wspace=0.2, hspace=0)
graph_KAV = fig.add_subplot(1,1,1)#创建子图


""" 绘制K线图 """
#方法1
ohlc = []
ohlc = list(zip(np.arange(0,len(df_stockload.index)),df_stockload.Open,df_stockload.Close,df_stockload.High,df_stockload.Low))#使用zip方法生成数据列表 
#mpf.candlestick_ochl(graph_KAV, ohlc, width=0.2, colorup='r', colordown='g', alpha=1.0)#绘制K线走势 Python3.7.1
mpf.candlestick(graph_KAV, ohlc, width=0.2, colorup='r', colordown='g', alpha=1.0)#绘制K线走势 Python2.7.5
#方法2
#mpf.candlestick2_ochl(graph_KAV, df_stockload.Open,df_stockload.Close,df_stockload.High,df_stockload.Low, width=0.5, colorup='r', colordown='g')#绘制K线走势 Python3.7.1

""" 绘制K线图 """

""" 绘制移动平均线图 """

df_stockload['Ma20'] = pd.rolling_mean(df_stockload.Close,window=20)#df_stockload.Close.rolling(window=20).mean()
df_stockload['Ma30'] = pd.rolling_mean(df_stockload.Close,window=30)#df_stockload.Close.rolling(window=30).mean()
df_stockload['Ma60'] = pd.rolling_mean(df_stockload.Close,window=60)#df_stockload.Close.rolling(window=60).mean()

numt = np.arange(0, len(df_stockload.index))

#绘制收盘价走势    
graph_KAV.plot(numt, df_stockload['Ma20'],'black', label='M20',lw=1.0)
graph_KAV.plot(numt, df_stockload['Ma30'],'green',label='M30', lw=1.0)
graph_KAV.plot(numt, df_stockload['Ma60'],'blue',label='M60', lw=1.0)		
graph_KAV.legend(loc='best')
""" 绘制移动平均线图 """

#fig.suptitle('600797 浙大网新', fontsize = 14, fontweight='bold')
graph_KAV.set_title(u"600797 浙大网新-日K线")
graph_KAV.set_xlabel(u"日期")
graph_KAV.set_ylabel(u"价格")
graph_KAV.set_xlim(0,len(df_stockload.index)) #设置一下x轴的范围
graph_KAV.set_xticks(range(0,len(df_stockload.index),15))#X轴刻度设定 每15天标一个日期
graph_KAV.grid(True,color='k')
graph_KAV.set_xticklabels([df_stockload.index.strftime('%Y-%m-%d')[index] for index in graph_KAV.get_xticks()])#标签设置为日期

for label in graph_KAV.xaxis.get_ticklabels():   
	label.set_rotation(45)
	label.set_fontsize(10)#设置标签字体

""" 跳空缺口 基类"""   
"""
# 新版类继承派生实现方式
class JumpGap_Base:
    def __init__(self, stock_dat):
        self.stock_dat = stock_dat

        self.jump_pd = pd.DataFrame()
        self.stock_dat['changeRatio'] = self.stock_dat.Close.pct_change()*100#计算涨/跌幅 (今收-昨收)/昨收*100% 判断向上跳空缺口/向下跳空缺口
        self.stock_dat['preClose'] = self.stock_dat.Close.shift(1) #增加昨收序列

    def CaljumpGap(self):
        jump_threshold = self.stock_dat.Close.median()*0.01 #跳空阈值 收盘价中位数*0.01
        
        for kl_index in np.arange(0, self.stock_dat.shape[0]):
            today = self.stock_dat.ix[kl_index]#若版本提示已经弃用 可使用loc或iloc替换  
            
            if (today.changeRatio > 0) and ((today.Low-today.preClose) > jump_threshold):
            #向上跳空 (今最低-昨收)/阈值
                today['jump_power'] = (today.Low-today.preClose)/jump_threshold
                #self.DrawjumpGap('up',kl_index,today)
                self.jump_pd = self.jump_pd.append(today)      
            elif (today.changeRatio < 0) and ((today.preClose-today.High) > jump_threshold):
            #向下跳空 (昨收-今最高)/阈值
                today['jump_power'] = (today.High-today.preClose)/jump_threshold
                #self.DrawjumpGap('down',kl_index,today) 
                self.jump_pd = self.jump_pd.append(today)   
                
        print(self.jump_pd.filter(['jump_power','preClose','changeRatio','Close','Volume']))#按顺序只显示该列            
    
        return self.jump_pd

class draw_annotate:    
    def __init__(self, draw_obj):    
        self.am = draw_obj
    def draw_jumpgap(self,stockdat,jump_pd): 
        ''' 绘制跳空缺口 '''        
        for kl_index in np.arange(0, jump_pd.shape[0]):
            today = jump_pd.ix[kl_index]#若版本提示已经弃用 可使用loc或iloc替换 
            inday = stockdat.index.get_loc(jump_pd.index[kl_index])
            if today['jump_power']  > 0:  
                self.am.annotate('up',xy=(inday,today.Low*0.95),xytext=(inday, today.Low*0.9),arrowprops=dict(facecolor='red',shrink=0.1),horizontalalignment='left',verticalalignment='top')
            elif today['jump_power']  < 0:  
                self.am.annotate('down',xy=(inday,today.High*1.05),xytext=(inday, today.High*1.1),arrowprops=dict(facecolor='green',shrink=0.1),horizontalalignment='left',verticalalignment='top')
  
class JumpGap_Redef(JumpGap_Base):
    def __init__(self, stock_dat, draw_obj):    
        JumpGap_Base.__init__(self, stock_dat)     
        self.draw_way = draw_obj
    
    def filtjumpGap(self):
        #self.CaljumpGap()
        self.jump_pd = self.jump_pd[(np.abs(self.jump_pd.changeRatio) > 3)&(self.jump_pd.Volume > self.jump_pd.Volume.median())]#abs取绝对值
        
        print(self.jump_pd.filter(['jump_power','preClose','changeRatio','Close','Volume']))#按顺序只显示该列
        return self.jump_pd
        
    def DrawjumpGap(self):  
        self.draw_way.draw_jumpgap(self.stock_dat,self.jump_pd)

    
app_jumpd = JumpGap_Redef(df_stockload,draw_annotate(graph_KAV))
app_jumpd.CaljumpGap()
app_jumpd.filtjumpGap()
app_jumpd.DrawjumpGap() 
"""

""" 检测跳空缺口 """
""" 
# 以前粗暴实现方式
jump_pd = pd.DataFrame()    
df_stockload['changeRatio'] = df_stockload.Close.pct_change()*100#计算涨/跌幅 (今收-昨收)/昨收*100% 判断向上跳空缺口/向下跳空缺口
df_stockload['preClose'] = df_stockload.Close.shift(1) #增加昨收序列
jump_threshold = df_stockload.Close.median()*0.01 #跳空阈值 收盘价中位数*0.01

for kl_index in np.arange(0, df_stockload.shape[0]):
    today = df_stockload.ix[kl_index]#若版本提示已经弃用 可使用loc或iloc替换  
    
    if (today.changeRatio > 0) and ((today.Low-today.preClose) > jump_threshold):
    #向上跳空 (今最低-昨收)/阈值
        today['jump_power'] = (today.Low-today.preClose)/jump_threshold
        jump_pd = jump_pd.append(today)
        graph_KAV.annotate('up',xy=(kl_index,today.Low-0.2),xytext=(kl_index, today.Low-1),arrowprops=dict(facecolor='red',shrink=0.1),horizontalalignment='left',verticalalignment='top')

    elif (today.changeRatio < 0) and ((today.preClose-today.High) > jump_threshold):
    #向下跳空 (昨收-今最高)/阈值
        today['jump_power'] = (today.High-today.preClose)/jump_threshold
        jump_pd = jump_pd.append(today)
        graph_KAV.annotate('down',xy=(kl_index,today.High+0.2),xytext=(kl_index, today.High+1),arrowprops=dict(facecolor='green',shrink=0.1),horizontalalignment='left',verticalalignment='top')

        
jump_pd = jump_pd[(np.abs(jump_pd.changeRatio) > 2)&(jump_pd.Volume > jump_pd.Volume.median())]#abs取绝对值
format = lambda x: '%.2f' % x
jump_pd = jump_pd.applymap(format)#处理后数据为str

print(jump_pd.filter(['jump_power','preClose','changeRatio','Close','Volume']))#按顺序只显示该列
"""
""" 检测跳空缺口 """    



""" 显示均线金叉/死叉提示符 """    

#显示均线金叉/死叉提示符
list_diff = np.sign(df_stockload['Ma20']-df_stockload['Ma60'])
list_signal = np.sign(list_diff-list_diff.shift(1))

#print("list_diff",list_diff)
#list_signal = list_signal[list_signal !=0]
#list_signal = list_signal.dropna(axis=0,how='any')#去除NA值
#print("list_signal",list_signal)

#循环方式实现
for i in range(len(list_signal)):
    if list_signal[i] < 0:
        graph_KAV.annotate(u"死叉", xy=(i, df_stockload['Ma20'][i]), xytext=(i, df_stockload['Ma20'][i]+1.5),
                         arrowprops=dict(facecolor='green', shrink=0.2))
        print(df_stockload.iloc[i])
    if list_signal[i] > 0:
        graph_KAV.annotate(u"金叉", xy=(i, df_stockload['Ma20'][i]), xytext=(i, df_stockload['Ma20'][i]-1.5),
                         arrowprops=dict(facecolor='red', shrink=0.2))
        print(df_stockload.iloc[i])

""" 显示均线金叉/死叉提示符 """    

plt.show()
