# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Created on 2018年7月6日

@author: yanghang

Description:
    此脚本适用于中央不亮平台使用mysqldump备份数据库
    数据库服务器IP地址:blxx_netmanager-db01:10.99.0.30
    异机备份服务器IP地址:blxx_netmanager-db04:10.99.0.29
    数据库保留份数:7份
    脚本运行服务器:10.99.0.30
    定时任务:0 9 * * * python /data/blxx_mysql_backup.py
'''

import tarfile
import datetime
import os
import ftplib


# 上传至ftp
def upload_file(ftpHost, ftpUser, ftpPwd, ftpDir, fileName, overdueFileName):
    ftp = ftplib.FTP(ftpHost)
    ftp.login(ftpUser, ftpPwd)
    try:
        ftp.mkd(ftpDir)
    except Exception as e:
        print(e)
    ftp.cwd(ftpDir)
    try:
        ftp.delete(overdueFileName)
    except Exception as e:
        print(e)
    ftp.storbinary("STOR " + fileName, open(fileName, "rb"))
    ftp.quit()


# tar打包
def tar_file(backup_path, package_name, local_path):
    os.chdir(backup_path)
    tar = tarfile.open(package_name, 'w:gz', encoding='UTF-8')
    tar.add(local_path)
    tar.close()

    
# 主运行函数
if __name__ == "__main__":
    # 定义日期
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    deleteDay = today - 7 * oneday
    # ftp server 配置信息
    ftp_host = '10.99.0.29'
    ftp_user = 'mvtechftp'
    ftp_pwd = 'mvtech123'
    # ftp 备份工作目录
    ftp_dir = 'mysqlBackup'
    # mysql server 配置信息
    db_host = '10.99.0.30'
    db_user = 'blxx_netmanager'
    db_pwd = 'Mvtech123!@'
    # 本地备份目录
    db_backup_dir = '/data/backupMysql/'
    # 今天的临时备份目录
    today_backup_dir = '/data/backupMysql/' + str(today)
    # 创建今天的临时备份目录
    if not os.path.exists(today_backup_dir):
        os.system('mkdir -p %s' % today_backup_dir)
    # tar包名称
    tar_package_name = db_host + '_' + str(today) + '.tar.gz'
    # 过期tar包名称
    overdue_package_name = db_host + str(deleteDay) + '.tar.gz'
    # 备份的数据库列表
    db_name_list = ['blxx_mobile']
    
    for db_name in db_name_list:
        backup_file_name = db_name + '.sql';
        # 注:mysqldump位置位于/usr/bin/mysqldump，若不是该目录需要更改
        mysqlcmd = "/usr/bin/mysqldump -h " + db_host + " -u" + db_user + " -p" + db_pwd + " --single-transaction " + db_name + " > " + today_backup_dir + "/" + backup_file_name;
        # 执行备份
        os.system(mysqlcmd);
        
    # 将备份文件使用tar_file打包
    tar_file(db_backup_dir, tar_package_name, today_backup_dir);
    # 通过ftp上传tar包备份
    upload_file(ftp_host, ftp_user, ftp_pwd, ftp_dir, tar_package_name, overdue_package_name);
    # 清除今天的临时备份目录
    os.system('rm -rf %s' % today_backup_dir);
    # 删除过期tar包
    os.system('rm -rf %s' % overdue_package_name);
