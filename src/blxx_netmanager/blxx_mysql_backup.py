# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Created on 2018年7月24日

@author: yanghang

Description:
    1.此脚本用于定时备份mysql库，并将相关信息插入t_nm_mysql_backup表中
    2.python包依赖:pymysql
    3.定时任务(每天凌晨两点) : 0 2 * * * python /mvtech/mysql_backup.py
'''

import datetime
import os
import pymysql

#获取主机名
def hostname():
    host = os.popen('echo $HOSTNAME')
    try:
        hostname = host.read()
        return hostname
    finally:
        host.close()
#根据文件路径获取文件大小
def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)

#向t_nm_database_backup中插入记录
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

#主运行函数
if __name__ == "__main__":
    #定义日期
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    #备份脚本运行服务器
    host_name = str(hostname())
    host_ip = '192.168.2.253'
    #mysql server 配置信息
    db_host = '192.168.2.253'
    db_user = 'root'
    db_pwd = 'mvtech123'
    db_name = 'blxx_shyd'
    #本地备份目录
    db_backup_dir = '/mvtech/backupMysql/'
    #创建今天的备份目录
    if not os.path.exists(db_backup_dir):
        os.system('mkdir -p %s' % db_backup_dir)
    #备份文件名称
    backup_file_name = db_name+ '_' + str(today) + '.sql';
    #现在时间
    start_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
    mysqlcmd = "/mvtech/mysql/bin/mysqldump -h " + db_host + " -u" + db_user + " -p" + db_pwd + " --single-transaction " + db_name + " > " + db_backup_dir + "/" + backup_file_name;
    #执行备份
    os.system(mysqlcmd);
    filePath = db_backup_dir + backup_file_name
    #print(filePath)
    backup_file_size = str(get_FileSize(filePath))
    end_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insert(host_name,host_ip,db_host,db_name,start_time,end_time,backup_file_size)