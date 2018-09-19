#!/usr/local/python3.6.4/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 2018/09/19
@filename: test.py
@author: yanghang
Description:
"""
import sys
import os

package_path = os.getcwd()+os.sep+"utils"
sys.path.append(package_path)
from PropertiesUtiil import Properties

dictProperties=Properties("constant.properties").getProperties()
print(dictProperties)
