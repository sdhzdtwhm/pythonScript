#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/08/28
@filename: blxx_domain_process_time_monitor.py
@author: yanghang
Description:
    1.此脚本用于网管系统》业务监控》域名处理时长业务监控
    2.加入crontab中，每小时执行一次：0 * * * * python /data/script/blxx_domain_process_time_monitor.py
    3.此脚本需要安装pymysql
"""
import pymysql
import datetime


def select(sql):
    """sql查询"""
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


if __name__ == '__main__':
    # 现在时间
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    # print(current_date)
    #sql = "SELECT ifnull(floor(AVG(daqutime)), 0) AS avgdaqutime , ifnull(floor(AVG(systime)), 0) AS avgsystime , ifnull(floor(AVG(ubtime)), 0) AS avgubtime , ifnull(floor(AVG(fbtime)), 0) AS avgfbtime , ifnull(floor(AVG(sysblocktime)), 0) AS sysblocktime FROM ( SELECT td.domain, date(td.updatetime) AS blockdate, 0 AS isreopen, tdt.endtime , td.sendtime, td.updatetime, td.firstapplytime, td.domaintype, td.domainsource , TIMESTAMPDIFF(SECOND, tdt.endtime, td.sendtime) AS daqutime , TIMESTAMPDIFF(SECOND, td.sendtime, td.updatetime) AS systime , TIMESTAMPDIFF(SECOND, td.updatetime, td.blocktime) AS ubtime , TIMESTAMPDIFF(SECOND, td.firstapplytime, td.blocktime) AS fbtime , TIMESTAMPDIFF(SECOND, td.send_block_time, td.recv_block_time) AS sysblocktime FROM t_domain td INNER JOIN t_domain_time tdt ON td.domain = tdt.domain INNER JOIN t_zywzjc_task zyt ON td.domain = zyt.domain ) b WHERE b.blockdate = '" + current_date + "' AND b.blockdate IS NOT NULL GROUP BY b.blockdate;"
    sql = "SELECT blockdate , ifnull(floor(AVG(daqutime)), 0) AS avgdaqutime , ifnull(floor(AVG(systime)), 0) AS avgsystime , ifnull(floor(AVG(ubtime)), 0) AS avgubtime , ifnull(floor(AVG(fbtime)), 0) AS avgfbtime , ifnull(floor(AVG(sysblocktime)), 0) AS sysblocktime FROM ( SELECT tb.domain, date(td.updatetime) AS blockdate, tb.isreopen, tdt.endtime , td.sendtime, td.updatetime, td.firstapplytime, td.domaintype, td.domainsource , TIMESTAMPDIFF(SECOND, tdt.endtime, td.sendtime) AS daqutime , TIMESTAMPDIFF(SECOND, td.sendtime, td.updatetime) AS systime , TIMESTAMPDIFF(SECOND, td.updatetime, td.blocktime) AS ubtime , TIMESTAMPDIFF(SECOND, td.firstapplytime, td.blocktime) AS fbtime , TIMESTAMPDIFF(SECOND, td.send_block_time, td.recv_block_time) AS sysblocktime FROM t_domain td INNER JOIN t_blacklist tb ON tb.domain = td.domain INNER JOIN t_domain_time tdt ON tb.domain = tdt.domain WHERE 1 = 1 ) b WHERE b.blockdate IS NOT NULL AND date(b.blockdate) = date(now());"
    # print(sql)
    result = select(sql)[0]
    # print(result)
    avgdaqutime = str(result["avgdaqutime"])
    avgsystime = str(result["avgsystime"])
    avgubtime = str(result["avgubtime"])
    avgfbtime = str(result["avgfbtime"])
    sysblocktime = str(result["sysblocktime"])
    insertSQL = "INSERT INTO `t_nm_domain_process_time_monitor` ( `avgdaqutime`, `avgsystime`, `avgubtime`, `avgfbtime`, `sysblogtime`, `create_date`, `update_date`) VALUES ('" + avgdaqutime + "', '" + avgsystime + "', '" + avgubtime + "', '" + avgfbtime + "', '" + sysblocktime + "', '" + current_time + "', '" + current_time + "');"
    insert(insertSQL)
