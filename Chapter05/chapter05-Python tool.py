#! /usr/bin/env python 
#-*- encoding: utf-8 -*- 
#author pythontab.com 

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#3、继承、派生和组合的应用
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#定义类ParentClass1
class ParentClass1: 
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        print('speak ParentClass1')

#建立另外一个类SubClass1 继承ParentClass1        
class SubClass1(ParentClass1): 
    def __init__(self, name, age, country):
        ParentClass1.__init__(self, name, age)     
        self.country = country    
    #新增write()方法
    def write(self):
        print('write SubClass1')

b1 = SubClass1('jack', 21, 'China')  
#SubClass1包含了ParentClass1所有的属性
print(b1.name) #结果为：jack
print(b1.age)  #结果为：21
print(b1.country) #结果为： China
b1.speak() #结果为： test ParentClass1
b1.write()  #结果为： test SubClass1'

#例程代码
#定义类ParentClass1
class ParentClass1: 
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def speak(self):
        print('speak ParentClass1')
        
#定义类ParentClass2
class ParentClass2: 
    def walk(self):
        print('walk ParentClass2')

#子类SubClass2继承ParentClass1和ParentClass2两个类        
class SubClass2(ParentClass1,ParentClass2): 
    def __init__(self, name, age, country):
        ParentClass1.__init__(self, name, age)     
        self.country = country          
#SubClass2包含了ParentClass1和ParentClass2所有的属性
b2 = SubClass2('jack', 21, 'China')
b2.speak()	 #结果为：speak ParentClass1
b2.walk() 	 #结果为：walk ParentClass2

""" 跳空缺口 基类"""   
class JumpGap_Base:
    def __init__(self, stock_dat):
        self.stock_dat = stock_dat
        self.jump_pd = []#跳空缺口
        
    def CaljumpGap(self):
        print("Calculating Gap")
        return self.jump_pd
"""
# 新版类继承派生实现方式
class JumpGap_Redef(JumpGap_Base):
    def __init__(self, stock_dat, draw_obj):    
        JumpGap_Base.__init__(self, stock_dat)     
    
    def filtjumpGap(self):
        print("filter Gap")
        self.jump_pd = self.jump_pd[(np.abs(self.jump_pd.changeRatio) > 3)&(self.jump_pd.Volume > self.jump_pd.Volume.median())]#过滤缺口
        return self.jump_pd
"""
# 新版类组合实现方式
class JumpGap_Redef(JumpGap_Base):
    def __init__(self, stock_dat, draw_obj):    
        JumpGap_Base.__init__(self, stock_dat)     
        self.draw_way = draw_obj
        
    def filtjumpGap(self):
        print("filter Gap")
        self.jump_pd = self.jump_pd[(np.abs(self.jump_pd.changeRatio) > 3)&(self.jump_pd.Volume > self.jump_pd.Volume.median())]#过滤缺口
        return self.jump_pd

    def DrawjumpGap(self):  
        self.draw_way.draw_jumpgap(self.stock_dat,self.jump_pd)
        
        
class draw_annotate:    
    def __init__(self, draw_obj):    
        self.am = draw_obj
    def draw_jumpgap(self,stockdat,jump_pd):   
        print("draw Gap")#绘制跳空缺口   

        
#创建人类
class Human: 
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def speak(self):
        print('Human speak skill')
#创建电脑类
class Computer:
    def __init__(self, model ,brand):
        self.model=model
        self.brand=brand
        
#程序员继承人类的属性
class Programmer(Human):  
    def __init__(self, name, age, country, computer):
        Human.__init__(self, name, age)    
        self.country = country          
        self.computer = computer
        
#程序员增加电脑属性 
b3=Programmer('jack', 21, 'China',Computer('X10','dell'))
print(b3.computer.model,b3.computer.brand) #结果为：('X10','dell')
