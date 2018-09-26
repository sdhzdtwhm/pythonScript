# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Created on 2018年7月30日

@author: yanghang

Description:
    1.此脚本用于移动中央不良系统统计接口服务器数据积压，并写入mysql中
    2.python包依赖：pymysql，os,datetime
    3.定时任务示例（每五分钟获取一次）:*/5 * * * * python /mvtech/count_dir_file.py
'''

import os
import pymysql
import datetime
import socket

#获取本机IP函数
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
#获取主机名
def hostname():
    host = os.popen('echo $HOSTNAME')
    try:
        hostname = host.read()
        return hostname
    finally:
        host.close()
#统计目录中文件的数量
def count(path):
    cou = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path,name))]);
    return cou
#统计目录的大小
def duDir(path):
    os.chdir(path);
    command = "du -sh . |awk '{print $1}'"
    process = os.popen(command);
    output = process.read()
    return output;
    process.close()
#入库
def insert(sql):
    conn = pymysql.connect(user='mvtech', passwd='mvtech123',host='10.99.128.7', db='blxx_netmanager',charset='utf8')
    cur = conn.cursor()
    print(sql)
    sta=cur.execute(sql)
    if sta==1:
        print('Done')
    else:
        print('Failed')
    conn.commit()
    cur.close()
    conn.close()
if __name__ == "__main__":
    #定义变量
    device_name = str(hostname())
    device_ip = str(get_host_ip())
    frist_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    last_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #监控时间
    monitor_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #北京大区统计积压文件并入库
    data_province = '1'
    bid_document_path = '/data/sftp/upload/jinhui'
    overstock_file_size = str(count(bid_document_path))
    overstock_file_count = duDir(bid_document_path)
    sql_bj = "INSERT INTO t_nm_data_analysis_performance_info (device_ip,device_name,data_province,bid_document_path,overstock_file_size,overstock_file_count,frist_time,last_time,monitor_time) VALUES ('"+device_ip+"','"+device_name+"','"+data_province+"','"+bid_document_path+"','"+overstock_file_size+"','"+overstock_file_count+"','"+frist_time+"','"+last_time+"','"+monitor_time+"')"
    insert(sql_bj);
    #上海大区上传文件数目统计入库
    data_province = '2'
    bid_document_path = '/data/sftp/upload/nuoxi'
    overstock_file_size = str(count(bid_document_path))
    overstock_file_count = duDir(bid_document_path)
    sql_sh = "INSERT INTO t_nm_data_analysis_performance_info (device_ip,device_name,data_province,bid_document_path,overstock_file_size,overstock_file_count,frist_time,last_time,monitor_time) VALUES ('"+device_ip+"','"+device_name+"','"+data_province+"','"+bid_document_path+"','"+overstock_file_size+"','"+overstock_file_count+"','"+frist_time+"','"+last_time+"','"+monitor_time+"')"
    insert(sql_sh);
    #广州大区上传文件数目统计入库
    data_province = '3'
    bid_document_path = '/data/sftp/upload/hanbang'
    overstock_file_size = str(count(bid_document_path))
    overstock_file_count = duDir(bid_document_path)
    sql_gz = "INSERT INTO t_nm_data_analysis_performance_info (device_ip,device_name,data_province,bid_document_path,overstock_file_size,overstock_file_count,frist_time,last_time,monitor_time) VALUES ('"+device_ip+"','"+device_name+"','"+data_province+"','"+bid_document_path+"','"+overstock_file_size+"','"+overstock_file_count+"','"+frist_time+"','"+last_time+"','"+monitor_time+"')"
    insert(sql_gz);
