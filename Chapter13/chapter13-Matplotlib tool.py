#! /usr/bin/env python 
#-*- encoding: utf-8 -*- 
#author pythontab.com 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt#(1)
from matplotlib.figure import Figure

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

#基础数据
y_value = np.random.randn(200)
x_value = np.arange(200)

ylim_min = y_value.min()-1
ylim_max = y_value.max()+1

yticks_min = y_value.min()+0.5
yticks_max = y_value.max()-0.5
ylim_setp = (yticks_max - yticks_min)/2.1
#基础数据
"""
#函数式编程
plt.xlim(0,len(x_value))#注释(2)
plt.ylim(ylim_min,ylim_max)#注释(2)
plt.xticks(np.arange(0,len(x_value),20),['2015-02-01','2015-03-01','2015-04-02','2015-05-02','2015-06-02','2015-07-02','2015-08-02','2015-09-02','2015-10-02','2015-11-02'],rotation=45)#注释(3)
plt.yticks(np.arange(yticks_min,yticks_max,ylim_setp),[u'上限预警值',u'标准值',u'下限预警值'])#注释(3)
plt.title(u"函数式编程")#注释(4)
plt.xlabel(u"日期")#注释(5):
plt.ylabel(u"数值")  #注释(5):
plt.grid(True)#注释(6)
plt.legend(loc='best')#注释(7)
plt.plot(x_value,y_value,label=u"随机误差",ls='-',c='r',lw=1) #注释(8) 
plt.show()  
#函数式编程
"""

''' 对象式编程 '''
"""
fig = plt.figure()

#ax1 = fig.add_subplot(211)
ax1 = fig.add_axes([0.1, 0.1, 0.4, 0.3])

ax1.plot(x_value,y_value,label=u"随机误差",ls='-',c='r',lw=1)  
ax1.set_xlim(0,len(x_value))#调节X轴范围
ax1.set_ylim(ylim_min,ylim_max)#调节Y轴范围

ax1.set_xticks(np.arange(0,len(x_value),20))
ax1.set_yticks(np.arange(yticks_min,yticks_max,ylim_setp))
ax1.set_xticklabels(['2015-02-01','2015-03-01','2015-04-02','2015-05-02','2015-06-02','2015-07-02','2015-08-02','2015-09-02','2015-10-02','2015-11-02'],fontsize='small')
ax1.set_yticklabels([u'上限预警值',u'标准值',u'下限预警值'])
ax1.set_title(u"对象式编程子图1")
ax1.set_xlabel(u"日期")
ax1.set_ylabel(u"数值")

#ax2 = fig.add_subplot(212)
ax2 = fig.add_axes([0.5, 0.5, 0.4, 0.3])
ax2.plot(x_value,y_value,label=u"随机误差",ls='-',c='y',lw=1)      

ax2.set_xlim(0,len(x_value))#调节X轴范围
ax2.set_ylim(ylim_min,ylim_max)#调节Y轴范围

ax2.set_xticks(np.arange(0,len(x_value),20))
ax2.set_yticks(np.arange(yticks_min,yticks_max,ylim_setp))
ax2.set_xticklabels(['2015-02-01','2015-03-01','2015-04-02','2015-05-02','2015-06-02','2015-07-02','2015-08-02','2015-09-02','2015-10-02','2015-11-02'],rotation=45,fontsize='small')
ax2.set_yticklabels([u'上限预警值',u'标准值',u'下限预警值'])

ax2.set_title(u"对象式编程子图2")
ax2.set_xlabel(u"日期")
ax2.set_ylabel(u"数值")
plt.show()
"""
''' 对象式编程 '''


""" subplots 遍历显示图形"""
"""
fig_ps,axes_ps = plt.subplots(2,3)
print(axes_ps)
for i in range(2):
    for j in range(3):
        axes_ps[i,j].hist(np.random.randn(500),bins=50,color='k',alpha=0.5)
plt.show()
"""
""" subplots 遍历显示图形"""
""" Artist 对象测试"""

fig = plt.figure()
ax = fig.add_subplot(111)
line = ax.plot(x_value,y_value,label=u"随机误差",ls='-',c='r',lw=1)  
print("line",line)
print("ax.line",ax.lines)

plt.show()
"""
