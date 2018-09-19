#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/09/19
@filename: use_schedule.py
@author: yanghang
Description:
"""
import datetime
import schedule
import time
import threading

def job1():
    time.sleep(2)
    print("job1:", datetime.datetime.now())

def job2():
    time.sleep(2)
    print("job2:", datetime.datetime.now())

# 执行job
# schedule.every(1).seconds.do(job1)
# schedule.every(1).seconds.do(job2)
# while True:
#     schedule.run_pending()
#     time.sleep(1)


def job1_task():
    threading.Thread(target=job1).start()


def job2_task():
    threading.Thread(target=job2).start()

schedule.every(2).seconds.do(job1_task)
schedule.every(2).seconds.do(job2_task)
while True:
    schedule.run_pending()
    time.sleep(1)

# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).days.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

