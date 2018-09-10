# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Created on 2018年7月27日

@author: yanghang

Description:
'''
import time
from kafka import SimpleProducer, KafkaClient
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers = ['10.200.1.X:9092', '10.200.1.X:9092', '10.200.1.X:9092'])
# Assign a topic
topic = 'my-topic'

def test():
    print('begin')
    n = 1
    while (n<=100):
        producer.send(topic, str(n))
        print ("send" + str(n))
        n += 1
        time.sleep(0.5)
    print('done')

if __name__ == '__main__':
    test()