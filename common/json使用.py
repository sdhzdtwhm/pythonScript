#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/09/04
@filename: json使用.py
@author: yanghang
Description:
"""
import json

dict = {'name':'zhangsan','age':33,'address':'红星路'}
print(type(dict))
print(dict)
#对dict进行序列化
dict_xulie = json.dumps(dict,ensure_ascii=False)
print(type(dict_xulie))
print(dict_xulie)

#对dict_xulie进行反序列化处理
dict_fan = json.loads(dict_xulie)
print(type(dict_fan))
print(dict_fan)