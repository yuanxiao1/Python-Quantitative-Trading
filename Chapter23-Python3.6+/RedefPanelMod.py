#! /usr/bin/env python 
#-*- encoding: utf-8 -*- 
#author pythontab.com 
import wx
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure  
import matplotlib.dates as mdates
import mpl_finance as mpf #替换 import matplotlib.finance as mpf
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.gridspec as gridspec#分割子图
import datetime

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

class MPL_Panel_Base(wx.Panel):  
    def __init__(self, parent):
        wx.Panel.__init__(self,parent=parent, id=-1)

        self.figure = Figure()
        gs = gridspec.GridSpec(4, 1, left=0.05, bottom=0.10, right=0.96, top=0.96, wspace=None, hspace=0.1, height_ratios=[3.5,1,1,1])
        self.am = self.figure.add_subplot(gs[0,:])
        self.vol = self.figure.add_subplot(gs[1,:])
        self.macd = self.figure.add_subplot(gs[2,:])
        self.devol = self.figure.add_subplot(gs[3,:])

        self.FigureCanvas = FigureCanvas(self, -1, self.figure)#figure加到FigureCanvas
        self.TopBoxSizer = wx.BoxSizer(wx.VERTICAL)  
        self.TopBoxSizer.Add(self.FigureCanvas,proportion = -1, border = 2,flag = wx.ALL | wx.EXPAND)  
        self.SetSizer(self.TopBoxSizer) 

    def draw_subgraph(self,stockdat,numt):  
    
        """ 绘制K线图 """
        ohlc = list(zip(np.arange(0,len(stockdat.index)),stockdat.Open,stockdat.Close,stockdat.High,stockdat.Low))#使用zip方法生成数据列表 
        #mpf.candlestick(self.am, ohlc, width=0.5, colorup='r', colordown='g')#绘制K线走势
        mpf.candlestick_ochl(self.am, ohlc, width=0.5, colorup='r', colordown='g')#绘制K线走势 py3.7
        ''' 绘制均线 '''    
        self.am.plot(numt, stockdat['Ma20'],'black', label='M20',lw=1.0)
        self.am.plot(numt, stockdat['Ma60'],'green',label='M60', lw=1.0)
        self.am.plot(numt, stockdat['Ma120'],'blue',label='M120', lw=1.0)
        self.am.legend(loc='best',shadow=True, fontsize ='10')
        ''' 绘制成交量 '''    
        self.vol.bar(numt, stockdat.Volume,color=['g' if stockdat.Open[x] > stockdat.Close[x] else 'r' for x in range(0,len(stockdat.index))])
        ''' 绘制MACD '''   
        #绘制BAR>0 柱状图
        bar_red = np.where(stockdat['macd_bar']>0, 2*stockdat['macd_bar'], 0)
        #绘制BAR<0 柱状图
        bar_green = np.where(stockdat['macd_bar']<0, 2*stockdat['macd_bar'], 0)        
        
        self.macd.plot(numt, stockdat['macd_dif'], 'red', label='macd dif') #dif    
        self.macd.plot(numt, stockdat['macd_dea'], 'blue', label='macd dea') #dea 
        self.macd.bar(numt, bar_red, facecolor='red',label='hist bar')
        self.macd.bar(numt, bar_green, facecolor='green',label='hist bar')
        self.macd.legend(loc='best',shadow=True, fontsize ='10')
        #legend = self.macd.legend(loc='best',shadow=True, fontsize ='10')
        #legend.get_frame().set_facecolor('#00FFCC')# Put a nicer background color on the legend.
        #legend.get_title().set_fontsize(fontsize = 20)
        ''' 绘制KDJ '''
        self.devol.plot(numt, stockdat['K'], 'blue', label='K') #K    
        self.devol.plot(numt, stockdat['D'], 'g--', label='D') #D
        self.devol.plot(numt, stockdat['J'], 'r-', label='J') #J         
        self.devol.legend(loc='best',shadow=True, fontsize ='10')

    def draw_jumpgap(self,stockdat,jump_pd):  
        ''' 绘制跳空缺口 '''        
        for kl_index in np.arange(0, jump_pd.shape[0]):
            today = jump_pd.ix[kl_index]#若版本提示已经弃用 可使用loc或iloc替换 
            inday = stockdat.index.get_loc(jump_pd.index[kl_index])
            if today['jump_power']  > 0:  
                self.am.annotate('up',xy=(inday,today.Low*0.95),xytext=(inday, today.Low*0.9),arrowprops=dict(facecolor='red',shrink=0.1),horizontalalignment='left',verticalalignment='top')
            elif today['jump_power']  < 0:  
                self.am.annotate('down',xy=(inday,today.High*1.05),xytext=(inday, today.High*1.1),arrowprops=dict(facecolor='green',shrink=0.1),horizontalalignment='left',verticalalignment='top')      
                
    def draw_avercross(self,stockdat,list_signal):  
        ''' 绘制金叉死叉 '''               
        for kl_index,signal_dat in enumerate(list_signal):   
            inday = stockdat.index.get_loc(list_signal.index[kl_index])
            if signal_dat < 0:
                self.am.annotate(u"死叉", xy=(inday, stockdat['Ma20'][inday]), xytext=(inday, stockdat['Ma20'][inday]+1.5),arrowprops=dict(facecolor='green', shrink=0.2))
            elif signal_dat > 0:
                self.am.annotate(u"金叉", xy=(inday, stockdat['Ma60'][inday]), xytext=(inday, stockdat['Ma60'][inday]-1.5),arrowprops=dict(facecolor='red', shrink=0.2))

    def draw_ndaysbreak(self,stockdat,list_signal):  
        ''' 绘制N日突破 '''               
        for kl_index in np.arange(0, stockdat.shape[0]):
            today = stockdat.ix[kl_index]
            """ 收盘价超过N2最低价 卖出股票持有"""
            if today['Close'] < today['N2_Low']:
                self.am.annotate(u"下突破", xy=(kl_index, stockdat['High'][kl_index]), xytext=(kl_index, stockdat['High'][kl_index]+1.5),arrowprops=dict(facecolor='green', shrink=0.2))
               
            """ 收盘价超过N1最高价 买入股票持有"""     
            if today['Close'] > today['N1_High']:
                self.am.annotate(u"上突破", xy=(kl_index, stockdat['Low'][kl_index]), xytext=(kl_index, stockdat['Low'][kl_index]-1.5),arrowprops=dict(facecolor='red', shrink=0.2))

    def update_subgraph(self):  
        #修改图形的任何属性后都必须使用self.updatePlot()更新GUI界面
        self.FigureCanvas.draw()  
        
    def clear_subgraph(self):  
        #再次画图前,必须调用该命令清空原来的图形  
        self.am.clear() 
        self.vol.clear()
        self.devol.clear()
        self.macd.clear()    
        #self.figure.set_canvas(self.FigureCanvas)  
        #self.updatePlot()
        
    def xylabel_tick_lim(self,title,dates):  
        # 设置X轴 Y轴的标签
        # 给图像添加一个标题   
        # 设置X轴的刻度大小 
        # 设置x轴的显示范围 

        self.devol.set_xlabel(u"时间")
        self.am.set_ylabel(u"日K线")
        self.vol.set_ylabel(u"成交量")
        self.devol.set_ylabel(u"KDJ")
        self.macd.set_ylabel(u"MACD")
        self.am.set_title(title)  
        dir(self.figure)
        
        major_tick = len(dates)
        self.am.set_xlim(0,major_tick) #设置一下x轴的范围
        self.vol.set_xlim(0,major_tick) #设置一下x轴的范围
        self.devol.set_xlim(0,major_tick) #设置一下x轴的范围
        self.macd.set_xlim(0,major_tick) #设置一下x轴的范围
        
        self.am.set_xticks(range(0,major_tick,15))#每五天标一个日期
        self.vol.set_xticks(range(0,major_tick,15))#每五天标一个日期
        self.devol.set_xticks(range(0,major_tick,15))#每五天标一个日期   
        self.macd.set_xticks(range(0,major_tick,15))#每五天标一个日期        
        self.devol.set_xticklabels([dates.strftime('%Y-%m-%d')[index] for index in self.devol.get_xticks()])#标签设置为日期
        
        for line in self.am.xaxis.get_ticklabels():#X-轴每个ticker标签隐藏
            line.set_visible(False)
        for line in self.vol.xaxis.get_ticklabels():#X-轴每个ticker标签隐藏
            line.set_visible(False)
        for line in self.macd.xaxis.get_ticklabels():#X-轴每个ticker标签隐藏
            line.set_visible(False)
        for label in self.devol.xaxis.get_ticklabels():   
            label.set_rotation(45)#X-轴每个ticker标签都向右倾斜45度
            label.set_fontsize(10)#设置标签字体
            
        self.am.grid(True,color='k')
        self.vol.grid(True,color='k')  
        self.macd.grid(True,color='k')
        self.devol.grid(True,color='k')  

class Loop_Panel_Base(wx.Panel):  
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=-1)
        self.figure = Figure()

        gs = gridspec.GridSpec(3, 1, left=0.05, bottom=0.10, right=0.96, top=0.96, wspace=None, hspace=0.1, height_ratios=[1.5,1,1])

        self.trade = self.figure.add_subplot(gs[0,:])
        self.total = self.figure.add_subplot(gs[1,:])
        self.profit = self.figure.add_subplot(gs[2,:])    

        self.FigureCanvas = FigureCanvas(self, -1, self.figure)#figure加到FigureCanvas
        self.TopBoxSizer = wx.BoxSizer(wx.VERTICAL)  
        self.TopBoxSizer.Add(self.FigureCanvas,proportion = -1, border = 2,flag = wx.ALL | wx.EXPAND)  
        self.SetSizer(self.TopBoxSizer) 

    def update_subgraph(self):  
        #修改图形的任何属性后都必须使用self.updatePlot()更新GUI界面
        self.FigureCanvas.draw()  
        
    def clear_subgraph(self):  
        #再次画图前,必须调用该命令清空原来的图形  
        self.trade.clear() 
        self.total.clear()
        self.profit.clear()
        
    def xylabel_tick_lim(self,title):  
        # 设置X轴 Y轴的标签
        # 给图像添加一个标题   
        # 设置X轴的刻度大小 
        # 设置x轴的显示范围 

        self.profit.set_xlabel(u"时间")
        self.trade.set_ylabel(u"交易区间")
        self.total.set_ylabel(u"资金收益")
        self.profit.set_ylabel(u"收益率对比")
        self.trade.set_title(title)  
         
        #self.trade.xticks([])  #去掉横坐标值        
        #self.total.xticks([])  #去掉横坐标值
        self.profit.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(1),interval=1))
        self.profit.xaxis.set_minor_formatter(mdates.DateFormatter('%d\n%a'))#标签设置为日期  

