#! /usr/bin/env python 
#-*- encoding: utf-8 -*- 
#author pythontab.com 

#2.变量类型及动态特性
#2.1变量类型的种类
#查看数值的类型  注：type()用于判断数据类型
print(type(123))   	#结果为：<class 'int'>
print(type(1.12))  	#结果为：<class 'float'>
print(type(3j + 1))  #结果为：<class 'complex'>
#查看数值的运算
print(1.0/3)         #结果为：0.3333333333333333
print(12.5*10)     #结果为：125.0
#查看数值变量的运算
a = 1
b = 3
print(a + b)      #结果为：4
print(a - b)      #结果为：-2
print(a * b)      #结果为：3
print(a / b)    #结果为：0
print(a % b)     #结果为：1
print(a ** b)     #结果为：1
print(a // b)     #结果为：0

#查看字符串常量
print('hello world!') #结果为：hello world!
print("hello world!") #结果为：hello world!
#查看字符串变量 
a = "hello world!"  
print(a) #结果为：hello world!

#创建列表变量
list1 = ['physics', 'chemistry', 1997, 2000]
list2 = [1, 2, 3, 4, 5, 6, 7 ]
#列表访问
print(list1[2])  	#结果为：1997
print(list2[1:5]) 	#结果为：[2, 3, 4, 5]
#列表二次赋值
list1[2] = 2001;
print(list1[2])   	#结果为：2001

#创建元组并初始化
name_1 = ("Madonna", "Cory", ["Annie", "Nelly"], "Cory")    
#元组访问
print(name_1)         #结果为：('Madonna', 'Cory', ['Annie', 'Nelly'], 'Cory')
print(name_1[1:3])    #结果为：('Cory', ['Annie', 'Nelly'])
print(name_1.index("Madonna"))  #结果为：0
print(len(name_1))   #结果为：4

#创建字典变量
math_score = {'Madonna': 89, 'Cory': 99, 'Annie': 65, 'Nelly': 89} 
print(math_score)   #{'Madonna': 89, 'Cory': 99, 'Annie': 65, 'Nelly': 89}
#字典访问
print(math_score['Madonna'])  #结果为：89

#2.2动态类型的特性 
#int 
i = 5
print(i)  		 #结果为：5
print(hex(id(i))) #结果为：0xa26f880
#重新创建值为6的int对象 
i += 1
print(i)  		 #结果为：6
print(hex(id(i))) #结果为：0xa26f874
#指向数值5的内存地址
j = 5 
print(j)		 #结果为：5
print(hex(id(j))) #结果为：0xa26f880

#float相同
i = 1.5
print(i)	#结果为：1.5
print(hex(id(i))) #结果为：0x9e86c8c

i += 1
print(i) #结果为：2.5
print(hex(id(i))) #结果为：0x9e86cac
 
j = 1.5
print(j) #结果为：1.5
print(hex(id(j))) #结果为：0x9e86c8c


#例程代码：
#list
i = [1, 2, 3]
print(i) 			#结果为：[1, 2, 3]
print(hex(id(i))) 	#结果为：0xb73fa1acL

#append后仍指向同一内存地址
i.append(4) 	
print(i) 		 #结果为：[1, 2, 3, 4]
print(hex(id(i))) #结果为：0xb73fa1acL

#j、k的值虽然相同，但指向的内存地址却不同
j = [1.5, 2.5, 3.5]
print(j) 	#结果为：[1.5, 2.5, 3.5]
print(hex(id(j)))  #结果为：0xb6fed06cL
k = [1.5, 2.5, 3.5]
print(k)  	#结果为：[1.5, 2.5, 3.5]
print(hex(id(k))) #结果为：0xb6fed04cL

#赋值语句让j、k指向同一个内存地址
j = k
print(j) #结果为：[1.5, 2.5, 3.5]
print(hex(id(j))) #结果为：0xb6fed04cL
print(k) #结果为：[1.5, 2.5, 3.5]
print(hex(id(k))) #结果为：0xb6fed04cL

#j、k任意一个list变量修改，会影响另外一个list变量的值
j.append(4)
print(j) #结果为：[1.5, 2.5, 3.5, 4]
print(hex(id(j))) #结果为：0xb6fed04cL
print(j) #结果为：[1.5, 2.5, 3.5, 4]
print(hex(id(k))) #结果为：0xb6fed04cL 

#Python解释器优化情况
s1 =  'a' * 20
s2 =  'a' * 20
print(hex(id(s1)), hex(id(s2))) #结果为：0xb7075320L 0xb7075320L

s1 =  'a' * 21
s2 =  'a' * 21
print(hex(id(s1)), hex(id(s2))) #结果为：0xb70752f0L 0xb7075350L
