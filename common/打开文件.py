#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/09/04
@filename: 打开文件.py
@author: yanghang
Description:
"""

import os

def readFile(filepath,filename):
    """
        1.读取filepath下的filename的文件，将其存入字典中
    """
    os.chdir(filepath)
    f = open(filename, 'r')
    result = {}
    for line in f.readlines():
        line = line.strip()
        if not len(line):
            continue
        key = line.split(':')[0].strip()
        value = line.split(':')[1].strip()
        result[key] = value
    return result
    f.close()

if __name__ == '__main__':
    filepath = os.getcwd()
    filename = "host.txt"
    print(readFile(filepath,filename))