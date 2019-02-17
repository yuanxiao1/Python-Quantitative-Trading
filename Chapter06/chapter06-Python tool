#!/usr/bin/python
from threading import Thread
from multiprocessing import Process,Manager
from timeit import timeit

#计算密集型任务
def count(n):
	while n > 0:
		n-=1
#不采用多任务方式     
def test_normal():
	count(1000000)
	count(1000000)
#多线程方式     
def test_Thread():
 	t1 = Thread(target=count,args=(1000000,))
 	t2 = Thread(target=count,args=(1000000,))
 	t1.start()
 	t2.start()
 	t1.join()
 	t2.join()			
#多进程方式  		
def test_Process():
 	t1 = Process(target=count,args=(1000000,))
 	t2 = Process(target=count,args=(1000000,))
 	t1.start()
 	t2.start()
 	t1.join()
 	t2.join()	

if __name__ == '__main__':
 	print "test_normal",timeit('test_normal()','from __main__ import test_normal',number=10)
 	print "test_Thread",timeit('test_Thread()','from __main__ import test_Thread',number=10)
 	print "test_Process",timeit('test_Process()','from __main__ import test_Process',number=10)
