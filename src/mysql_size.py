# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Created on 2018年7月26日

@author: yanghang

Description:
'''
import pymysql

def mysql_size():
    conn = pymysql.connect(user='root', passwd='mvtech123',host='192.168.2.253', db='net_manager_blxx',charset='utf8')
    cur = conn.cursor()
    sql= "select round(sum(DATA_LENGTH/1024/1024),2) as data from information_schema.TABLES;"
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
    print(mysql_size())