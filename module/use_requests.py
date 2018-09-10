# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 2018年8月15日

@author: yanghang

Description:
"""
import requests
headers = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
res_get = requests.get('http://httpbin.org/get')
print(res_get.text)
