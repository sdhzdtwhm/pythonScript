#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2018/08/29
@filename: blxx_domain_audit_total_monitor.py
@author: yanghang
Description:
    1.此脚本用于网管系统》业务监控》系统审核量监控
    2.加入crontab中，每小时执行一次：0 * * * * python /data/script/blxx_domain_audit_total_monitor.py
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
    #现在时间
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #大区上报量
    region_report_total_sql = "SELECT COUNT(*) AS domainnum  FROM t_source_domain d  WHERE 1=1 and  date(d.createtime) =date(now());"
    region_report_total_result = select(region_report_total_sql)[0]
    region_report_total = str(region_report_total_result["domainnum"])
    #print(region_report_total)
    #过滤入库量
    zb_total_sql = "select count(*) as zb_total from t_domain d where date(d.updatetime) =date(now());"
    tb_total_sql = "select count(*) as tb_total from t_blacklist t where date(t.blocktime) =date(now());"
    zb_total_result = int(select(zb_total_sql)[0]["zb_total"])
    tb_total_result = int(select(tb_total_sql)[0]["tb_total"])
    filter_warehouse_total = str(zb_total_result + tb_total_result)
    #print(filter_warehouse_total)
    #初审违规量
    firt_suppl_total_sql = "select count(*) firt_suppl_total from t_supplements_domain_record d where d.firstauditstatus = 1 and d.secondauditstatus = 0 and date(d.updatetime) =date(now());"
    firt_fish_total_sql = "select count(*) firt_fish_total from t_fish_domain_record r where r.firstauditstatus = 1 and r.secondauditstatus = 0 and date(r.updatetime) =date(now());"
    firt_record_total_sql = "select count(*) firt_record_total from t_domain_record c where c.firstauditstatus = 1 and c.secondauditstatus = 0 and date(c.updatetime) =date(now());"
    firt_suppl_total_result = int(select(firt_suppl_total_sql)[0]["firt_suppl_total"])
    firt_fish_total_result = int(select(firt_fish_total_sql)[0]["firt_fish_total"])
    firt_record_total_result = int(select(firt_fish_total_sql)[0]["firt_fish_total"])
    first_total = str(firt_suppl_total_result + firt_fish_total_result + firt_record_total_result)
    #print(first_total)
    #初审不违规量
    firt_no_suppl_total = "select count(*) firt_no_suppl_total from t_supplements_domain_record d where d.firstauditstatus = 2 and d.secondauditstatus = 0 and date(d.updatetime) =date(now());"
    firt_no_fish_total = "select count(*) firt_no_fish_tota from t_fish_domain_record r where r.firstauditstatus = 2 and r.secondauditstatus = 0 and date(r.updatetime) =date(now());"
    firt_no_record_total = "select count(*) firt_record_total from t_domain_record c where c.firstauditstatus = 1 and c.secondauditstatus = 0 and date(c.updatetime) =date(now());"
    firt_no_suppl_total_result = int(select(firt_no_suppl_total)[0]["firt_no_suppl_total"])
    firt_no_fish_tota_result = int(select(firt_no_fish_total)[0]["firt_no_fish_tota"])
    firt_no_record_total_result = int(select(firt_no_record_total)[0]["firt_record_total"])
    first_no_total = str(firt_no_suppl_total_result + firt_no_fish_tota_result + firt_no_record_total_result)
    #print(first_no_total)
    #复审违规量
    second_suppl_total_sql = "select count(*) second_suppl_total from t_supplements_domain td where td.firstauditstatus = 1 and (td.secondauditstatus != 0 and td.secondauditstatus != 2) and date(td.updatetime) =date(now());"
    second_fish_total_sql = "select count(*) second_fish_total from t_fish_domain ts where ts.firstauditstatus = 1 and (ts.secondauditstatus != 0 and ts.secondauditstatus != 2) and date(ts.updatetime) =date(now());"
    second_record_total_sql = "select count(*) second_record_total from t_domain tt where tt.firstauditstatus = 1 and (tt.secondauditstatus != 0 and tt.secondauditstatus != 2) and date(tt.updatetime) =date(now());"
    second_suppl_total_result = int(select(second_suppl_total_sql)[0]["second_suppl_total"])
    second_fish_total_result = int(select(second_fish_total_sql)[0]["second_fish_total"])
    second_record_total_result = int(select(second_record_total_sql)[0]["second_record_total"])
    second_total = str(second_suppl_total_result + second_fish_total_result + second_record_total_result)
    #print(second_total)
    #复审不违规量
    second_no_suppl_total_sql = "select count(*) second_no_suppl_total  from t_supplements_domain_record rd where rd.firstauditstatus = 1 and rd.secondauditstatus = 2 and date(rd.updatetime) =date(now());"
    second_no_fish_total_sql = "select count(*) second_no_fish_total   from t_fish_domain_record fs where fs.firstauditstatus = 1 and fs.secondauditstatus = 2 and date(fs.updatetime) =date(now());"
    second_no_record_total = "select count(*) second_no_record_total   from t_domain_record ec where ec.firstauditstatus = 1 and ec.secondauditstatus = 2 and date(ec.updatetime) =date(now());"
    second_no_suppl_total_result = int(select(second_no_suppl_total_sql)[0]["second_no_suppl_total"])
    second_no_fish_total_result = int(select(second_no_fish_total_sql)[0]["second_no_fish_total"])
    second_no_record_total_result = int(select(second_no_record_total)[0]["second_no_record_total"])
    second_no_total = str(second_no_suppl_total_result + second_no_fish_total_result + second_no_record_total_result)
    #print(second_total)
    #封堵域名量
    block_domain_total_sql = "select count(*) fengdu_domain_total from t_blacklist t where date(t.blocktime) =date(now());"
    block_domain_total_result = select(block_domain_total_sql)[0]["fengdu_domain_total"]
    block_domain_total = str(block_domain_total_result)
    #print(block_domain_total)
    #内网网站数
    internal_total_sql = "SELECT COUNT(ff.domain) AS internal_total FROM ( SELECT domain, createtime FROM t_domain_record WHERE 1 = 1 AND secondauditstatus = 4 UNION ALL SELECT domain, createtime FROM t_fish_domain WHERE 1 = 1 AND secondauditstatus = 4 UNION ALL SELECT domain, createtime FROM t_supplements_domain WHERE 1 = 1 AND secondauditstatus = 4 ) ff WHERE date(ff.createtime) = date(now());"
    internal_total_result = select(internal_total_sql)[0]["internal_total"]
    internal_total = str(internal_total_result)
    #print(internal_total)
    #知名网站数
    famous_total_sql = "SELECT COUNT(aa.domain) AS famous_total FROM ( SELECT domain, createtime FROM t_domain WHERE 1 = 1 AND secondauditstatus = 3 UNION ALL SELECT domain, createtime FROM t_fish_domain WHERE 1 = 1 AND secondauditstatus = 3 UNION ALL SELECT domain, createtime FROM t_supplements_domain WHERE 1 = 1 AND secondauditstatus = 3 ) aa WHERE date(aa.createtime) = date(now());"
    famous_total_result = select(famous_total_sql)[0]["famous_total"]
    famous_total = str(famous_total_result)
    #print(famous_total)
    #插入数据至网管数据库表：t_nm_domain_audit_total_monitor
    insertSQL ="INSERT INTO `t_nm_domain_audit_total_monitor` ( `region_report_total`, `filter_warehouse_total`, `first_total`, `first_no_total`, `second_total`, `second_no_total`,`block_domain_total`,`internal_total`,`famous_total`,`create_date`, `update_date`) VALUES ('"+region_report_total+"', '"+filter_warehouse_total+"', '"+first_total+"', '"+first_no_total+"', '"+second_total+"', '"+second_no_total+"', '"+block_domain_total+"', '"+internal_total+"', '"+famous_total+"', '"+current_time+"', '"+current_time+"');"
    #print(insertSQL)
    insert(insertSQL)
