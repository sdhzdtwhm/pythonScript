#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/09/20
@filename: main.py
@author: yanghang
Description:
"""
import sys
import os
package_path = os.getcwd()+os.sep+"utils"
sys.path.append(package_path)

from redis_utils import RedisUtils
from config_utils import ConfigUtils

if __name__ == '__main__':
    config = ConfigUtils('conf/config.ini')
    REDIS_HOST = config.get_value('redis', 'host')
    REDIS_PORT = config.get_value('redis', 'port')
    MYSQL_HOST = config.get_value('mysql', 'host')
    MYSQL_PORT = config.get_value('mysql', 'port')
    MYSQL_USERNAME = config.get_value('mysql', 'username')
    MYSQL_PASSWORD = config.get_value('mysql', 'password')
    MYSQL_DATABASE = config.get_value('mysql', 'database')
    redis = RedisUtils(REDIS_HOST,REDIS_PORT)
    redis.set_str('hello','11111')
    print(redis.get_str('hello'))
