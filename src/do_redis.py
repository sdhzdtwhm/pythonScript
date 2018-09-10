# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 2018年7月27日
@author: yanghang
Description:
    1.使用redis操作redis
"""
import redis

r = redis.Redis(host='127.0.0.1', port=6379,db=0)
r.set('name', 'zhangsan')   #添加
print (r.get('name'))   #获取