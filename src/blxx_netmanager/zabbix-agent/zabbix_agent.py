# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Created on 2018年7月26日

@author: yanghang

Description:
    1.此脚本用于使用yum安装zabbix_agent,替换配置文件，服务自启动
    2.适用于centos7
    3.使用方法:python zabbix_agent.py
	4.注：需要将zabbix_agent.py zabbix-2.4.8-1.el7.x86_64.rpm zabbix-agent-2.4.8-1.el7.x86_64.rpm一同上传至同一目录
'''
import socket
import os

#获取本机IP函数
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
# 主运行函数
if __name__ == "__main__":
    # 定义变量
    zabbix_server = '192.168.2.250'
    host_ip = str(get_host_ip())
    package1 = 'zabbix-2.4.8-1.el7.x86_64.rpm'
    package2 = 'zabbix-agent-2.4.8-1.el7.x86_64.rpm'
    #安装rpm包
    os.system('rpm -ivh --nodeps %s' % package1)
    os.system('rpm -ivh --nodeps %s' % package2)
    #修改配置文件
    cmd1='sed -i s#Server=127.0.0.1#Server='+zabbix_server+'#g /etc/zabbix/zabbix_agentd.conf'
    os.system(cmd1)
    cmd2='sed -i s#ServerActive=127.0.0.1#ServerActive='+zabbix_server+'#g /etc/zabbix/zabbix_agentd.conf'
    os.system(cmd2)
    cmd3='sed -i s#Hostname=Zabbix\ server#Hostname='+host_ip+'#g /etc/zabbix/zabbix_agentd.conf'
    os.system(cmd3)
    #启动agent和开机自启动
    os.system('systemctl start zabbix-agent && systemctl enable zabbix-agent')