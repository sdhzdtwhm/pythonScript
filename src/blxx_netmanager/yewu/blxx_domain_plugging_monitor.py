#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/08/28
@filename: blxx_domain_plugging_monitor.py
@author: yanghang
Description:
    1.此脚本用于网管系统》业务监控》域名封堵失败状态监控
    2.加入crontab中，每天凌晨执行一次：0 1 * * * python /data/script/blxx_domain_plugging_monitor.py
    3.此脚本需要安装pymysql
"""
import pymysql
import datetime


def select(sql):
    """从blxx_mobile库中查询业务数据"""
    conn = pymysql.connect(user='weihu', passwd='Mvtech123!@', host='10.99.0.92', db='blxx_mobile', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result


def insert(sql):
    """向网管库中插入数据"""
    conn = pymysql.connect(user='mvtech', passwd='mvtech123', host='127.0.0.1', db='blxx_netmanager', charset='utf8')
    cursor = conn.cursor()
    sta = cursor.execute(sql)
    if sta == 1:
        print('Done')
    else:
        print('Failed')
    conn.commit()
    cursor.close()
    conn.close()


def truncate(sql):
    """清除网管数据库t_nm_domain_plugging_monitor表中数据"""
    conn = pymysql.connect(user='mvtech', passwd='mvtech123', host='127.0.0.1', db='blxx_netmanager', charset='utf8')
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    # 现在时间
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 清除t_nm_domain_plugging_monitor表中的数据
    truncateSQL = "truncate table t_nm_domain_plugging_monitor"
    truncate(truncateSQL)
    ymfdsql = "SELECT g.domain, IFNULL(t.blocktime,t.createtime) blocktime, g.begintime, g.readytime, g.state FROM t_domain_need_dialing g, t_domain t WHERE t.domain = g.domain AND g.state = '4'"
    # print(ymfdsql)
    result = select(ymfdsql)
    # print(result)
    # 遍历列表，根据每个列表项生成
    for i in result:
        # print(i)
        domain = str(i["domain"])
        blocktime = str(i["blocktime"])
        begintime = str(i["begintime"])
        readytime = str(i["readytime"])
        insertSQL = "INSERT INTO `t_nm_domain_plugging_monitor` ( `domain`, `blocktime`, `begintime`, `readytime`,`state`, `create_date`, `update_date`) VALUES ('" + domain + "', '" + blocktime + "', '" + begintime + "', '" + readytime + "','4',  '" + current_time + "', '" + current_time + "');"
        insert(insertSQL)
