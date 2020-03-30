# -*- coding: utf-8 -*-
#!/usr/bin/env python

import pandas as pd
from fbprophet import Prophet
from pymongo import MongoClient
import matplotlib.pyplot as plt # first line

def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    return conn[db]

def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find()

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df

#df = pd.read_csv('../examples/example_wp_log_peyton_manning.csv')
#df.head()

df = read_mongo(db='epsi_iot',collection='lum',query='',host='192.168.0.17')
df.head()
m = Prophet()
m.fit(df)
future = m.make_future_dataframe(periods=30)
future.tail()
forecast = m.predict(future)
m.plot_components(forecast).savefig('/var/www/html/lum.png')


df = read_mongo(db='epsi_iot',collection='temp',query='',host='192.168.0.17')
df.head()
m = Prophet()
m.fit(df)
future = m.make_future_dataframe(periods=30)
future.tail()
forecast = m.predict(future)
m.plot_components(forecast).savefig('/var/www/html/temp.png')

