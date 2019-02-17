#! /usr/bin/env python 
#-*- encoding: utf-8 -*- 
#author pythontab.com 
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import datetime
import csv,os
import codecs
import talib

#获取股票数据接口
def GetStockDatApi(stockName=None,stockTimeS=None,stockTimeE=None):
    
    path = 'C:\programPY\GUI_Inter_StoMPL\StockData'
    
    str_stockTimeS = stockTimeS.strftime('%Y-%m-%d')
    str_stockTimeE = stockTimeE.strftime('%Y-%m-%d')
    newname = stockName+'+'+str_stockTimeS+'+'+str_stockTimeE+'.csv'
    newpath = os.path.join(path,newname)
    
    #path=os.path.abspath('.')#获取当前脚本所在的路径 C:\Program Files\Notepad++
    print(u"当前:%s" % os.getcwd())#当前工作目录
    os.chdir(path)
    print(u"修改为:%s" % os.getcwd())#修改后工作目录
   
    for filename in os.listdir(path):#遍历路径下所有文件
        #print(os.path.join(path,filename))

        if stockName in filename: 
            if filename.count('+') == 2:#存在CSV文件
                str_dfLoadTimeS = filename.split('+')[1]
                str_dfLoadTimeE = filename.split('+')[2].split('.')[0]

                dtm_dfLoadTimeS = datetime.datetime.strptime(str_dfLoadTimeS,'%Y-%m-%d') 
                dtm_dfLoadTimeE = datetime.datetime.strptime(str_dfLoadTimeE,'%Y-%m-%d')
                
                if((dtm_dfLoadTimeS - stockTimeS).days <= 0)and((dtm_dfLoadTimeE - stockTimeE).days >= 0):#起止日期在文件内则读取CSV文件获取数据
                    print("123",(dtm_dfLoadTimeS - stockTimeS).days)
                    print("345",(dtm_dfLoadTimeE - stockTimeE).days)
                    stockDat = pd.read_csv(os.path.join(path,filename),parse_dates=True,index_col=0,encoding='gb2312')
                    print(stockDat.head(),stockDat.tail())
                    stockDat = stockDat.loc[stockTimeS:stockTimeE]
                    print(stockDat.head(),stockDat.tail())
                else:#起止日期不相同则重新下载
                    stockDat = web.DataReader(stockName, "yahoo", stockTimeS, stockTimeE) 
                    os.rename(filename, newname)
                    stockDat.to_csv(newpath,columns=stockDat.columns,index=True)   
                return stockDat
            else:
                break

    stockDat = web.DataReader(stockName, "yahoo", stockTimeS, stockTimeE)  
    stockDat.to_csv(newpath,columns=stockDat.columns,index=True)   
    
    return stockDat

#处理股票数据接口
def GetStockDatPro(stockName=None,stockTimeS=None,stockTimeE=None):
        stockPro = GetStockDatApi(stockName, stockTimeS, stockTimeE)

        #处理移动平均线
        stockPro['Ma20'] = pd.rolling_mean(stockPro.Close,window=20)
        stockPro['Ma60'] = pd.rolling_mean(stockPro.Close,window=60)
        stockPro['Ma120'] = pd.rolling_mean(stockPro.Close,window=120)
        
        #处理MACD
        stockPro['macd_dif'],stockPro['macd_dea'], stockPro['macd_bar'] = talib.MACD(stockPro['Close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
 
        #处理KDJ
        xd = 9-1
        date = stockPro.index.to_series()
        RSV = pd.Series(np.zeros(len(date)-xd),index=date.index[xd:])
        Kvalue = pd.Series(0.0,index=RSV.index)
        Dvalue = pd.Series(0.0,index=RSV.index)
        Kvalue[0],Dvalue[0] = 50,50
        
        for day_ind in range(xd, len(date)):
            RSV[date[day_ind]] = (stockPro.Close[day_ind] - stockPro.Low[day_ind-xd:day_ind+1].min())/(stockPro.High[day_ind-xd:day_ind+1].max()-stockPro.Low[day_ind-xd:day_ind+1].min())*100
            if day_ind > xd:
                index = day_ind-xd
                Kvalue[index] = 2.0/3*Kvalue[index-1]+RSV[date[day_ind]]/3
                Dvalue[index] = 2.0/3*Dvalue[index-1]+Kvalue[index]/3
        stockPro['RSV'] = RSV
        stockPro['K'] = Kvalue
        stockPro['D'] = Dvalue
        stockPro['J'] = 3*Kvalue-2*Dvalue   
        return stockPro

      
