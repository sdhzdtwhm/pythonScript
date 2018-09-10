# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 2018年8月21日

@author: yanghang

Description:
    1.shutil模块使用
                    拷贝文件：shutil.copy('d:\\myloader.sh','c:\\1\\myloader.sh')
                    拷贝文件夹：shutil.copytree('d:\\1','c:\\1')
"""
import shutil

def yasuo():
    shutil.make_archive(base_name='d:\\a',format='gztar',root_dir='D:\\360Downloads')

if __name__ == '__main__':
    yasuo()
