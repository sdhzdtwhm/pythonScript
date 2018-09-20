#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/09/20
@filename: redis_utils.py
@author: yanghang
Description:
    1.redis 工具类
"""
import redis


class RedisUtils:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def single_conn(self):
        pool = redis.ConnectionPool(host=self.host, port=self.port)
        r = redis.Redis(connection_pool=pool)
        return r

    def conn(self):
        #redis单实例连接
        r = self.single_conn()
        #redis cluster连接
        #r = self.cluster_conn()
        return r

    def get_str(self, key):
        r = self.conn()
        result = r.get(key).decode()
        r.connection_pool.disconnect()
        return result

    def set_str(self, key, value):
        r = self.conn()
        r.set(key,value)
        r.connection_pool.disconnect()
