# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Created on 2018年7月27日

@author: yanghang

Description:
    1.此脚本用于返回url状态码
'''

import requests

res = requests.get("http://192.168.2.106:8080/")
print(res)
print(res.status_code)