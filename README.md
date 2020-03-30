# Cours 4 DonneesEtObjetConnectes

## Liens tutoriels

https://www.locoduino.org/spip.php?article216
 
http://johnny-five.io/examples/
 
https://github.com/rwaldron/johnny-five/wiki/Getting-started-with-Johnny-Five-and-Proteus
 
https://www.pubnub.com/blog/howcreate-a-smart-device-with-arduino-and-node-js-using-johnny-five/
 
https://facebook.github.io/prophet/docs/quick_start.html

https://www.theengineeringprojects.com/2015/12/arduino-library-proteus-simulation.html
 
https://medium.com/@imtiaz101325/using-johnny-five-with-proteus-on-ubuntu-70f6b0c39591
 
http://blog.ricardofilipe.com/post/getting-started-arduino-johhny-five

## Description du projet

Recuperer 
	* Température 
	* Luminosité
	* Date + heure
Envoyer les données toutes les 2 minutes sur le serveur RabbitMQ

Le serveur RabbitMQ enregistre les données dans une base de données MongoDB

Une api python fbprophet / spark permet de recuperer les données plus de la prévision

Un site web affiche les données dans un graphique

## Réalisation

1. Développement programme python qui envoie toutes les deux minutes:
	* Température
	* Luminosité
	* Date(heure)
2. Mise en place d'un RabbitMQ
2. (bis) peut etre besoin de développer un middle-ware, si RabbitMQ n'est pas capable de faire des inserts en base
3. Mise en place d'un MongoDB
4. Développement de l'api python
5. Développement du site web

## RabbitMQ
```bash
sudo apt install rabbitmq-server
sudo service rabbitmq-server start
sudo service rabbitmq-server status

sudo rabbitmqctl add_user rbmqUser rbmqPassword
sudo rabbitmqctl set_user_tags rbmqUser administrator
sudo rabbitmqctl set_permissions -p / rbmqUser ".*" ".*" ".*"
```
```python
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
```
```python
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
```

## MongoDB
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
sudo apt-get install gnupg
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
sudo apt-get update
sudo apt-get install -y mongodb-org

service mongod status
sudo service mongod start
mongo

sudo nano /etc/mongod.conf
# net: bindIp : 0.0.0.0


use first
db.myCollection.insertOne( { x: 1 } )

db.getCollection("3 test").find()
db.myCollection.find().pretty()

show tables
show dbs
show collections

quit()
```

```python
# -*- coding: utf-8 -*-
#!/usr/bin/env python

from pymongo import MongoClient
client = MongoClient('mongodb://192.168.0.17:27017')
db = client['epsi_iot']
lum = db.lum
temp = db.temp

post_data = {
    'ds': '02/04/1970 00h00',
    'y': 24
}

result = temp.insert_one(post_data)

post_data = {
    'ds': '02/04/1970 00h00',
    'y': 3
}
result = lum.insert_one(post_data)
#print('One post: {0}'.format(result.inserted_id))
#new_result = posts.insert_many([post_1, post_2, post_3])
"""
bills_post = posts.find_one({'author': 'Scott'})
print(bills_post)

scotts_posts = posts.find({'author': 'Scott'})
print(scotts_posts)
for post in scotts_posts:
    print(post)
"""
```

## Client Python
```bash
pip3 install pika
pip3 install pymongo
pip3 install fbprophet
pip3 install --upgrade plotly
```

## Sensor
```python
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
```




