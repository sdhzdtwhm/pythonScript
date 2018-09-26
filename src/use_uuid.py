# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 2018年8月24日

@author: yanghang

Description:
"""
import uuid
s_uuid=str(uuid.uuid1())
print(s_uuid)
l_uuid=s_uuid.split('-')
print(l_uuid)
s_uuid=''.join(l_uuid)
print(s_uuid)