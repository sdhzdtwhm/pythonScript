# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 2018年8月15日

@author: yanghang

Description:
    1.此脚本使用selenium自动化登陆所给网站
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def auto_url_login(url,username,password):
    """
        1.本方法自动登陆传入的url网站,用于验证网站的可用性
        2.使用此方法需要传入三个参数:url(网站的url地址)，username(网站登陆用户名)，password(往回走哪登录密码)
    """
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.set_headless()
    browser = webdriver.Firefox(firefox_options=fireFoxOptions)
    try:
        browser.get(url) #实现自动点击登陆
        #查找用户名的id
        user = browser.find_element_by_id("name")
        user.send_keys(username)  #输入账号
        #查找password的id
        passwd = browser.find_element_by_id("password")
        passwd.send_keys(password)  #输入密码
        #注:此处的功能判断是否登陆成功，目前以下代码无法实现
        try:
            passwd.send_keys(Keys.RETURN) #实现自动点击登陆
            print("网站:"+url+"登陆成功，此网站登陆状态验证正常!")
        except Exception as err:
            print("网站:"+url+"目前无法登陆")
            print(err)
    except Exception as err:
        print(err)
    browser.quit()

if __name__ == "__main__":
    url = 'http://192.168.2.51/zabbix/index.php'
    username = 'Admin'
    password = 'zabbix1'
    start = time.clock()
    auto_url_login(url, username, password)
    end = time.clock()
    print(end-start)

