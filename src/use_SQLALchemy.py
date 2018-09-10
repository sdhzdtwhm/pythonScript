# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 2018年8月22日

@author: yanghang

Description:
    1.SQLALchemy用法
"""
import sqlalchemy
#查看版本
print(sqlalchemy.__version__)

"""
1.创建连接
2.声明映射
3.创建模式
4.初始化映射类实例
5.创建会话
6.持久化实例对象
"""
#1.创建连接
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:1qaz2wsx@127.0.0.1:3306/sqlalchemy',echo=True)

#2.声明映射文件
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column,INTEGER,String

class User(Base):
    __tablename__ = 'users'
    id = Column(INTEGER,primary_key=True)
    name = Column(String(10))
    password = Column(String(10))

    def __repr__(self):
        return "<User(id='%s',name='%s',password='%s')>" % (self.id,self.name,self.password)

#创建数据库表
User.metadata.create_all(engine)

#创建会话
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

#持久化一个实例对象
ed_user = User(id=2,name='ed',password='edpasd')
session.add(ed_user)
session.commit()