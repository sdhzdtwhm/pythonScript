# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 2018年8月27日

@author: yanghang

Description:
"""
import json
import requests

def getToken(url,headers,username,passwd):
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

def getHostids(tokens):
    """从api中获取主机信息"""
    data = {
         "jsonrpc": "2.0",
         "method": "host.get",
         "params": {
             "output": [
                 "host",
                 ],
        "filter": {
               "status":0,#0为被监控的，1为不被监控的
        }
                   },
         "id": 2,
         "auth": tokens,
             }
    request = requests.post(url=url,headers=headers,data=json.dumps(data))
    resultDict = json.loads(request.content)
    #print(resultDict)
    return resultDict['result']

def getItemidByHost(tokens,host):
    """从api中获取主机信息"""
    data = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": ["hostid","itemid","name"],
        "filter": {
            "host":host
        }
                   },
         "id": 2,
         "auth": tokens,
             }
    request = requests.post(url=url,headers=headers,data=json.dumps(data))
    resultDict = json.loads(request.content)
    #print(resultDict)
    return resultDict['result']

def getHistory(tokens,history_type,hostids,itemids):
    """通过给定的hostid和itemid获取最新的值"""
    data = {
         "jsonrpc": "2.0",
         "method": "history.get",
         "params": {
                "output": "extend",
                #"history": "0",
                "history": history_type,
                "hostids": hostids,
                 "itemids": itemids,
                "sortfield": "clock",
                "sortorder": "DESC",
                "limit": 1,
                   },
         "id": 1,
         "auth": tokens,
             }
    request = requests.post(url=url,headers=headers,data=json.dumps(data))
    resultDict = json.loads(request.content)
    #print(resultDict)
    return resultDict['result']

if __name__ == '__main__':
    headers = {'Content-Type': 'application/json-rpc'}
    server_ip = '192.168.2.51'
    url = 'http://%s/zabbix/api_jsonrpc.php' %server_ip
    username = 'Admin'
    passwd = 'zabbix'
    tokens = getToken(url,headers,username,passwd)
    #获取主机列表
    host_list = getHostids(tokens)
    #print(host_list)
    #遍历主机列表获取每个主机包含的item
    for i in host_list:
        item_list = getItemidByHost(tokens,i['host'])
        print(item_list)
        #将hostid和itemid传入getHistory()方法中获取items的参数
        for j in item_list:
            for history_type in range(5):#传入k值，遍历所有的history类型
                amd1 = getHistory(tokens,history_type,i["hostid"], j['itemid'])
                if len(amd1):
                    #print("hostid="+str(i)+":"+str(getHistory(tokens,i, j['itemid'])))
                    print("host="+str(i["host"])+" itemname="+str(j["name"])+":"+str(getHistory(tokens,history_type,i["hostid"], j['itemid'])))
                else:
                    continue