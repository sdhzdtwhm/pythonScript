# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 2018年8月13日
@author: yanghang
Description:
        1.本脚本用于从zabbixserver中同步主机信息至网管数据库中
"""
import json
import requests
import uuid
import datetime
import pymysql

def getToken(username,passwd):
    """获取zabbix-server的token值"""
    data = {
           "jsonrpc": "2.0",
           "method": "user.login",
           "params": {
           "user": username,
           "password": passwd
           },
           "id": 0
          }
    request = requests.post(url=url,headers=headers,data=json.dumps(data))
    tokenDict= json.loads(request.text)
    return tokenDict['result']

def getHosts(tokens):
    """从api中获取主机信息"""
    data = {
         "jsonrpc": "2.0",
         "method": "host.get",
         "params": {
             "output":["hostid","host","name"],
                   },
         "id": 2,
         "auth": tokens,

             }
    request = requests.post(url=url,headers=headers,data=json.dumps(data))
    resultDict = json.loads(request.content)
    #print(resultDict)
    return resultDict['result']

def createID():
    """生成uuid作为主机的id"""
    s_uuid=str(uuid.uuid1())
    l_uuid=s_uuid.split('-')
    s_uuid=''.join(l_uuid)
    return s_uuid

def insert(sql):
    """向网管库中插入数据"""
    conn = pymysql.connect(user='root', passwd='1qaz2wsx',host='127.0.0.1', db='blxx_netmanager',charset='utf8')
    cur = conn.cursor()
    sta=cur.execute(sql)
    if sta==1:
        print('Done')
    else:
        print('Failed')
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    headers = {'Content-Type': 'application/json-rpc'}
    server_ip = '192.168.2.250'
    url = 'http://%s/zabbix/api_jsonrpc.php' %server_ip
    username = 'Admin'
    passwd = 'zabbix'
    tokens = getToken(username,passwd)
    host_list = getHosts(tokens)
    print(host_list)
    for i in host_list:
        #print(i)
        tid = createID()
        device_ip=i['host']
        manage_ip=i['host']
        device_no=i['name']
        device_name=i['name']
        z_h_id=i['hostid']
        #现在时间
        current_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql="INSERT INTO `blxx_netmanager`.`t_nm_device_info` (`id`, `device_ip`, `manage_ip`, `device_no`, `device_name`, `device_type`, `tap_type`, `house_id`, `logic_house_id`, `close_mac_address`, `business_card_mac_address`, `device_used`, `device_company`, `device_os_type`, `frame_no`, `brand`, `model`, `cpu_model`, `cpu_num`, `cpu_frequency`, `memory_size`, `storage_size`, `status`, `z_h_id`, `warning_switch`, `create_id`, `create_time`, `update_id`, `update_time`, `del_flag`, `memo`) VALUES ('"+tid+"', '"+device_ip+"', '"+manage_ip+"', '"+device_no+"', '"+device_name+"', '1', '', '712809a53f074600b237f4c77da2820b', '', '', '', '', '', '1', '', '', '', '', '', '', '', '', '1', '"+z_h_id+"', '1', '1', '"+current_time+"', '1', '"+current_time+"', '0', '');"
        print(sql)
        try:
            insert(sql);
        except Exception as e:
            print(e)
