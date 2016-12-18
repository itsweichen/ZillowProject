"""
Add tasks (zpid) to MQ from zipcode list file
"""

import os, sys
import time
import random

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import zillow_web_scraper_client

from cloudAMQP_client import CloudAMQPClient

# RabbitMQ config
CLOUD_AMQP_URL = '''amqp://kdflangt:w3wO5ExwRgGqixP6q-4Y9HDy2aGXETCG@hyena.rmq.cloudamqp.com/kdflangt'''
DATA_FETCHER_QUEUE_NAME = 'dataFetcherTaskQueue'
ZIPCODE_FILE = 'san_diego_zipcode_list.txt'
SHUFFLE_ZIPCODES = True

WAITING_TIME = 3

cloudAMQP_client = CloudAMQPClient(CLOUD_AMQP_URL, DATA_FETCHER_QUEUE_NAME)

zipcode_list = []

with open(ZIPCODE_FILE, 'r') as zipcode_file:
    for zipcode in zipcode_file:
        zipcode_list.append(str(zipcode))

if SHUFFLE_ZIPCODES:
    print "shuffle zipcodes!"
    random.shuffle(zipcode_list)

for zipcode in zipcode_list:
    zpids = zillow_web_scraper_client.get_zpid_by_zipcode(zipcode)
    time.sleep(WAITING_TIME)

    for zpid in zpids:
        cloudAMQP_client.sendDataFetcherTask({"zpid": zpid})
