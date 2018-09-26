#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/09/18
@filename: do_url.py
@author: yanghang
Description:
"""
from urllib.parse import urlparse

result = urlparse('https://www.baidu.com/index.html')
print(result)
