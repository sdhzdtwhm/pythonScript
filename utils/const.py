#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/09/20
@filename: const.py
@author: yanghang
Description:
    1.常量类
"""
from config_utils import ConfigUtils

class Const:
    config = ConfigUtils('conf/config.ini')
    REDIS_HOST = config.get_value('redis', 'host')
    REDIS_PORT = config.get_value('redis', 'port')
    MYSQL_HOST = config.get_value('mysql', 'host')
    MYSQL_PORT = config.get_value('mysql', 'port')
    MYSQL_USERNAME = config.get_value('mysql', 'username')
    MYSQL_PASSWORD = config.get_value('mysql', 'password')
    MYSQL_DATABASE = config.get_value('mysql', 'database')