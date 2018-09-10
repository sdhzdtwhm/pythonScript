#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/09/10
@filename: 集合练习.py
@author: yanghang
Description:
"""

set1 = {1,2,3,4,5,6,6,5,3}
print(set1)

dic = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
print(dic)
set1 = set(dic)
print(set1)

tup1 = ('physics', 'chemistry', 1997, 2000)
tup2 = (1, 2, 3, 4, 5, 6, 7 )
tup3 = tup1 + tup2
print(tup3)