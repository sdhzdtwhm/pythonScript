#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/09/19
@filename: testConfig.py
@author: yanghang
Description:
"""
from ConfigUtils import ConfigUtils

# import configparser

# import os
#
# os.chdir(os.getcwd())
#
# cu = ConfigUtils('conf.ini')
#
# # cu.read('conf.ini',encoding='utf-8')
# print(cu.conf.sections())
# conList = cu.conf.sections()
#
# print(cu['SFTP']['host'])
# host = cu['SFTP']['host']
# username = cu['SFTP']['user']
# password = cu['SFTP']['password']
# print(host)
# print(username)
# print(password)

if __name__ == '__main__':
    # conf = configparser.ConfigParser()
    # conf = conf.read('conf.ini',encoding='utf-8')
    info = ConfigUtils('conf.ini')
    info.get_value()
