# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pika
from pymongo import MongoClient

credentials = pika.PlainCredentials(username='rbmqUser', password='rbmqPassword')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.17', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='firstQueue')

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
	
	client = MongoClient('mongodb://192.168.0.17:27017')
	db = client['epsi_iot']
	post_data = {'ds': body.decode("utf-8").split('|')[0],'y': body.decode("utf-8").split('|')[2]}
	result = db.temp.insert_one(post_data)
	post_data = {'ds': body.decode("utf-8").split('|')[0],'y': body.decode("utf-8").split('|')[1]}
	result = db.lum.insert_one(post_data)
	
channel.basic_consume(queue='firstQueue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

