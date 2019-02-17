#! /usr/bin/env python 
#-*- encoding: utf-8 -*- 
#author pythontab.com 
import pandas as pd
import numpy as np
import datetime #存储CSV文件使用
#1、Pandas工具快速入门：数据生成和访问
#1.1Series数据生成和访问
print(u"**********************************1.1Series数据生成和访问************************************************")
#以列表作为数据类型创建一个Series对象
s = pd.Series([-1.55666192,-0.75414753,0.47251231,-1.37775038,-1.64899442], index=['a', 'b', 'c', 'd', 'e'])
print(s)
"""
#执行结果如下：
a   -1.556662
b   -0.754148
c    0.472512
d   -1.377750
e   -1.648994
dtype: float64
"""

#list数据包含数字和字符串
s = pd.Series(['a',-0.75414753,123,66666,-1.64899442], index=['a', 'b', 'c', 'd', 'e'],)
print(s)
"""
#执行结果如下：
a           a
b   -0.754148
c         123
d       66666
e    -1.64899
dtype: object
"""
#dtype指定int8类型
s = pd.Series([-1.55666192,-0.75414753,0.47251231,-1.37775038,-1.64899442], index=['a', 'b', 'c', 'd', 'e'],dtype='int8' )
print(s)
"""
#执行结果如下：
a   -1
b    0
c    0
d   -1
e   -1
dtype: int8
"""

#以ndarray作为数据类型创建一个Series对象
s = pd.Series(np.random.randn(5))
print(s)
"""
#执行结果如下：
0    0.485468
1   -0.912130
2    0.771970
3   -1.058117
4    0.926649
dtype: float64
"""

#指定的内容创建索引
s = pd.Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e'])
print(s)
"""
#执行结果如下：
a    0.485468
b   -0.912130
c    0.771970
d   -1.058117
e    0.926649
dtype: float64
"""

#以常量值作为数据创建一个Series对象
s = pd.Series(5., index=['a', 'b', 'c', 'd', 'e'])
print(s)
"""
#执行结果如下：
a    5.0
b    5.0
c    5.0
d    5.0
e    5.0
dtype: float64
"""

#以字典作为数据类型创建一个Series对象
s = pd.Series({'a' : 0., 'b' : 1., 'c' : 2.},index=['b', 'c', 'd', 'a'])
print(s)
"""
#执行结果如下：
b    1.0
c    2.0
d    NaN
a    0.0
dtype: float64
"""

#访问Series全部元素数值
print(s.values)
#执行结果：[  1.   2.  nan   0.]

#访问Series全部索引值
print(s.index)
#执行结果：Index([u'b', u'c', u'd', u'a'], dtype='object

#访问a索引的元素值
print(s['a'])
#执行结果：0.0

#访问a和b索引的元素值
print(s[['a','b']])
"""
#执行结果如下：
a    0.0
b    1.0
dtype: float64
"""
   
#访问a、b、c索引的元素值
print(s[['a','b','c']])
"""
#执行结果如下：
a    0.0
b    1.0
c    2.0
dtype: float64
"""
    
#访问前两个数据
print(s[:2])
"""
#执行结果如下：
b    1.0
c    2.0
dtype: float64
"""
print(u"**********************************1.1Series数据生成和访问************************************************")
print(u"*********************************************************************************************************")
print(u"*********************************************************************************************************")
print(u"**********************************1.2dataframe数据生成和访问************************************************")

#以列表组成的字典形式创建DataFrame
df = pd.DataFrame({'one': [1., 2., 3., 5], 'two': [1., 2., 3., 4.]})
print(df)
"""
#执行结果如下：
   one  two
0  1.0  1.0
1  2.0  2.0
2  3.0  3.0
3  5.0  4.0
"""
#以嵌套列表形式创建DataFrame
df = pd.DataFrame([[1., 2., 3., 5],[1., 2., 3., 4.]],index=['a', 'b'],columns=['one','two','three','four'])
print(df)
"""
#执行结果如下：
   one  two  three  four
a  1.0  2.0    3.0   5.0
b  1.0  2.0    3.0   4.0
"""
#创建一个二维ndarray阵列
data = np.zeros((2,), dtype=[('A', 'i4'),('B', 'f4'),('C', 'a10')])
print(data)
"""
#执行结果如下：
[(0,  0., '') (0,  0., '')]
"""
#以整数、浮点和字符串类型对data进行赋值
data[:] = [(1,2.,'Hello'), (2,3.,"World")]        
#二维ndarray形式创建DataFrame
df = pd.DataFrame(data)
print(df)
"""
#执行结果如下：
   A    B      C
0  1  2.0  Hello
1  2  3.0  World
"""
#指定行索引为['first', 'second']
df = pd.DataFrame(data, index=['first', 'second'])
print(df)
"""
#执行结果如下：
         A    B      C
first   1  2.0  Hello
second  2  3.0  World
"""
#指定列索引columns
df = pd.DataFrame(data, columns=['C', 'A', 'B'])
print(df)
"""
#执行结果如下：
        C  A    B
0  Hello  1  2.0
1  World  2  3.0
"""
#创建一组以Series组成的字典
data = {'one' : pd.Series([1., 2., 3.], index=['a', 'b', 'c']),
        'two' : pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
#以Series组成的字典形式创建DataFrame
df = pd.DataFrame(data)
print(df)
"""
#执行结果如下：
   one  two
a  1.0  1.0
b  2.0  2.0
c  3.0  3.0
d  NaN  4.0
"""
#创建一组字典的列表数据
data2 = [{'a': 1, 'b': 2}, {'a': 5, 'b': 10, 'c': 20}]
#字典的列表创建DataFrame
df = pd.DataFrame(data2)
print(df)
"""
#执行结果如下：
   a   b     c
0  1   2   NaN
1  5  10  20.0
"""

print(u"**********************************dataframe数据访问************************************************")
#创建一组以Series组成的字典
data = {'one' : pd.Series([1., 2., 3.], index=['a', 'b', 'c']),
        'two' : pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
#以Series组成的字典形式创建DataFrame
df = pd.DataFrame(data)
print(df)
"""
#执行结果如下：
   one  two
a  1.0  1.0
b  2.0  2.0
c  3.0  3.0
d  NaN  4.0
"""
print(df.loc['a'])
"""
#执行结果如下：
one    1.0
two    1.0
Name: a, dtype: float64
 """       
print(df.loc[:,['one','two'] ])
"""
#执行结果如下：
   one  two
a  1.0  1.0
b  2.0  2.0
c  3.0  3.0
d  NaN  4.0
"""
print(df.loc[['a',],['one','two']])
"""
#执行结果如下：
   one  two
a  1.0  1.0
"""
print(df.iloc[0:2,0:1])  
"""
#执行结果如下：
   one
a  1.0
b  2.0
"""
print(df.iloc[0:2])  
"""
#执行结果如下：
   one  two
a  1.0  1.0
b  2.0  2.0
"""
print(df.iloc[[0,2],[0,1]])
"""
#执行结果如下：
   one  two
a  1.0  1.0
c  3.0  3.0
"""

print(df.ix['a'])
"""
#执行结果如下：
one    1.0
two    1.0
Name: a, dtype: float64
"""
print(df.ix['a',['one','two']])
"""
#执行结果如下：
one    1.0
two    1.0
Name: a, dtype: float64
"""

print(df.ix['a',[0,1]])
"""
#执行结果如下：
one    1.0
two    1.0
Name: a, dtype: float64
"""

print(df.ix[['a','b'],[0,1]])
"""
#执行结果如下：
   one  two
a  1.0  1.0
b  2.0  2.0
"""
print(df.ix[df.one>1,:1])
"""
#执行结果如下：
   one
b  2.0
c  3.0
"""
print(u"**********************************1.2dataframe数据生成和访问************************************************")
print(u"*********************************************************************************************************")
print(u"*********************************************************************************************************")
