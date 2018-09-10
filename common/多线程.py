#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/09/04
@filename: 多线程.py
@author: yanghang
Description:
"""
import threading
import time
import datetime

def thread_run():
    for i in range(5):
        time.sleep(2)
        current_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print(str(i)+"....."+current_time)

if __name__ == '__main__':
    t1 = threading.Thread(target=thread_run,args=())
    t2 = threading.Thread(target=thread_run,args=())
    t1.start()
    t2.start()