#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the circuit
temp_pin = 7
light_pin = 11

def rc_time (temp_pin):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(temp_pin, GPIO.OUT)
    GPIO.output(temp_pin, GPIO.LOW)
    time.sleep(0.1)

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
        print("Temperature : "+str(rc_time(temp_pin)))
        print("Light : "+str(rc_time(light_pin)))
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()