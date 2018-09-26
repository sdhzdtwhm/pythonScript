#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/09/14
@filename: check_server_config.py
@author: yanghang
Description:
    1.查询服务器的硬件配置
"""
import os

def get_result(command):
    result = os.popen(command).read()
    return result

if __name__ == '__main__':
    commmand_dict = {
            '物理CPU个数：':"cat /proc/cpuinfo |grep 'physical id'|sort|uniq|wc -l",
            '每个物理cpu的核数：':"cat /proc/cpuinfo |grep 'cores'|uniq",
            '逻辑cpu个数：':"cat /proc/cpuinfo |grep 'processor'|wc -l",
            '内存大小为：': "cat /proc/meminfo | grep MemTotal"
            }
    for key in commmand_dict:
        command = commmand_dict[key]
        result = get_result(command)
        print(key+result)
