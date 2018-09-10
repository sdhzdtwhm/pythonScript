# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Created on 2018年7月9日

@author: yanghang

Description: 
'''
import pyhdfs

fs = pyhdfs.HdfsClient(hosts='192.168.2.153:50070', user_name='hdfs')

#输出根目录下的文件夹
print(fs.listdir('/'))
