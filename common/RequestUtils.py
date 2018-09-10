#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/08/31
@filename: RequestUtils.py
@author: yanghang
Description:
"""
import requests

url = 'https://www.baidu.com/'
response = requests.get(url)
print(response.content.decode())
# headers = {
#     "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
# }
# response = requests.get(url,headers=headers)