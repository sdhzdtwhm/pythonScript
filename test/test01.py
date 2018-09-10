#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/08/30
@filename: test01.py
@author: yanghang
Description:
"""
import sys
import os

print(os.getcwd())
sys.path.append("D:\work\tools\project\python20180821\common")
print(sys.path)
import A

a=A.A(2,3)
a.add()