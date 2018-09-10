#!/usr/bin/python 
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     autoSvnBackup.py
   Description :  自动备份svn文件并上传至ftp服务器中
   Author :       yanghang
   date：          2018/5/8
-------------------------------------------------
   Change Activity:
                   2018/5/8:
-------------------------------------------------
"""
import tarfile,datetime,os,ftplib

today = datetime.date.today()
oneday = datetime.timedelta(days=1)
deleteDay = today - 30*oneday

# 备份文件存放的路径
backupDir = 'D:\\svn-backup\\backup'
# 备份文件的名称
packageName='svn_'+str(today)+'.tar.gz'
# 所要备份的文件夹
localPath="D:\\Repositories"
# 30天以前的备份文件名称
deleteFileName='svn_'+str(deleteDay)+'.tar.gz'
# ftp 工作目录
ftpDir='svnBackup'

# tar打包
def tarFile(backupDir,packageName,localPath):
    os.chdir(backupDir)
    tar = tarfile.open(packageName, 'w:gz', encoding='GB2312')
    tar.add(localPath)
    tar.close()

# 删除30天以外的文件
def deleteFile(backupDir,deleteFileName):
    os.chdir(backupDir);
    try:
        os.remove(deleteFileName);
    except Exception as e:
        print(e)
# 上传至ftp
def uploadFile():
    ftp = ftplib.FTP("192.168.2.252")
    ftp.login("duftp", "mvtech123")
    try:
        ftp.mkd(ftpDir)
    except Exception as e:
        print(e)
    ftp.cwd(ftpDir)
    try:
        ftp.delete(deleteFileName)
    except Exception as e:
        print(e)
    ftp.storbinary("STOR " + packageName, open(packageName, "rb"))
    ftp.quit()
# 主运行函数
if __name__=="__main__":
    deleteFile(backupDir,deleteFileName);
    tarFile(backupDir,packageName,localPath);
    uploadFile();