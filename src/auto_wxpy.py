# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 2018年8月16日

@author: yanghang

Description:
    1.使用wxpy模块自动给微信好友发送消息
"""
# 导入模块
#from __future__ import unicode_literals
import threading
import wxpy
import time

#cache_path参数是缓存登陆信息
bot = wxpy.Bot(cache_path=True)

def send_msg_self():
    """给机器人自己发送消息"""
    bot.self.send('Hello World!')

def send_msg_file():
    """给文件助手发送消息"""
    bot.file_helper.send("现在时间："+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    global timer
    timer = threading.Timer(5, send_msg_file)
    timer.start()

def send_msg_friend():
    """搜索朋友名称并发送消息"""
    my_friend = bot.friends().search('杉歌')[1]
    my_friend.send("现在时间是："+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    global timer
    timer = threading.Timer(5, send_msg_friend)
    timer.start()

if __name__ == "__main__":
    timer = threading.Timer(5, send_msg_friend)
    timer.start()