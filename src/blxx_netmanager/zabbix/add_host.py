# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 2018年8月13日

@author: yanghang

Description:
        1.本脚本用于通过向zabbix-server中添加主机
        2.使用注意：需要将添加的主机以    主机名：ip的形式一行行的记录在host.txt文本中，脚本读取文件获取要添加的主机并将其存成字典
"""
import json
import requests
import os

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

def addHost(tokens,hostname,ip,port,groupid,templateid):
    """添加主机方法"""
    data = {
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": ip,
                "name": hostname,
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": ip,
                        "dns": "",
                        "port": port
                    }
                ],
                "groups": [
                    {
                        "groupid": groupid
                    }
                ],
                "templates": [
                    {
                        "templateid": templateid
                    }
                ],
                "inventory_mode": 0,
            },
            "auth": tokens,
            "id": 1
        }
    request = requests.post(url=url,headers=headers,data=json.dumps(data))
    resultDict = json.loads(request.content)
    print(resultDict['result'])
    return resultDict['result']

def readFile(filepath,filename):
    """
        1.读取filepath下的filename的文件，将其存入字典中
    """
    os.chdir(filepath)
    f = open(filename, 'r')
    result = {}
    for line in f.readlines():
        line = line.strip()
        if not len(line):
            continue
        key = line.split(':')[0].strip()
        value = line.split(':')[1].strip()
        result[key] = value
    f.close()
    #print(result)
    return result

if __name__ == "__main__":
    headers = {'Content-Type': 'application/json-rpc'}
    server_ip = '192.168.2.99'
    url = 'http://%s/zabbix/api_jsonrpc.php' %server_ip
    username = 'Admin'
    passwd = 'zabbix'
    tokens = getToken(username,passwd)
    #批量添加服务器
    #host_dict = {'blxx_netmanager-dmz01':'10.99.128.2','blxx_netmanager-dmz02':'10.99.128.3','blxx_netmanager-nginx01':'10.99.64.9','blxx_netmanager-nginx02':'0.99.64.10','blxx_netmanager-web01':'10.99.64.4','blxx_netmanager-web02':'10.99.64.2','blxx_netmanager-web03':'10.99.64.3','blxx_netmanager-ha01':'10.99.0.6','blxx_netmanager-ha02':'10.99.0.7','blxx_netmanager-get01':'10.99.0.10','blxx_netmanager-get02':'10.99.0.15','blxx_netmanager-get03':'10.99.0.8','blxx_netmanager-get04':'10.99.0.13','blxx_netmanager-get05':'10.99.0.9','blxx_netmanager-get06':'10.99.0.12','blxx_netmanager-get07':'10.99.0.14','blxx_netmanager-get08':'10.99.0.11','blxx_netmanager-nginx03':'10.99.64.7','blxx_netmanager-nginx04':'10.99.64.8','blxx_netmanager-int01':'10.99.64.5','blxx_netmanager-int02':'10.99.64.6'}
    filepath=os.getcwd()
    filename='host.txt'
    host_dict = readFile(filepath, filename)
    #print(host_dict)
    #遍历字典获取主机名和ip地址，并添加
    for (hostname,ip) in host_dict.items():
        try:
            addHost(tokens, hostname, ip, '10050',"8", "10105")
            print("已添加主机ip: "+ip)
        except Exception as e:
            print(e)
            print(ip+'添加失败！')