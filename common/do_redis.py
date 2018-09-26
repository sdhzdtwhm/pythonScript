# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 2018年7月27日
@author: yanghang
Description:
    1.使用redis操作redis
"""
import redis

def get_hash_key(key):
    pass

pool = redis.ConnectionPool(host='192.168.2.253', port=6379,db=0)
conn = redis.Redis(connection_pool=pool)
keys = conn.keys()
print(keys)
for i in keys:
    print(str(i)+'键的类型是'+str(conn.type(i)))

conn.connection_pool.disconnect()
