#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/08/31
@filename: MysqlUtils.py
@author: yanghang
Description:
"""
import pymysql

def execute(host,user,passwd,dbname,sql):
    """
    :param host:
    :param user:
    :param passwd:
    :param dbname:
    :param sql:
    :return: 返回sql查询结果
    """
    conn = pymysql.connect(host=host,user=user, passwd=passwd,db=dbname, charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result

if __name__ == '__main__':
    host = '192.168.2.153'
    user = 'root'
    passwd = 'mvtech123'
    dbname = 'information_schema'
    db_size_sql = "select concat(sum(DATA_LENGTH/1024/1024)+SUM(index_length/1024/1024),' MB') as '数据库占用总空间( MB)' from information_schema.tables;"
    result = execute(host, user, passwd, dbname, db_size_sql)
    print("数据库占用总空间为: "+result[0]["数据库占用总空间( MB)"])
