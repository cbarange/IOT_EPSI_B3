# -*- coding: utf-8 -*-
#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time
from datetime import datetime
import pika

GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the circuit
temp_pin = 7
light_pin = 11

def rc_time (temp_pin):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(temp_pin, GPIO.OUT)
    GPIO.output(temp_pin, GPIO.LOW)
    

    #Change the pin back to input
    GPIO.setup(temp_pin, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(temp_pin) == GPIO.LOW):
        count += 1    
    return count

#Catch when script is interupted, cleanup correctly
try:
    # Main loop
    while True:
        credentials = pika.PlainCredentials(username='rbmqUser', password='rbmqPassword')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.17', credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue='firstQueue')
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        msg = dt_string+"|"+str(rc_time(temp_pin))+"|"+str(rc_time(light_pin))
        channel.basic_publish(exchange='', routing_key='firstQueue', body=msg)
        connection.close()

        print({'date': msg.split('|')[0],'temp': msg.split('|')[1],'lum': msg.split('|')[2]})
        # Wait 5 Minutes
        time.sleep(300)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()