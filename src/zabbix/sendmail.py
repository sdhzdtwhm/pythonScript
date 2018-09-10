# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 2018年8月13日

@author: yanghang

Description:
        1.本脚本用于通过发送邮件
        2.使用方式python sendmai.py 13716320887@139.com hello test
"""
import smtplib
from email.mime.text import MIMEText
import sys
mail_host = 'smtp.qq.com'  
mail_user = '996883832'
mail_pass = 'sazdbfpxvwffbaja'
mail_postfix = 'qq.com'
def send_mail(to_list,subject,content):
    me = "zabbix 监控告警平台"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = me
    msg['to'] = to_list
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me,to_list,msg.as_string())
        s.close()
        return True
    except Exception as e:
        print(str(e))
        return False
if __name__ == "__main__":
    send_mail(sys.argv[1], sys.argv[2], sys.argv[3])
