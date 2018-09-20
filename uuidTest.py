#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/09/19
@filename: uuidTest.py
@author: yanghang
Description:
"""
import sys
import os

package_path = os.getcwd()+os.sep+"utils"
sys.path.append(package_path)

from UUIDUtils import UUID

print(UUID.getUUID(1))
