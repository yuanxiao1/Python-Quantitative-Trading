#! /usr/bin/env python 
#-*- encoding: utf-8 -*- 
#author pythontab.com 
import wx
import wx.adv
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
import talib
import csv,os
import codecs

from RedefPanelMod import MPL_Panel_Base,Loop_Panel_Base
from StockDataMod import GetStockDatPro
from IndicatStrateMod import Excave_Indic_Base, QuantPickTimeSys,FactorPickStockAng

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

class UserDialog(wx.Dialog):# user-defined

    def __init__(self,parent,text):
        wx.Dialog.__init__(self,parent,-1,u"选股提示",size=(400,500),style=wx.CAPTION|wx.CLOSE_BOX|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        pstock_Text = wx.StaticText(self, -1, u'选股策略筛选结果') 
        pstock_Text.SetFont(wx.Font(18,wx.DEFAULT,wx.NORMAL,wx.BOLD))
        pstock_sure = wx.TextCtrl(self, -1, "角度值:\n",size=(350,300),style = wx.TE_MULTILINE|wx.TE_READONLY)#多行|只读
        pstock_sure.SetFont(wx.Font(10,wx.DEFAULT,wx.NORMAL,wx.BOLD))

        okbtn = wx.Button(self,wx.ID_OK,u"确认")
        okbtn.SetDefault()
       
        sizer.Add(pstock_Text,flag=wx.ALIGN_CENTER)
        sizer.Add(pstock_sure,flag=wx.ALIGN_CENTER)
        sizer.Add(okbtn,flag=wx.ALIGN_CENTER)       
        self.SetSizer(sizer)
        for i in text:pstock_sure.AppendText(i)
    
        
class Frame(wx.Frame):   
    def __init__(self):   
        wx.Frame.__init__(self, parent = None, title = u'量化软件', size=(1500,800),   
                      style=wx.DEFAULT_FRAME_STYLE^wx.MAXIMIZE_BOX)   
        #创建显示区面板
        self.DispPanel = MPL_Panel_Base(self)
        self.BackPanel = Loop_Panel_Base(self)
        self.am = self.DispPanel.am
        self.vol = self.DispPanel.vol
        self.devol = self.DispPanel.devol
        self.macd = self.DispPanel.macd        
        
        #创建参数区面板
        self.ParaPanel = wx.Panel(self,-1)
        
        paraInput_Box = wx.StaticBox(self.ParaPanel, -1, u'参数输入') 
        paraInput_Sizer = wx.StaticBoxSizer(paraInput_Box, wx.VERTICAL)    
        self.StNameCodedict = {u"开山股份":"300257.SZ",u"浙大网新":"600797.SS",u"水晶光电":"002273.SZ", u"高鸿股份":"000851.SZ"}
        
        #初始化股票代码变量
        self.stockName_Val = u"开山股份"
        self.stockCode_Val = self.StNameCodedict[self.stockName_Val]
        
        self.stockName_CMBO = wx.ComboBox(self.ParaPanel, -1,self.stockName_Val, choices = list(self.StNameCodedict.keys()), style = wx.CB_READONLY|wx.CB_DROPDOWN) #股票名称
        stockCode_Text = wx.StaticText(self.ParaPanel, -1, u'股票名称') 

       #策略选取
        strate_Text = wx.StaticText(self.ParaPanel, -1, u'策略名称') 
        strate_Combo_Val = [u"双趋势融合", u"阿尔法", u"布林带"]
        self.pickstrate_Val = u"双趋势融合"
        self.pickstrate_CMBO = wx.ComboBox(self.ParaPanel, -1, self.pickstrate_Val, choices = strate_Combo_Val, style = wx.CB_READONLY|wx.CB_DROPDOWN) #策略名称        

        #日历控件选择数据周期
        #self.dpcEndTime = wx.DatePickerCtrl(self.ParaPanel, -1,style = wx.DP_DROPDOWN|wx.DP_SHOWCENTURY|wx.DP_ALLOWNONE)#结束时间
        #self.dpcStartTime = wx.DatePickerCtrl(self.ParaPanel, -1,style = wx.DP_DROPDOWN|wx.DP_SHOWCENTURY|wx.DP_ALLOWNONE)#起始时间
        self.dpcEndTime = wx.adv.DatePickerCtrl(self.ParaPanel, -1,style = wx.adv.DP_DROPDOWN|wx.adv.DP_SHOWCENTURY|wx.adv.DP_ALLOWNONE)#结束时间
        self.dpcStartTime = wx.adv.DatePickerCtrl(self.ParaPanel, -1,style = wx.adv.DP_DROPDOWN|wx.adv.DP_SHOWCENTURY|wx.adv.DP_ALLOWNONE)#起始时间

        DateTimeNow = wx.DateTime.Now()#wx.DateTime格式"03/03/18 00:00:00"

        self.dpcEndTime.SetValue(DateTimeNow)
        #DateTimeNow.SetYear(DateTimeNow.Year-1)
        DateTimeNow.SetYear(DateTimeNow.year - 1)
        self.dpcStartTime.SetValue(DateTimeNow)
        stockData_Text = wx.StaticText(self.ParaPanel, -1, u'日期(Start-End)')
        
        #初始化时间变量
        dateVal = self.dpcStartTime.GetValue() 
        self.stockSdate_Val = datetime.datetime(dateVal.year,dateVal.month+1,dateVal.day)
        dateVal = self.dpcEndTime.GetValue() 
        self.stockEdate_Val = datetime.datetime(dateVal.year,dateVal.month+1,dateVal.day)

        paraInput_Sizer.Add(stockCode_Text,proportion=0,flag=wx.EXPAND|wx.ALL,border=2)
        paraInput_Sizer.Add(self.stockName_CMBO, 0, wx.EXPAND|wx.ALL|wx.CENTER, 2)
        paraInput_Sizer.Add(stockData_Text,proportion=0,flag=wx.EXPAND|wx.ALL,border=2)
        paraInput_Sizer.Add(self.dpcStartTime, 0, wx.EXPAND|wx.ALL|wx.CENTER, 2) 
        paraInput_Sizer.Add(self.dpcEndTime, 0, wx.EXPAND|wx.ALL|wx.CENTER, 2) 
        paraInput_Sizer.Add(strate_Text, 0, wx.EXPAND|wx.ALL|wx.CENTER, 2)
        paraInput_Sizer.Add(self.pickstrate_CMBO, 0, wx.EXPAND|wx.ALL|wx.CENTER, 2)
        
        RadioList = ["不显示","跳空缺口", "金叉/死叉", "N日突破"] 
        self.StratInputBox = wx.RadioBox(self.ParaPanel, -1, label=u'指标提示', choices=RadioList,majorDimension = 4, style = wx.RA_SPECIFY_ROWS) 
        self.StratInputBox.Bind(wx.EVT_RADIOBOX,self.OnRadioBox_Indicator) 
        #初始化指标变量
        self.IndicatInput_Val = self.StratInputBox.GetStringSelection()  
        
        self.TextAInput = wx.TextCtrl(self.ParaPanel, -1, "交易信息提示:", style = wx.TE_MULTILINE|wx.TE_READONLY)#多行|只读

        vboxnetA = wx.BoxSizer(wx.VERTICAL)#纵向box 
        vboxnetA.Add(paraInput_Sizer,proportion=0,flag=wx.EXPAND|wx.BOTTOM,border=2) #proportion参数控制容器尺寸比例
        vboxnetA.Add(self.StratInputBox,proportion=0,flag=wx.EXPAND|wx.BOTTOM,border=2)         
        vboxnetA.Add(self.TextAInput,proportion=1,flag=wx.EXPAND|wx.ALL,border=2) 
        self.ParaPanel.SetSizer(vboxnetA)
        
        #创建Right面板
        self.CtrlPanel = wx.Panel(self,-1) 
        #创建FlexGridSizer布局网格
        self.FlexGridSizer=wx.FlexGridSizer(rows=3, cols=1, vgap=3, hgap=3)  
        
        #行情按钮
        self.Firmoffer = wx.Button(self.CtrlPanel,-1,"行情")
        self.Firmoffer.Bind(wx.EVT_BUTTON,self.FirmEvent)#绑定行情按钮事件  
        #选股按钮
        self.Stockpick = wx.Button(self.CtrlPanel,-1,"选股")  
        self.Stockpick.Bind(wx.EVT_BUTTON,self.PstockpEvent)#绑定选股按钮事件
        #回测按钮  
        self.Backtrace = wx.Button(self.CtrlPanel,-1,"回测")  
        self.Backtrace.Bind(wx.EVT_BUTTON,self.BackEvent)#绑定回测按钮事件
         
        #加入Sizer中  
        self.FlexGridSizer.Add(self.Firmoffer,proportion = 1, border = 5,flag = wx.ALL | wx.EXPAND)  
        self.FlexGridSizer.Add(self.Stockpick,proportion = 1, border = 5,flag = wx.ALL | wx.EXPAND)  
        self.FlexGridSizer.Add(self.Backtrace,proportion = 1, border = 5,flag = wx.ALL | wx.EXPAND) 
        self.FlexGridSizer.SetFlexibleDirection(wx.BOTH)  
        
        self.CtrlPanel.SetSizer(self.FlexGridSizer)  
        
        self.HBoxPanel = wx.BoxSizer(wx.HORIZONTAL)
        self.HBoxPanel.Add(self.ParaPanel,proportion = 1.5, border = 2,flag = wx.EXPAND|wx.ALL) 
        self.HBoxPanel.Add(self.DispPanel,proportion = 8, border = 2,flag = wx.EXPAND|wx.ALL )         
        self.HBoxPanel.Add(self.CtrlPanel,proportion = 1, border = 2,flag = wx.EXPAND|wx.ALL ) 
        self.SetSizer(self.HBoxPanel)    

    def ProcessStock(self):         
        #df_stockload = web.DataReader("600797.SS", "yahoo", datetime.datetime(2017,1,1), datetime.date.today())
        df_stockload = GetStockDatPro(self.stockCode_Val,self.stockSdate_Val, self.stockEdate_Val)

        """ 绘制移动平均线图 """
        #self.am.plot(self.numic[0:self.butNum],self.close[0:self.butNum],'#0f0ff0',linewidth=1.0)
        
        dispCont_List = []

        examp_trade= Excave_Indic_Base()
        if self.IndicatInput_Val == u"金叉/死叉":  
            dispCont_pd,dispCont_List = examp_trade.plot_Aver_Cross(df_stockload)
            self.DispPanel.draw_avercross(df_stockload,dispCont_pd)
        elif self.IndicatInput_Val == u"跳空缺口":
            dispCont_pd,dispCont_List = examp_trade.plot_Jump_Thrd(df_stockload)
            self.DispPanel.draw_jumpgap(df_stockload,dispCont_pd)
        elif self.IndicatInput_Val == u"N日突破":
            dispCont_pd,dispCont_List = examp_trade.plot_Ndays_Break(df_stockload)
            self.DispPanel.draw_ndaysbreak(df_stockload,dispCont_pd)
        else:
            dispCont_List = dispCont_List
            
        self.TextAInput.SetValue(u"指标提示信息如下:"+'\n')
        for i in dispCont_List:self.TextAInput.AppendText(i)

        numic = np.arange(0,len(df_stockload.index))
        butNum = len(df_stockload.index)
        self.DispPanel.xylabel_tick_lim(self.stockName_Val,df_stockload.index)
        self.DispPanel.draw_subgraph(df_stockload,numic)

    def ProcessLoop(self): 

        df_stockload = GetStockDatPro(self.stockCode_Val,self.stockSdate_Val, self.stockEdate_Val)
        dispCont_List = []
        if self.pickstrate_Val == u"双趋势融合":  
            #多趋势融合策略执行 """
            examp_trade= QuantPickTimeSys(df_stockload)
            dispCont_List = examp_trade.run_factor_plot(self.BackPanel.trade,self.BackPanel.total,self.BackPanel.profit)           
        else:
            #执行其他策略
            pass    
            
        self.TextAInput.SetValue(u"策略提示信息如下:"+'\n')
        for i in dispCont_List:self.TextAInput.AppendText(i)
        self.BackPanel.xylabel_tick_lim(self.stockName_Val)
        
    def reFlashLoop(self): 
        self.BackPanel.clear_subgraph()#必须清理图形才能显示下一幅图
        self.ProcessLoop()
        self.BackPanel.update_subgraph()#必须刷新才能显示下一幅图 

    def reFlashFrame(self): 
        self.DispPanel.clear_subgraph()#必须清理图形才能显示下一幅图
        self.ProcessStock()
        self.DispPanel.update_subgraph()#必须刷新才能显示下一幅图 
        
    def FirmEvent(self,event):
        #显示行情面板
        self.HBoxPanel.Hide(self.BackPanel)
        self.HBoxPanel.Replace(self.BackPanel,self.DispPanel)
        self.HBoxPanel.Show(self.DispPanel)
        #self.HBoxPanel.Remove(self.BackPanel)
        self.SetSizer(self.HBoxPanel)  
        self.HBoxPanel.Layout()    
    
        #获取列表股票代码和起始时间
        self.stockName_Val = self.stockName_CMBO.GetString(self.stockName_CMBO.GetSelection())
        self.stockCode_Val = self.StNameCodedict[self.stockName_Val]

        dateVal = self.dpcStartTime.GetValue() 
        self.stockSdate_Val = datetime.datetime(dateVal.year,dateVal.month+1,dateVal.day)
        dateVal = self.dpcEndTime.GetValue() 
        self.stockEdate_Val = datetime.datetime(dateVal.year,dateVal.month+1,dateVal.day)

        self.reFlashFrame()
 
    def BackEvent(self,event):       
        #显示回测面板
        self.HBoxPanel.Hide(self.DispPanel)
        self.HBoxPanel.Replace(self.DispPanel,self.BackPanel)
        self.HBoxPanel.Show(self.BackPanel)
        #self.HBoxPanel.Remove(self.DispPanel)
        self.SetSizer(self.HBoxPanel)  
        self.HBoxPanel.Layout()

        #获取策略名称
        self.pickstrate_Val = self.pickstrate_CMBO.GetString(self.pickstrate_CMBO.GetSelection())
        self.reFlashLoop()
        
    def PstockpEvent(self,event):
        dispCont_List = []
        """ 选股策略执行 """
        examp_trade= FactorPickStockAng()
        for index, stockName in enumerate(self.StNameCodedict.keys()) : 
            print("stockName",stockName,self.StNameCodedict[stockName])
            df_stockload = GetStockDatPro(self.StNameCodedict[stockName],self.stockSdate_Val, self.stockEdate_Val)
            df_stockload.fillna(method='bfill',inplace=True)#后一个数据填充NAN1
            dispCont_List.append(stockName+'\n'+examp_trade.fit_pick(df_stockload.Close)+'\n')
        print(dispCont_List)
        """ 选股策略执行 """
        """ 自定义提示框 """
        myPickStock = UserDialog(self,dispCont_List)    
        if myPickStock.ShowModal() == wx.ID_OK:
            pass 
        else:
            pass
        """ 自定义提示框 """

    def OnRadioBox_Indicator(self,event):  
        self.IndicatInput_Val = self.StratInputBox.GetStringSelection()

      
class App(wx.App):
    def OnInit(self):
        self.frame = Frame()  
        self.frame.ProcessStock()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True
    
if __name__ == '__main__':   
    app = App()
    app.MainLoop() 
 
