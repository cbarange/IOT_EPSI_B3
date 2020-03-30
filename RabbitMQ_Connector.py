# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials(username='rbmqUser', password='rbmqPassword')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.17', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='firstQueue')

channel.basic_publish(exchange='', routing_key='firstQueue', body='Hello World!')
msg = "HelloWorld"
print(" [x] Sent '"+msg+"'")
connection.close()
