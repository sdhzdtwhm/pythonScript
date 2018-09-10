#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/09/04
@filename: HostUtils.py
@author: yanghang
Description:
"""
import socket
import platform
import psutil
import os

def get_host_ip():
    """
    :return:获取本机IP函数
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def get_hostname():
    """
    :return:获取主机名
    """
    hostname = socket.gethostname()
    return hostname

def get_os_version():
    """
    :return:获取操作系统版本
    """
    os_version = platform.platform()
    return os_version
def get_mem_used():
    mem = psutil.virtual_memory();
    return mem.used
if __name__ == '__main__':
    print(get_host_ip())
    print(get_hostname())
    print(get_os_version())
    print(platform.version())
    print(platform.machine())
    print(platform.platform())
    print(get_mem_used())
    print(os.sep)