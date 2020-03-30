# -*- coding: utf-8 -*-
#!/usr/bin/env python

from pymongo import MongoClient
client = MongoClient('mongodb://192.168.0.17:27017')
db = client['epsi_iot']
lum = db.lum
temp = db.temp

post_data = {
    'ds': '02/04/2000 00h00',
    'y': 5200
}

result = temp.insert_one(post_data)

post_data = {
    'ds': '02/04/2000 00h00',
    'y': 1200
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