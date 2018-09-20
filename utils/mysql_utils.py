#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/09/20
@filename: mysql_utils.py
@author: yanghang
Description:
"""
import pymysql


class MysqlUtils:

    def __init__(self, host, username, password, port, database):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.database = database

    def conn(self):
        pass
