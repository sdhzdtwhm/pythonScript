#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/08/30
@filename: TarUtils.py
@author: yanghang
Description:
"""
import tarfile
import os

class Foo:
    def tar_dir(self, package_dir, package_name, file_path):
        """
        :param backup_dir:压缩包存放的文件夹
        :param package_name:压缩包的名称·
        :param file_path:被压缩的文件所在的路径
        :return:
        """
        os.chdir(package_dir)
        tar = tarfile.open(package_name, 'w:gz', encoding='GB2312')
        tar.add(file_path)
        tar.close()

if __name__ == '__main__':
    package_dir = "D:\\"
    package_name = "mysite.tar.gz"
    file_path = "D:\\mysite"
    #初始化实例
    obj = Foo()
    obj.tar_dir(package_dir, package_name, file_path)
