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
    db_name_list = []
    for i in result:
        db_name_list.append(i['Database'])
    conn.commit()
    cursor.close()
    conn.close()
    return db_name_list

if __name__ == '__main__':
    host = '192.168.2.153'
    user = 'root'
    passwd = 'mvtech123'
    dbname = 'information_schema'
    sql = "show databases"
    db_name_list = execute(host, user, passwd, dbname, sql)
    print(db_name_list)
