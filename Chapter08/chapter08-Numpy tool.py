#! /usr/bin/env python 
#-*- encoding: utf-8 -*- 
#author pythontab.com 

import numpy as np#推荐引用方式
from timeit import timeit 

print(np.ones((10, 5)))
"""
[[ 1.  1.  1.  1.  1.]
 [ 1.  1.  1.  1.  1.]
 [ 1.  1.  1.  1.  1.]
 [ 1.  1.  1.  1.  1.]
 [ 1.  1.  1.  1.  1.]
 [ 1.  1.  1.  1.  1.]
 [ 1.  1.  1.  1.  1.]
 [ 1.  1.  1.  1.  1.]
 [ 1.  1.  1.  1.  1.]
 [ 1.  1.  1.  1.  1.]]
 """
print(np.ones((10, 5)).shape)
#(10, 5)
print(np.ones((10, 5)).dtype)
#float64
print(np.ones((10, 5)).strides)
#(40, 8)

#测试Numpy数组和等价的Python列表性能差距
my_arr = np.arange(1000000)
my_list = list(range(1000000))
t1 = timeit('for _ in range(10): my_arr2 = my_arr * 2','from __main__ import my_arr',number=1)
t2 = timeit('for _ in range(10): my_list2 = [x * 2 for x in my_list]','from __main__ import my_list',number=1)
print(t1,t2)

#矢量化运算
arrA = np.array([[1., 2., 3.], [4., 5., 6.]])
arrB = np.array([[2., 2., 2.], [2., 2., 2.]])
print(arrA)
"""
[[ 1.  2.  3.]
 [ 4.  5.  6.]]
"""
print(arrB)
"""
[[ 2.  2.  2.]
 [ 2.  2.  2.]]
"""
print(arrA * arrB)
"""
[[  2.   4.   6.]
 [  8.  10.  12.]]
"""
print(arrA * 2.0)
"""
[[  2.   4.   6.]
 [  8.  10.  12.]]
"""
arrA = np.array([[0., 0., 0.], [1., 1., 1.], [2., 2., 2.], [3., 3., 3.]])
print(arrA)
"""
[[ 0.  0.  0.]
 [ 1.  1.  1.]
 [ 2.  2.  2.]
 [ 3.  3.  3.]]
"""
print(arrA.shape)
#(4, 3)
arrB = np.array([1., 2., 3.])
print(arrB)
#[ 1.  2.  3.]
print(arrB.shape)
#(3,)
print(arrA+arrB)
"""
[[ 1.  2.  3.]
 [ 2.  3.  4.]
 [ 3.  4.  5.]
 [ 4.  5.  6.]]
"""

x = np.ones((4,1))
print(x)
y = np.ones((1,4,3))
print(y)
print(x+y)
#operands could not be broadcast together with shapes (2,1) (5,4,3)
"""
[[ 1.]
 [ 1.]
 [ 1.]
 [ 1.]]
[[[ 1.  1.  1.]
  [ 1.  1.  1.]
  [ 1.  1.  1.]
  [ 1.  1.  1.]]]
[[[ 2.  2.  2.]
  [ 2.  2.  2.]
  [ 2.  2.  2.]
  [ 2.  2.  2.]]]
"""
#data = np.random.randn(3, 4)

data = np.array([[ 0.81516464,0.54699707,0.25469129,-0.35725194],
 [-0.1594436,0.47096122,-0.51086806,-0.82336626],
 [-0.76274312,0.66010544,0.45585599,0.80401797]])
print(data)
"""
[[ 0.81516464  0.54699707  0.25469129 -0.35725194]
 [-0.1594436   0.47096122 -0.51086806 -0.82336626]
 [-0.76274312  0.66010544  0.45585599  0.80401797]]
[[ 0.81516464  0.54699707  0.25469129 -0.35725194]]
"""
print(data[[True, False, False]])
#[[ 0.81516464  0.54699707  0.25469129 -0.35725194]]
print(data[[True, False, False],1])
#[ 0.54699707]
print(data < 0)
"""
[[False False False  True]
 [ True False  True  True]
 [ True False False False]]
"""
print(data[data < 0])
#[-0.35725194 -0.1594436  -0.51086806 -0.82336626 -0.76274312]




