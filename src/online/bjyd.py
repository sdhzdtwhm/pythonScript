# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     北京移动.py
   Description :
   Author :       yanghang
   date：          2018/1/4
-------------------------------------------------
   Change Activity:
                   2018/1/4:
-------------------------------------------------
"""
# !/usr/bin/python
import pymysql
import datetime
import os
import ftplib
import time
from impala.dbapi import connect

# 定义变量
today = datetime.date.today()
oneday = datetime.timedelta(days=1)
yesterday = today - oneday
first_time = "'"+str(yesterday)+"' 00:00:00"
last_time = "'"+str(yesterday)+"' 23:59:59"
idc="100001, 100002, 100003, 100004"
special="200001"
oldftpdir=str(yesterday)
ftpdir = str(today)
#local_filedir='c://'+str(today)+''
# 定义本地存储csv文件目录
old_local_filedir='/data/csvdir/'+str(yesterday)+''
local_filedir='/data/csvdir/'+str(today)+''
# sql01:精细化封堵指令
sql01_1="SELECT isc.commandid, crd.rule_valuestart, cri.rule_valuestart, isc.create_date FROM info_security_command isc LEFT JOIN command_rule crd ON isc.id = crd.security_command_id AND crd.rule_subtype = 1 LEFT JOIN command_rule cru ON isc.id = cru.security_command_id AND cru.rule_subtype = 2 LEFT JOIN command_rule crk ON isc.id = crk.security_command_id AND crk.rule_subtype = 3 LEFT JOIN command_rule cri ON isc.id = cri.security_command_id AND cri.rule_subtype = 5 WHERE isc.commandtype = 2 AND isc.operationType = 0 AND isc.issued_flag = 1 AND isc.action_reason = '自动封堵' AND crd.rule_valuestart IS NOT NULL AND cri.rule_valuestart IS NOT NULL AND isc.create_date <= '"+str(yesterday)+" 23:59:59' AND isc.house_num IN ("+idc+")"
sql01_2="SELECT isc.commandid, crd.rule_valuestart, cri.rule_valuestart, isc.create_date FROM info_security_command isc LEFT JOIN command_rule crd ON isc.id = crd.security_command_id AND crd.rule_subtype = 1 LEFT JOIN command_rule cru ON isc.id = cru.security_command_id AND cru.rule_subtype = 2 LEFT JOIN command_rule crk ON isc.id = crk.security_command_id AND crk.rule_subtype = 3 LEFT JOIN command_rule cri ON isc.id = cri.security_command_id AND cri.rule_subtype = 5 WHERE isc.commandtype = 2 AND isc.operationType = 0 AND isc.issued_flag = 1 AND isc.action_reason = '自动封堵' AND crd.rule_valuestart IS NOT NULL AND cri.rule_valuestart IS NOT NULL AND isc.create_date <= '"+str(yesterday)+" 23:59:59' AND isc.house_num IN ("+special+")"
# sql02:精细化封堵指令域名去重
sql02_1="SELECT isc.commandid, crd.rule_valuestart, cri.rule_valuestart, isc.create_date FROM info_security_command isc LEFT JOIN command_rule crd ON isc.id = crd.security_command_id AND crd.rule_subtype = 1 LEFT JOIN command_rule cru ON isc.id = cru.security_command_id AND cru.rule_subtype = 2 LEFT JOIN command_rule crk ON isc.id = crk.security_command_id AND crk.rule_subtype = 3 LEFT JOIN command_rule cri ON isc.id = cri.security_command_id AND cri.rule_subtype = 5 WHERE isc.commandtype = 2 AND isc.operationType = 0 AND isc.issued_flag = 1 AND isc.action_reason = '自动封堵' AND crd.rule_valuestart IS NOT NULL AND cri.rule_valuestart IS NOT NULL AND isc.create_date <= '"+str(yesterday)+" 23:59:59' AND isc.house_num IN ("+idc+") GROUP BY crd.rule_valuestart"
sql02_2="SELECT isc.commandid, crd.rule_valuestart, cri.rule_valuestart, isc.create_date FROM info_security_command isc LEFT JOIN command_rule crd ON isc.id = crd.security_command_id AND crd.rule_subtype = 1 LEFT JOIN command_rule cru ON isc.id = cru.security_command_id AND cru.rule_subtype = 2 LEFT JOIN command_rule crk ON isc.id = crk.security_command_id AND crk.rule_subtype = 3 LEFT JOIN command_rule cri ON isc.id = cri.security_command_id AND cri.rule_subtype = 5 WHERE isc.commandtype = 2 AND isc.operationType = 0 AND isc.issued_flag = 1 AND isc.action_reason = '自动封堵' AND crd.rule_valuestart IS NOT NULL AND cri.rule_valuestart IS NOT NULL AND isc.create_date <= '"+str(yesterday)+" 23:59:59' AND isc.house_num IN ("+special+") GROUP BY crd.rule_valuestart"
# sql03:每日自动封堵指令
sql03_1="SELECT isc.commandid, crd.rule_valuestart, cri.rule_valuestart, isc.create_date FROM info_security_command isc LEFT JOIN command_rule crd ON isc.id = crd.security_command_id AND crd.rule_subtype = 1 LEFT JOIN command_rule cru ON isc.id = cru.security_command_id AND cru.rule_subtype = 2 LEFT JOIN command_rule crk ON isc.id = crk.security_command_id AND crk.rule_subtype = 3 LEFT JOIN command_rule cri ON isc.id = cri.security_command_id AND cri.rule_subtype = 5 WHERE isc.commandtype = 2 AND isc.operationType = 0 AND isc.issued_flag = 1 AND isc.action_reason = '自动封堵' AND crd.rule_valuestart IS NOT NULL AND cri.rule_valuestart IS NOT NULL AND isc.create_date >= '"+str(yesterday)+" 00:00:00' AND isc.create_date <= '"+str(yesterday)+" 23:59:59' AND isc.house_num IN ("+idc+")"
sql03_2="SELECT isc.commandid, crd.rule_valuestart, cri.rule_valuestart, isc.create_date FROM info_security_command isc LEFT JOIN command_rule crd ON isc.id = crd.security_command_id AND crd.rule_subtype = 1 LEFT JOIN command_rule cru ON isc.id = cru.security_command_id AND cru.rule_subtype = 2 LEFT JOIN command_rule crk ON isc.id = crk.security_command_id AND crk.rule_subtype = 3 LEFT JOIN command_rule cri ON isc.id = cri.security_command_id AND cri.rule_subtype = 5 WHERE isc.commandtype = 2 AND isc.operationType = 0 AND isc.issued_flag = 1 AND isc.action_reason = '自动封堵' AND crd.rule_valuestart IS NOT NULL AND cri.rule_valuestart IS NOT NULL AND isc.create_date >= '"+str(yesterday)+" 00:00:00' AND isc.create_date <= '"+str(yesterday)+" 23:59:59' AND isc.house_num IN ("+special+")"
# sql04:每日自动封堵指令域名去重
sql04_1="SELECT isc.commandid, crd.rule_valuestart, cri.rule_valuestart, isc.create_date FROM info_security_command isc LEFT JOIN command_rule crd ON isc.id = crd.security_command_id AND crd.rule_subtype = 1 LEFT JOIN command_rule cru ON isc.id = cru.security_command_id AND cru.rule_subtype = 2 LEFT JOIN command_rule crk ON isc.id = crk.security_command_id AND crk.rule_subtype = 3 LEFT JOIN command_rule cri ON isc.id = cri.security_command_id AND cri.rule_subtype = 5 WHERE isc.commandtype = 2 AND isc.operationType = 0 AND isc.issued_flag = 1 AND isc.action_reason = '自动封堵' AND crd.rule_valuestart IS NOT NULL AND cri.rule_valuestart IS NOT NULL AND isc.create_date >= '"+str(yesterday)+" 00:00:00' AND isc.create_date <= '"+str(yesterday)+" 23:59:59' AND isc.house_num IN ("+idc+") GROUP BY crd.rule_valuestart"
sql04_2="SELECT isc.commandid, crd.rule_valuestart, cri.rule_valuestart, isc.create_date FROM info_security_command isc LEFT JOIN command_rule crd ON isc.id = crd.security_command_id AND crd.rule_subtype = 1 LEFT JOIN command_rule cru ON isc.id = cru.security_command_id AND cru.rule_subtype = 2 LEFT JOIN command_rule crk ON isc.id = crk.security_command_id AND crk.rule_subtype = 3 LEFT JOIN command_rule cri ON isc.id = cri.security_command_id AND cri.rule_subtype = 5 WHERE isc.commandtype = 2 AND isc.operationType = 0 AND isc.issued_flag = 1 AND isc.action_reason = '自动封堵' AND crd.rule_valuestart IS NOT NULL AND cri.rule_valuestart IS NOT NULL AND isc.create_date >= '"+str(yesterday)+" 00:00:00' AND isc.create_date <= '"+str(yesterday)+" 23:59:59' AND isc.house_num IN ("+special+") GROUP BY crd.rule_valuestart"
# sql05:IDC+专线现有指令
sql05_1="SELECT * FROM info_security_command WHERE operationType = 0 AND issued_flag = 1"
sql05_2="SELECT * FROM info_security_command WHERE operationType = 0 AND issued_flag = 1"
# sql06:自动封堵
sql06_1="SELECT * FROM info_security_command WHERE operationType = 0 AND issued_flag = 1 AND action_reason = '自动封堵'"
sql06_2="SELECT * FROM info_security_command WHERE operationType = 0 AND issued_flag = 1 AND action_reason = '自动封堵'"
# sql07:拦截涉黄网站
sql07_1="SELECT * FROM info_security_command WHERE operationType = 0 AND issued_flag = 1 AND action_reason = '涉黄'"
sql07_2="SELECT * FROM info_security_command WHERE operationType = 0 AND issued_flag = 1 AND action_reason = '涉黄'"
# sql08:拦截未备案网站
sql08_1="SELECT * FROM info_security_command WHERE operationType = 0 AND issued_flag = 1 AND action_reason = '未备案'"
sql08_2="SELECT * FROM info_security_command WHERE operationType = 0 AND issued_flag = 1 AND action_reason = '未备案'"
# sql09:拦截恶意网站
sql09_1="SELECT * FROM info_security_command WHERE operationType = 0 AND issued_flag = 1 AND action_reason = '恶意网站'"
sql09_2="SELECT * FROM info_security_command WHERE operationType = 0 AND issued_flag = 1 AND action_reason = '恶意网站'"
# sql10:管理IDC网站
sql10_1="SELECT DISTINCT domain_name FROM service_domain sd LEFT JOIN service_info si ON sd.service_id = si.id LEFT JOIN idc_user_data_info iudi ON iudi.id = si.user_data_id LEFT JOIN house_info hinf ON iudi.house_id = hinf.house_num WHERE sd.valid_flag = 1 AND si.valid_flag = 1 AND iudi.valid_flag = 1 AND hinf.valid_flag = 1 AND sd.domain_name IS NOT NULL AND sd.domain_name != '' AND iudi.house_id IN ("+idc+")"
sql10_2="SELECT DISTINCT domain_name FROM service_domain sd LEFT JOIN service_info si ON sd.service_id = si.id LEFT JOIN idc_user_data_info iudi ON iudi.id = si.user_data_id LEFT JOIN house_info hinf ON iudi.house_id = hinf.house_num WHERE sd.valid_flag = 1 AND si.valid_flag = 1 AND iudi.valid_flag = 1 AND hinf.valid_flag = 1 AND sd.domain_name IS NOT NULL AND sd.domain_name != '' AND iudi.house_id IN ("+special+")"
# sql11:管理IP段
sql11_1="SELECT DISTINCT concat(it.start_ip, '-', it.end_ip) FROM ip_trans it LEFT JOIN house_hold_info hhi ON hhi.id = it.hhid LEFT JOIN service_info si ON si.id = hhi.service_id LEFT JOIN idc_user_data_info iudi ON iudi.id = si.user_data_id LEFT JOIN house_info hi ON hi.house_num = iudi.house_id WHERE it.valid_flag = 1 AND hhi.valid_flag = 1 AND si.valid_flag = 1 AND iudi.valid_flag = 1 AND hi.valid_flag = 1 AND hi.house_num in ("+idc+")"
sql11_2="SELECT DISTINCT concat(it.start_ip, '-', it.end_ip) FROM ip_trans it LEFT JOIN house_hold_info hhi ON hhi.id = it.hhid LEFT JOIN service_info si ON si.id = hhi.service_id LEFT JOIN idc_user_data_info iudi ON iudi.id = si.user_data_id LEFT JOIN house_info hi ON hi.house_num = iudi.house_id WHERE it.valid_flag = 1 AND hhi.valid_flag = 1 AND si.valid_flag = 1 AND iudi.valid_flag = 1 AND hi.valid_flag = 1 AND hi.house_num in ("+special+")"
# sql12:现有客户数
sql12_1="SELECT iudi.name FROM idc_user_data_info iudi LEFT JOIN house_info hi ON iudi.house_id = hi.house_num WHERE hi.valid_flag = 1 AND iudi.valid_flag = 1 AND iudi.house_id IN ("+idc+")"
sql12_2="SELECT iudi.name FROM idc_user_data_info iudi LEFT JOIN house_info hi ON iudi.house_id = hi.house_num WHERE hi.valid_flag = 1 AND iudi.valid_flag = 1 AND iudi.house_id IN ("+special+")"
# sql13:管局下发指令
sql13_2="SELECT commandid, commandxml FROM `command_task` WHERE commandid IS NOT NULL AND commandid NOT RLIKE '99999999' AND commandid > 9999999999 AND create_date >= '"+str(yesterday)+" 00:00:00' AND create_date <= '"+str(yesterday)+" 23:59:59' AND (commandxml like '%200001%')"
sql13_1="SELECT commandid, commandxml FROM `command_task` WHERE commandid IS NOT NULL AND commandid NOT RLIKE '99999999' AND commandid > 9999999999 AND create_date >= '"+str(yesterday)+" 00:00:00' AND create_date <= '"+str(yesterday)+" 23:59:59' AND (commandxml like '%100001%' or commandxml like '%100002%' or commandxml like '%100003%' or commandxml like '%100004%')"
# sql14:管局下发指令成功
sql14_2="SELECT commandid, commandxml, status FROM `command_task` WHERE commandid IS NOT NULL AND commandid NOT RLIKE '99999999' AND commandid > 9999999999 AND create_date >= '"+str(yesterday)+" 00:00:00' AND create_date <= '"+str(yesterday)+" 23:59:59' AND (commandxml like '%200001%') AND status = 9"
sql14_1="SELECT commandid, commandxml, status FROM `command_task` WHERE commandid IS NOT NULL AND commandid NOT RLIKE '99999999' AND commandid > 9999999999 AND create_date >= '"+str(yesterday)+" 00:00:00' AND create_date <= '"+str(yesterday)+" 23:59:59' AND (commandxml like '%100001%' or commandxml like '%100002%' or commandxml like '%100003%' or commandxml like '%100004%') AND status = 9"
# sql15:工信部下发指令
sql15_2="SELECT commandid, commandxml FROM `command_task` WHERE commandid IS NOT NULL AND commandid NOT RLIKE '99999999' AND commandid <= 9999999999 AND create_date >= '"+str(yesterday)+" 00:00:00' AND create_date <= '"+str(yesterday)+" 23:59:59' AND (commandxml like '%200001%')"
sql15_1="SELECT commandid, commandxml FROM `command_task` WHERE commandid IS NOT NULL AND commandid NOT RLIKE '99999999' AND commandid <= 9999999999 AND create_date >= '"+str(yesterday)+" 00:00:00' AND create_date <= '"+str(yesterday)+" 23:59:59' AND (commandxml like '%100001%' or commandxml like '%100002%' or commandxml like '%100003%' or commandxml like '%100004%')"
# sql16:工信部下发指令成功
sql16_2="SELECT commandid, commandxml, status FROM `command_task` WHERE commandid IS NOT NULL AND commandid NOT RLIKE '99999999' AND commandid <= 9999999999 AND create_date >= '"+str(yesterday)+" 00:00:00' AND create_date <= '"+str(yesterday)+" 23:59:59' AND (commandxml like '%200001%') AND status = 9"
sql16_1="SELECT commandid, commandxml, status FROM `command_task` WHERE commandid IS NOT NULL AND commandid NOT RLIKE '99999999' AND commandid <= 9999999999 AND create_date >= '"+str(yesterday)+" 00:00:00' AND create_date <= '"+str(yesterday)+" 23:59:59' AND (commandxml like '%100001%' or commandxml like '%100002%' or commandxml like '%100003%' or commandxml like '%100004%') AND status = 9"
# sql17:恶意软件封堵URL
sql17_1="SELECT * FROM info_security_command isc LEFT JOIN command_rule cr ON isc.id = cr.security_command_id AND cr.rule_subtype = 2 WHERE isc.commandtype = 2 AND isc.operationType = 0 AND isc.issued_flag = 1 AND cr.rule_valuestart IS NOT NULL AND isc.commandid RLIKE '99999999'"
sql17_2="SELECT * FROM info_security_command isc LEFT JOIN command_rule cr ON isc.id = cr.security_command_id AND cr.rule_subtype = 2 WHERE isc.commandtype = 2 AND isc.operationType = 0 AND isc.issued_flag = 1 AND cr.rule_valuestart IS NOT NULL AND isc.commandid RLIKE '99999999'"

# impala:活跃资源
impalaSQL01_1="SELECT ari.ip, ari.ip_long, ari.domain, ari.first_domain, ari.first_time , ari.last_time, ari.PORT, ari.visits_count, ari.houseid, ari.ds FROM active_resource_info ari WHERE ari.ds = '"+str(yesterday)+"' AND ari.houseid IN ("+idc+")"
impalaSQL01_2="SELECT ari.ip, ari.ip_long, ari.domain, ari.first_domain, ari.first_time , ari.last_time, ari.PORT, ari.visits_count, ari.houseid, ari.ds FROM active_resource_info ari WHERE ari.ds = '"+str(yesterday)+"' AND ari.houseid IN ("+special+")"
# impala:活跃资源按域名去重
impalaSQL02_1="SELECT MAX(ari.ip), MAX(ari.ip_long) , MAX(ari.domain), ari.first_domain , MAX(ari.first_time), MAX(ari.last_time) , MAX(ari.PORT), MAX(ari.visits_count) , MAX(ari.houseid), MAX(ari.ds) FROM active_resource_info ari WHERE ari.ds = '"+str(yesterday)+"' AND ari.houseid IN ("+idc+") GROUP BY ari.first_domain"
impalaSQL02_2="SELECT MAX(ari.ip), MAX(ari.ip_long) , MAX(ari.domain), ari.first_domain , MAX(ari.first_time), MAX(ari.last_time) , MAX(ari.PORT), MAX(ari.visits_count) , MAX(ari.houseid), MAX(ari.ds) FROM active_resource_info ari WHERE ari.ds = '"+str(yesterday)+"' AND ari.houseid IN ("+special+") GROUP BY ari.first_domain"
# impala:异常活跃资源
impalaSQL03_1="SELECT a.ipaddr AS ipaddr, a.ipaddrlong AS ipaddrlong, a.domain AS domain, a.firstdomain AS firstdomain, a.first_time AS first_time , a.last_time AS last_time, a.PORT AS PORT, a.visitscount AS visitscount, a.houseid AS houseid, a.ds AS ds FROM ( SELECT tdd.ip AS ipaddr, tdd.ip_long AS ipaddrlong, tdd.domain AS domain, tdd.houseid AS houseid, tdd.PORT AS PORT , tdd.first_domain AS firstdomain, tdd.protocol AS protocol, tdd.visits_count AS visitscount, tdd.ds AS ds , MIN(tdd.first_time) AS first_time, MAX(tdd.last_time) AS last_time , bas.domain_name AS domainname , CASE  WHEN bas.use_type = 2 THEN 1 WHEN find_in_set(tdd.first_domain, bas.domain_name) = 0 THEN 2 WHEN bas.start_ip = '' OR bas.start_ip IS NULL THEN 3 ELSE 0 END AS domainflag FROM active_resource_info tdd LEFT JOIN basic_data_info bas ON tdd.ip_long >= bas.startiplong AND tdd.ip_long <= bas.endiplong WHERE 1 = 1 AND ((tdd.first_time >= '"+str(yesterday)+" 00:00:00' AND tdd.first_time < '"+str(yesterday)+" 23:59:59') OR (tdd.last_time >= '"+str(yesterday)+" 00:00:00' AND tdd.last_time < '"+str(yesterday)+" 23:59:59') OR (tdd.first_time <= '"+str(yesterday)+" 00:00:00' AND tdd.last_time >= '"+str(yesterday)+" 23:59:59')) AND tdd.houseid IN ("+idc+") AND tdd.ds = '"+str(yesterday)+"' AND tdd.first_domain != 'null' GROUP BY tdd.houseid, tdd.domain, tdd.first_domain, tdd.ip, tdd.ip_long, tdd.PORT, tdd.visits_count, tdd.ds, tdd.protocol, bas.use_type, bas.domain_name, bas.start_ip ) a WHERE a.domainflag = 2"
impalaSQL03_2="SELECT a.ipaddr AS ipaddr, a.ipaddrlong AS ipaddrlong, a.domain AS domain, a.firstdomain AS firstdomain, a.first_time AS first_time , a.last_time AS last_time, a.PORT AS PORT, a.visitscount AS visitscount, a.houseid AS houseid, a.ds AS ds FROM ( SELECT tdd.ip AS ipaddr, tdd.ip_long AS ipaddrlong, tdd.domain AS domain, tdd.houseid AS houseid, tdd.PORT AS PORT , tdd.first_domain AS firstdomain, tdd.protocol AS protocol, tdd.visits_count AS visitscount, tdd.ds AS ds , MIN(tdd.first_time) AS first_time, MAX(tdd.last_time) AS last_time , bas.domain_name AS domainname , CASE  WHEN bas.use_type = 2 THEN 1 WHEN find_in_set(tdd.first_domain, bas.domain_name) = 0 THEN 2 WHEN bas.start_ip = '' OR bas.start_ip IS NULL THEN 3 ELSE 0 END AS domainflag FROM active_resource_info tdd LEFT JOIN basic_data_info bas ON tdd.ip_long >= bas.startiplong AND tdd.ip_long <= bas.endiplong WHERE 1 = 1 AND ((tdd.first_time >= '"+str(yesterday)+" 00:00:00' AND tdd.first_time < '"+str(yesterday)+" 23:59:59') OR (tdd.last_time >= '"+str(yesterday)+" 00:00:00' AND tdd.last_time < '"+str(yesterday)+" 23:59:59') OR (tdd.first_time <= '"+str(yesterday)+" 00:00:00' AND tdd.last_time >= '"+str(yesterday)+" 23:59:59')) AND tdd.houseid IN ("+special+") AND tdd.ds = '"+str(yesterday)+"' AND tdd.first_domain != 'null' GROUP BY tdd.houseid, tdd.domain, tdd.first_domain, tdd.ip, tdd.ip_long, tdd.PORT, tdd.visits_count, tdd.ds, tdd.protocol, bas.use_type, bas.domain_name, bas.start_ip ) a WHERE a.domainflag = 2"
# impala:异常活跃资源按域名去重
impalaSQL04_1="SELECT a.ipaddr AS ipaddr, a.ipaddrlong AS ipaddrlong, a.domain AS domain, a.firstdomain AS firstdomain, a.first_time AS first_time , a.last_time AS last_time, a.PORT AS PORT, a.visitscount AS visitscount, a.houseid AS houseid, a.ds AS ds FROM ( SELECT MAX(tdd.ip) AS ipaddr, MAX(tdd.ip_long) AS ipaddrlong , MAX(tdd.domain) AS domain, MAX(tdd.houseid) AS houseid , MAX(tdd.PORT) AS PORT, tdd.first_domain AS firstdomain , MAX(tdd.protocol) AS protocol, MAX(tdd.visits_count) AS visitscount , MAX(tdd.ds) AS ds, MIN(tdd.first_time) AS first_time , MAX(tdd.last_time) AS last_time, MAX(bas.domain_name) AS domainname , MAX(CASE  WHEN bas.use_type = 2 THEN 1 WHEN find_in_set(tdd.first_domain, bas.domain_name) = 0 THEN 2 WHEN bas.start_ip = '' OR bas.start_ip IS NULL THEN 3 ELSE 0 END) AS domainflag FROM active_resource_info tdd LEFT JOIN basic_data_info bas ON tdd.ip_long >= bas.startiplong AND tdd.ip_long <= bas.endiplong WHERE 1 = 1 AND ((tdd.first_time >= '"+str(yesterday)+" 00:00:00' AND tdd.first_time < '"+str(yesterday)+" 23:59:59') OR (tdd.last_time >= '"+str(yesterday)+" 00:00:00' AND tdd.last_time < '"+str(yesterday)+" 23:59:59') OR (tdd.first_time <= '"+str(yesterday)+" 00:00:00' AND tdd.last_time >= '"+str(yesterday)+" 23:59:59')) AND tdd.houseid IN ("+idc+") AND tdd.ds = '"+str(yesterday)+"' AND tdd.first_domain != 'null' GROUP BY tdd.first_domain ) a WHERE a.domainflag = 2"
impalaSQL04_2="SELECT a.ipaddr AS ipaddr, a.ipaddrlong AS ipaddrlong, a.domain AS domain, a.firstdomain AS firstdomain, a.first_time AS first_time , a.last_time AS last_time, a.PORT AS PORT, a.visitscount AS visitscount, a.houseid AS houseid, a.ds AS ds FROM ( SELECT MAX(tdd.ip) AS ipaddr, MAX(tdd.ip_long) AS ipaddrlong , MAX(tdd.domain) AS domain, MAX(tdd.houseid) AS houseid , MAX(tdd.PORT) AS PORT, tdd.first_domain AS firstdomain , MAX(tdd.protocol) AS protocol, MAX(tdd.visits_count) AS visitscount , MAX(tdd.ds) AS ds, MIN(tdd.first_time) AS first_time , MAX(tdd.last_time) AS last_time, MAX(bas.domain_name) AS domainname , MAX(CASE  WHEN bas.use_type = 2 THEN 1 WHEN find_in_set(tdd.first_domain, bas.domain_name) = 0 THEN 2 WHEN bas.start_ip = '' OR bas.start_ip IS NULL THEN 3 ELSE 0 END) AS domainflag FROM active_resource_info tdd LEFT JOIN basic_data_info bas ON tdd.ip_long >= bas.startiplong AND tdd.ip_long <= bas.endiplong WHERE 1 = 1 AND ((tdd.first_time >= '"+str(yesterday)+" 00:00:00' AND tdd.first_time < '"+str(yesterday)+" 23:59:59') OR (tdd.last_time >= '"+str(yesterday)+" 00:00:00' AND tdd.last_time < '"+str(yesterday)+" 23:59:59') OR (tdd.first_time <= '"+str(yesterday)+" 00:00:00' AND tdd.last_time >= '"+str(yesterday)+" 23:59:59')) AND tdd.houseid IN ("+special+") AND tdd.ds = '"+str(yesterday)+"' AND tdd.first_domain != 'null' GROUP BY tdd.first_domain ) a WHERE a.domainflag = 2"
# impala:ISP活跃资源
impalaSQL05_1="SELECT idl.ip, idl.ip_long, idl.domain, idl.first_domain, idl.first_time , idl.last_time, idl.PORT, idl.visits_count, idl.houseid, idl.ds FROM active_resource_info idl LEFT JOIN basic_data_info bas ON idl.ip_long >= bas.startiplong AND idl.ip_long <= bas.endiplong LEFT JOIN user_isp_info uii ON bas.user_id = uii.user_id WHERE uii.user_id IS NOT NULL AND idl.first_domain <> '' AND idl.first_domain <> 'null' AND idl.last_time >= '"+str(yesterday)+" 00:00:00' AND idl.last_time <= '"+str(yesterday)+" 23:59:59' AND idl.ds = '"+str(yesterday)+"' AND idl.houseid IN ("+idc+")"
impalaSQL05_2="SELECT idl.ip, idl.ip_long, idl.domain, idl.first_domain, idl.first_time , idl.last_time, idl.PORT, idl.visits_count, idl.houseid, idl.ds FROM active_resource_info idl LEFT JOIN basic_data_info bas ON idl.ip_long >= bas.startiplong AND idl.ip_long <= bas.endiplong LEFT JOIN user_isp_info uii ON bas.user_id = uii.user_id WHERE uii.user_id IS NOT NULL AND idl.first_domain <> '' AND idl.first_domain <> 'null' AND idl.last_time >= '"+str(yesterday)+" 00:00:00' AND idl.last_time <= '"+str(yesterday)+" 23:59:59' AND idl.ds = '"+str(yesterday)+"' AND idl.houseid IN ("+special+")"
# impala:ISP活跃资源按域名去重
impalaSQL06_1="SELECT MAX(idl.ip), MAX(idl.ip_long) , MAX(idl.domain), idl.first_domain , MAX(idl.first_time), MAX(idl.last_time) , MAX(idl.PORT), MAX(idl.visits_count) , MAX(idl.houseid), MAX(idl.ds) FROM active_resource_info idl LEFT JOIN basic_data_info bas ON idl.ip_long >= bas.startiplong AND idl.ip_long <= bas.endiplong LEFT JOIN user_isp_info uii ON bas.user_id = uii.user_id WHERE uii.user_id IS NOT NULL AND idl.first_domain <> '' AND idl.first_domain <> 'null' AND idl.last_time >= '"+str(yesterday)+" 00:00:00' AND idl.last_time <= '"+str(yesterday)+" 23:59:59' AND idl.ds = '"+str(yesterday)+"' AND idl.houseid IN ("+idc+") GROUP BY idl.first_domain"
impalaSQL06_2="SELECT MAX(idl.ip), MAX(idl.ip_long) , MAX(idl.domain), idl.first_domain , MAX(idl.first_time), MAX(idl.last_time) , MAX(idl.PORT), MAX(idl.visits_count) , MAX(idl.houseid), MAX(idl.ds) FROM active_resource_info idl LEFT JOIN basic_data_info bas ON idl.ip_long >= bas.startiplong AND idl.ip_long <= bas.endiplong LEFT JOIN user_isp_info uii ON bas.user_id = uii.user_id WHERE uii.user_id IS NOT NULL AND idl.first_domain <> '' AND idl.first_domain <> 'null' AND idl.last_time >= '"+str(yesterday)+" 00:00:00' AND idl.last_time <= '"+str(yesterday)+" 23:59:59' AND idl.ds = '"+str(yesterday)+"' AND idl.houseid IN ("+special+") GROUP BY idl.first_domain"


special_csv_name_list=['专线-精细化封堵指令.csv','专线-精细化封堵指令域名去重.csv','专线-每日自动封堵指令.csv','专线-每日自动封堵指令域名去重.csv','专线-IDC+专线现有指令.csv','专线-自动封堵.csv','专线-拦截涉黄网站.csv','专线-拦截未备案网站.csv','专线-拦截恶意网站.csv','专线-管理IDC网站.csv','专线-管理IP段.csv','专线-现有客户数.csv','专线-管局下发指令.csv','专线-管局下发指令成功.csv','专线-工信部下发指令.csv','专线-工信部下发指令成功.csv','专线-恶意软件封堵URL.csv']
idc_csv_name_list=['IDC-精细化封堵指令.csv','IDC-精细化封堵指令域名去重.csv','IDC-每日自动封堵指令.csv','IDC-每日自动封堵指令域名去重.csv','IDC-IDC+专线现有指令.csv','IDC-自动封堵.csv','IDC-拦截涉黄网站.csv','IDC-拦截未备案网站.csv','IDC-拦截恶意网站.csv','IDC-管理IDC网站.csv','IDC-管理IP段.csv','IDC-现有客户数.csv','IDC-管局下发指令.csv','IDC-管局下发指令成功.csv','IDC-工信部下发指令.csv','IDC-工信部下发指令成功.csv','IDC-恶意软件封堵URL.csv']

#impala_special_csv_list=['专线-活跃资源.csv','专线-活跃资源按域名去重.csv','专线-异常活跃资源.csv','专线-异常活跃资源按域名去重.csv','专线-ISP活跃资源.csv','专线-ISP活跃资源按域名去重.csv']
#impala_idc_csv_list=['IDC-活跃资源.csv','IDC-活跃资源按域名去重.csv','IDC-异常活跃资源.csv','IDC-异常活跃资源按域名去重.csv','IDC-ISP活跃资源.csv','IDC-ISP活跃资源按域名去重.csv']

impala_special_csv_list=['专线-活跃资源.csv','专线-活跃资源按域名去重.csv','专线-异常活跃资源.csv','专线-ISP活跃资源.csv','专线-ISP活跃资源按域名去重.csv']
impala_idc_csv_list=['IDC-活跃资源.csv','IDC-活跃资源按域名去重.csv','IDC-异常活跃资源.csv','IDC-ISP活跃资源.csv','IDC-ISP活跃资源按域名去重.csv']

# 定义sql执行函数
def execude_sql(args):
    #con = pymysql.connect('172.16.0.7', 'root', 'mvtech@123', 'isms_bjyd', charset='utf8')
    con = pymysql.connect('221.179.144.116', 'root', 'mvtech@123', 'isms_bjyd', charset='utf8')
    cur = con.cursor()
    cur.execute(args)
    result = cur.fetchall()
    result = list(result)
    cur.close()
    con.close()
    return result
# 定义mysql_init函数，输入sql变量和要导出的文件名即可产生文件夹
def mysql_init(sql,csv_name):
    result = execude_sql(sql)
    os.chdir(local_filedir)
    # 定义导出csv文件函数
    def exp_csv(exp_file):
        with open(exp_file, 'wb') as f:
            for item in result:
                try:
                    line = ','.join(str(s) for s in item) + '\n'
                    f.write(line.encode('utf-8'))
                except Exception as e:
                    print(e)
                    break
    exp_csv(csv_name)
# 定义impala_sql执行函数
def execude_impala_sql(args):
    #conn = connect(host='172.16.0.9', port=21050,timeout=3600)
    conn = connect(host='192.168.4.154', port=21050,timeout=3600)
    cur = conn.cursor()
    cur.execute(args)
    result = cur.fetchall()
    result = list(result)
    cur.close()
    conn.close()
    return result
# 定义impala_init函数
def impala_init(impalaSQL,impalaFile):
    os.chdir(local_filedir)
    result = execude_impala_sql(impalaSQL)
    os.chdir(local_filedir)
    # 定义导出csv文件函数
    def exp_csv(exp_file):
        with open(exp_file, 'wb') as f:
            for item in result:
                try:
                    line = ','.join(str(s) for s in item) + '\n'
                    f.write(line.encode('utf-8'))
                except Exception as e:
                    print(e)
                    break
    exp_csv(impalaFile)

# mysql主函数
def mysql_main(sql_list,csv_name_list):
    i = 0
    for sql in sql_list:
        csv_name = csv_name_list[i]
        try:
            print("即将开始导出")
            mysql_init(sql, csv_name)
            print("%s导出完毕" % csv_name)
        except Exception as e:
            print("%s导出报错" % csv_name)
            print("sql语句:%s" % sql)
            print(e)
        i = i + 1

# impala主函数
def impala_main(impala_list,impala_csv_list):
    i = 0
    for impalaSQL in impala_list:
        impalaFile = impala_csv_list[i]
        try:
            print("即将开始导出")
            impala_init(impalaSQL, impalaFile)
            print("%s导出完毕" % impalaFile)
        except Exception as e:
            print("%s导出报错" % impalaFile)
            print("impala-sql语句:%s" % impalaSQL)
            print(e)
        i = i + 1
# ftp上传文件函数
def scanfile(path,ftpdir):
    filelist = os.listdir(path)
    os.chdir(path)
    ftp = ftplib.FTP("172.16.0.5")
    ftp.login("csvfile", "1qaz2wsx3edc")
    #删除昨天的文件夹
    try:
        ftp.cwd(oldftpdir)
        for i in ftp.nlst():
            ftp.delete(i)
        ftp.cwd('/')
        ftp.rmd(oldftpdir)
    except Exception as e:
        print(e)
    #创建今天ftp目录
    try:
        ftp.mkd(ftpdir)
    except Exception as e:
        print(e)
    ftp.cwd(ftpdir)
    for filename in filelist:
        ftp.storbinary("STOR " + filename, open(filename, "rb" ))
    ftp.quit()
# 执行函数
if __name__=="__main__":
    # 创建文件夹
    os.system("mkdir -p %s" % local_filedir)
    # try:
    #     os.mkdir(local_filedir)
    # except Exception as e:
    #     print(e)
    # 删除昨天的文件
    #os.system("rm -rf %s"% old_local_filedir)
    #refresh_impala
    # 导出mysql-IDC数据
    idc_list = [sql01_1, sql02_1, sql03_1, sql04_1, sql05_1, sql06_1, sql07_1, sql08_1, sql09_1, sql10_1, sql11_1, sql12_1, sql13_1,sql14_1, sql15_1, sql16_1, sql17_1]
    # for i in idc_list:
    #     print(i)
    #mysql_main(idc_list, idc_csv_name_list)
    impala_list=[impalaSQL01_1,impalaSQL02_1,impalaSQL03_1,impalaSQL05_1,impalaSQL06_1]
    #impala_list=[impalaSQL01_1,impalaSQL02_1,impalaSQL03_1,impalaSQL04_1,impalaSQL05_1,impalaSQL06_1]
    # for i in impala_list:
    #     print(i)
    #impala_main(impala_list,impala_idc_csv_list)
    # 导出mysql-专线数据
    special_list = [sql01_2, sql02_2, sql03_2, sql04_2, sql05_2, sql06_2, sql07_2, sql08_2, sql09_2, sql10_2, sql11_2, sql12_2, sql13_2, sql14_2,sql15_2, sql16_2, sql17_2]
    # for i in special_list:
    #     print(i)
    # 导出mysql专线数据
    #mysql_main(special_list, special_csv_name_list)
    # 导出impala-专线数据
    #impala_list = [impalaSQL01_2, impalaSQL02_2, impalaSQL03_2, impalaSQL04_2, impalaSQL05_2, impalaSQL06_2]
    impala_list = [impalaSQL01_2, impalaSQL02_2, impalaSQL03_2, impalaSQL05_2, impalaSQL06_2]
    # for i in impala_list:
    #     print(i)
    # 导出专线impala
    #impala_main(impala_list, impala_special_csv_list)
    # 将文件上传至ftp中
    #allfile = scanfile(local_filedir, ftpdir)