# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Created on 2018年7月25日

@author: yanghang

Description:
    1.此脚本用于监控mysql性能指标，将查询出的性能指标插入mysql性能监控表中
    2.需要手工安装包:pymysql
    3.定时任务
    4.运行周期
'''
import os
import socket
import pymysql


# 查询设备名称
def hostname():
        sys = os.name
        if sys == 'nt':
                host_name = os.getenv('computername')
                return host_name

        elif sys == 'posix':
                host = os.popen('echo $HOSTNAME')
                try:
                        host_name = host.read()
                        return host_name
                finally:
                        host.close()
        else:
                return 'Unkwon host_name'
# 获取设备IP
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        host_ip = s.getsockname()[0]
    finally:
        s.close()
    return host_ip
# 获取运行状态

# 数据库运行时间
os.system('mysql')
# 当前连接数

# 数据库占用大小

# 告警开关

# 插入sql
def insert(host_name,host_ip,db_ip,db_name,start_time,end_time,backup_file_size):
    conn = pymysql.connect(user='root', passwd='mvtech123',host='192.168.2.253', db='net_manager_blxx',charset='utf8')
    cur = conn.cursor()
    sql= "INSERT INTO t_nm_database_backup (host_name,host_ip,db_ip,db_name,start_time,end_time,backup_file_size) VALUES ('"+host_name+"','"+host_ip+"','"+db_ip+"','"+db_name+"','"+start_time+"','"+end_time+"','"+backup_file_size+"')"
    print(sql)
    sta=cur.execute(sql)
    if sta==1:
        print('Done')
    else:
        print('Failed')
    conn.commit()
    cur.close()
    conn.close()

#查询mysql运行时间
def queryUptime():
    conn = pymysql.connect(user='root', passwd='mvtech123',host='192.168.2.253', db='net_manager_blxx',charset='utf8')
    cur = conn.cursor()
    sql= "show global status like 'uptime';"
    cur.execute(sql)
    uptime = cur.fetchone()
    result = uptime[1]
    print(result)
    return result
    conn.commit()
    cur.close()
    conn.close()

#查询mysql连接数
def queryConn():
    conn = pymysql.connect(user='root', passwd='mvtech123',host='192.168.2.107', db='mysql',charset='utf8')
    cur = conn.cursor()
    sql= "show global status like 'Threads_connected';"
    cur.execute(sql)
    uptime = cur.fetchone()
    result = uptime[1]
    return result
    conn.commit()
    cur.close()
    conn.close()

#将秒转化为day+hour+min+秒
def conver(value):
    days = int(value) // 86400;
    hours = int(value - (days * 86400)) // 3600;
    minutes = int(value - (days * 86400) - (hours * 3600))//60;
    seconds = value - (days * 86400) - (hours * 3600) - (minutes * 60)
    result = str(days)+'天' +str(hours)+'小时'+str(minutes)+'分钟'+str(seconds)+'秒'
    #result = 'mysql服务已运行:'+ str(days)+'天' +str(hours)+'小时'+str(minutes)+'分钟'+str(seconds)+'秒'
    return result

#数据库占用大小
def mysql_size():
    conn = pymysql.connect(user='root', passwd='mvtech123',host='192.168.2.107', db='mysql',charset='utf8')
    cur = conn.cursor()
    #计算DATA_LENGTH求和
    sql= "select round(sum(DATA_LENGTH/1024/1024),2) as data from information_schema.TABLES;"
    #计算INDEX_LENGTH求和
    #sql= "select round(sum(INDEX_LENGTH/1024/1024),2) as data from information_schema.TABLES;"
    #sql= "select DATA_LENGTH from information_schema.TABLES;"
    cur.execute(sql)
    uptime = cur.fetchone()
#     print(uptime[0])
    result = uptime[0]
    return result
    conn.commit()
    cur.close()
    conn.close()



# 主运行函数
if __name__ == "__main__":
    #获取主机名
    print(hostname());
    #获取本机ip
    print(get_host_ip());
    #查询mysql运行时间返回运行了多少秒
    mysql_uptime = float(queryUptime())
    #转换运行时间
    print('mysql服务已运行:'+ conver(mysql_uptime))
    #获取连接数
    mysql_conn = queryConn()
    print('mysql连接数为:'+mysql_conn)
    folder_path = 'd:\\360Downloads'
    full_size = sum(sum(os.path.getsize(os.path.join(parent, file)) for file in files) for parent, dirs, files in os.walk(folder_path))/1024/1024
    print(full_size)
    print(mysql_size())