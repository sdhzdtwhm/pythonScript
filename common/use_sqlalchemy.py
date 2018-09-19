#!/usr/local/python3.6.4/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 2018/09/19
@filename: use_sqlalchemy.py
@author: yanghang
Description:
"""
import schedule
import time
from sqlalchemy import create_engine
import pymysql


def get_conn():
    engine = create_engine("mysql+pymysql://root:1qaz2wsx@localhost:3306/monitor?charset=utf8")
    conn = engine.connect()
    return conn

def query(sql):
    conn =  get_conn()
    result = conn.execute(sql)
    print(result)
    return result

sql = "select * from t_device_info"

# schedule.every(2).seconds.do(query(sql))
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
query(sql)