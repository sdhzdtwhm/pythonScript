#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/09/20
@filename: config_utils.py
@author: yanghang
Description:
    1.读取config.ini文件中的配置项的value值
"""
import os,sys
from configobj import ConfigObj


class ConfigUtils:

    def __init__(self,file):
        self.file = file

    def config(self):
        config = ConfigObj(self.file, encoding='UTF8')
        return  config

    def get_value(self, section, item):
        config = self.config()
        value = config[section][item]
        return value
