#! /usr/bin/env python 
#-*- encoding: utf-8 -*- 
#author pythontab.com 


#装饰器的剖析
#输出一个股票当天的收盘价字符串
#二层嵌套
"""
def log(func):
    def wrapper(*args, **kw):
        print('output %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper
    
"""
"""
@log    
def Stock_600213():
    print('2018-12-25:6.54')
#调用函数打印结果：
Stock_600213()
#2018-12-25:6.54
"""
"""
@log
def Stock_600213(Close):
    print('2018-12-25 {} :6.54'.format(Close))
#调用函数打印结果：
Stock_600213('Close')    
#2018-12-25 Close :6.54

"""

"""
#直接增加打印日志功能
def Stock_600213():
    print('output Stock_600213()')
    print('2018-12-25:6.54')
#调用函数打印结果：
Stock_600213()
#output Stock_600213():
#2018-12-25:6.54
"""

#三层嵌套
def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print '%s %s():' % (text, func.__name__)
            return func(*args, **kw)
        return wrapper
    return decorator

@log('Now Output')
def Stock_600213(Close):
    print('2018-12-25 {} :6.54'.format(Close))
#调用函数打印结果：
Stock_600213('Close')
print(Stock_600213.__name__) 
#Now Output Stock_600213():
#2018-12-25 Close :6.54

import functools
def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print '%s %s():' % (text, func.__name__)
            return func(*args, **kw)
        return wrapper
    return decorator

@log('Now Output')
def Stock_600213(Close):
    print('2018-12-25 {} :6.54'.format(Close))
#调用函数打印结果：
Stock_600213('Close')
print(Stock_600213.__name__) 
#Now Output Stock_600213():
#2018-12-25 Close :6.54
#Stock_600213
    

#装饰器讲解
class SelfPools(): 
    def __init__(self): 
        self.routes = {} 
    def route(self, route_str): 
        def decorator(f): 
            self.routes[route_str] = f
            return  f
        return decorator 

    def output(self, path): 
        view_function = self.routes.get(path) 
        if view_function:
            print u"输出[%s]板块股票:" % path
            for str in view_function():
                print(str)             
            return
        else: 
            raise ValueError('Route "{}"" has not been registered'.format(path)) 
				
app = SelfPools() 

@app.route(u"5G") 
def Stock_pool(): 
    stock_name = [u"600776:东方通信",u"002792:通宇通信",u"002268:卫士通",u"300698:万马科技"]
    return stock_name
    
@app.route(u"量子通信") 
def Stock_pool(): 
    stock_name = [u"600746:中国海防",u"002126:银轮股份",u"600522:中天科技",u"600468:百利电气"]
    return stock_name
     
app.output(u"5G")
#输出[5G]板块股票:
#600776:东方通信
#002792:通宇通信
#002268:卫士通
#300698:万马科技
app.output(u"量子通信")
#输出[量子通信]板块股票:
#600746:中国海防
#002126:银轮股份
#600522:中天科技
#600468:百利电气
