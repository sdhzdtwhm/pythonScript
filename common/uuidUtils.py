#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/08/30
@filename: uuidUtils.py
@author: yanghang
Description:
"""
import uuid
import socket

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

def create_id_uuid3(ip):
    s_uuid=str(uuid.uuid3(uuid.NAMESPACE_URL,ip))
    l_uuid=s_uuid.split('-')
    s_uuid=''.join(l_uuid)
    return s_uuid
if __name__ == '__main__':
    ip = get_host_ip()
    print(create_id_uuid3(ip))
    print(create_id_uuid3(ip))