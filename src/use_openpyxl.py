# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 2018年8月16日

@author: yanghang

Description:
"""
import os
import openpyxl

os.chdir("d://")

wb = openpyxl.load_workbook('keyword.xlsx')
sheet_list = wb.sheetnames
print(sheet_list)
print(sheet_list[0])