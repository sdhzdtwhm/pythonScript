# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Created on 2018年7月12日

@author: yanghang

Description:
'''
import os
import configparser

config = configparser.ConfigParser()

conf_dir = os.path.abspath(os.path.dirname(os.getcwd())+os.path.sep+"\\conf")

os.chdir(conf_dir)

config.read('config.ini',encoding='utf-8')


def get(section, item):
    return config.get(section, item)


def getint(section, item):
    return config.getint(section, item)


def read(ini_file):
    return config.read(ini_file)

def getboolean(section, item):
    return config.getboolean(section, item)

def getSections():
    print(config.sections())
