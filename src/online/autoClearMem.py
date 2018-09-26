#!/usr/bin/python
#coding=utf-8
#此脚本适用于集中监控系统对不良系统的内存报警
#由于集中监控监控的指标不是减去buffer和cache后的使用量
#因此使用psutil监控内存的free值，若free的百分比超过30%则触发清除pagecahce(页面缓存),释放缓冲区内存
#添加到定时任务中每半小时执行一次
#脚本添加时间：2018-05-04

import psutil,os

mem = psutil.virtual_memory();

if((mem.free/float(mem.total))>0.3):
    print(mem.free/float(mem.total));
    print('内存free百分比超过total的30%，集中监控不会报警');
else:
    print("内存free百分比小于total的30%,集中监控会报警，即将执行pagecache清理")
    os.system('/bin/sync;echo 1 > /proc/sys/vm/drop_caches;');
    print(mem.free/float(mem.total));
    print("清除pagecache结束")
