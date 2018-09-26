# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Created on 2018年7月30日

@author: yanghang

Description:
    1.本脚本适用于中央不良系统ftp接口监控
    2.在zabbix中创建监控项，需要在/etc/zabbix/zabbix_agentd.conf配置文件添加参数：
        UnsafeUserParameters=1
        UserParameter=ftp.monitor,python /mvtech/ftp_interface_monitor.py
'''
import os
import ftplib


#测试ftp接口
def uploadFile(filename):
    ftp = ftplib.FTP("192.168.2.252")
    ftp.login("duftp", "mvtech123")
    ftp.storbinary("STOR " + filename, open(filename, "rb"))
    ftp.quit()

#主运行函数
if __name__ == "__main__":
    #删除/tmp/ftptest.txt文件
    os.system('rm -rf /tmp/ftptest.txt')
    #在/tmp目录中创建ftptest.txt文件
    os.system('touch /tmp/ftptest.txt && chmod 777 /tmp/ftptest.txt');
    #
    os.chdir('/tmp')
    try:
        uploadFile('ftptest.txt')
        result = 1
        #成功返回值为1
        print(result)
    except Exception as e:
        #上传文件不成功，返回值为2
        result = 2
        print(result)