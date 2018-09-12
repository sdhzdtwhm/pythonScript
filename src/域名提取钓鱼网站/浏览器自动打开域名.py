#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/09/11
@filename: 域名提取钓鱼网站.py
@author: yanghang
Description:
"""
import os
from selenium import webdriver
import time

def readFile(filepath,filename):
    """
        1.读取filepath下的filename的文件，将其存入字典中
    """
    os.chdir(filepath)
    f = open(filename, 'r',encoding='UTF-8')
    result_list = []
    for line in f.readlines():
        line = line.strip()
        line = line.split(',')[0].strip()
        # print(line)
        result_list.append(line)
    f.close()
    return result_list

def open_url(url):
    # 加启动配置
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    driver = webdriver.Chrome(chrome_options=option)
    # driver = webdriver.Firefox()
    # driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()

if __name__ == '__main__':
    filepath = os.getcwd()
    filename='3.txt'
    result_list = readFile(filepath, filename)
    print(len(result_list))
    set_list = set(result_list)
    print(len(set_list))
    # print(set_list)
    j = 0
    for i in set_list:
        j = j+1;
        print("正在处理第" + str(j) + "个,域名为：" + i)
        try:
            open_url("http://"+i);
        except Exception as e:
            print(e)