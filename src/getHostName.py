# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Created on 2018年7月30日

@author: yanghang

Description:
'''
import os

def hostname():
        sys = os.name

        if sys == 'nt':
                hostname = os.getenv('computername')
                return hostname

        elif sys == 'posix':
                host = os.popen('echo $HOSTNAME')
                try:
                        hostname = host.read()
                        return hostname
                finally:
                        host.close()
        else:
                return 'Unkwon hostname'

hostname()