import os, sys
import time
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import zillow_web_scraper_client

from cloudAMQP_client import CloudAMQPClient

# RabbitMQ config
CLOUD_AMQP_URL = '''amqp://kdflangt:w3wO5ExwRgGqixP6q-4Y9HDy2aGXETCG@hyena.rmq.cloudamqp.com/kdflangt'''
DATA_FETCHER_QUEUE_NAME = 'dataFetcherTaskQueue'

# mongodb config
PROPERTY_TABLE_NAME = 'property'

# fetcher config
FETCH_SIMILAR_PROPERTIES = True

SECONDS_IN_ONE_DAY = 3600 * 24
SECONDS_IN_ONE_WEEK = SECONDS_IN_ONE_DAY * 24

WAITING_TIME = 3

cloudAMQP_client = CloudAMQPClient(CLOUD_AMQP_URL, DATA_FETCHER_QUEUE_NAME)

def handle_message(msg):
    task = json.loads(msg)

    if (not isinstance(task, dict) or
        not 'zpid' in task or
        task['zpid'] is None):
        return

    zpid = task['zpid']

    # scrape the zillow for details
    property_detail = zillow_web_scraper_client.get_property_by_zpid(zpid)
    property_detail['last_update'] = time.time()
    print property_detail

    # update db
    db = mongodb_client.getDB()
    db[PROPERTY_TABLE_NAME].replace_one({'zpid': zpid}, property_detail, upsert=True) # use replace_one

    if FETCH_SIMILAR_PROPERTIES:
        # get its similar properties' zpid
        similar_zpids = zillow_web_scraper_client.get_similar_homes_for_sale_by_id(zpid)

        # generate tasks for similar
        for zpid in similar_zpids:
            old = db[PROPERTY_TABLE_NAME].find_one({'zpid': zpid})
            # don't send task if the record is recent
            if (old is not None and
                time.time() - old['last_update'] < SECONDS_IN_ONE_WEEK):
                continue
            cloudAMQP_client.sendDataFetcherTask({'zpid': zpid})

# main thread
while True:
    # fetch a message
    if cloudAMQP_client is not None:
        msg = cloudAMQP_client.getDataFetcherTask()
        if msg is not None:
            handle_message(msg)
        time.sleep(WAITING_TIME)
