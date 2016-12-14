"""
changes
    * rename "searchAreaByZip" -> "getZpidByZip"
    * rename "searchAreaByCityState" -> "getZpidByCityState"
    * TODO: use multithreading to add searched properties to the queue
"""

import os, sys
import pyjsonrpc
import json
import re
import time

from bson.json_util import dumps

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import zillow_web_scraper_client

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

PROPERTY_TABLE_NAME = 'property'

# TODO: search by detailed address

"""Search properties in an area"""
def searchArea(text):
    properties = []
    if text.isdigit():
        properties = searchAreaByZip(text)
    else:
        city = text.split(',')[0].strip()
        state = text.split(', ')[1].strip()
        properties = searchAreaByCityState(city, state)
    return properties

"""Search properties by zip code"""
def searchAreaByZipcode(zipcode):
    print "searchAreaByZip() gets called with zipcode=[%s]" % str(zipcode)
    properties = findProperyByZipcode(zipcode) #rename
    if len(properties) == 0:
        # cannot find in db, use scraper to fetch
        zpids = zillow_web_scraper_client.get_zpid_by_zipcode() # rename
        for zpid in zpids:
            property_detail = zillow_web_scraper_client.get_property_by_zpid(zpid)
            properties.append(property_detail)
        # update db
        storeUpdates(properties)
    return properties

"""Search properties by city state"""
def searchAreaByCityState(city, state):
    print "searchAreaByCityState() gets called with city=[%s] abd state=[%s]" % (city, state)
    properties = findProperyByCityState(city, state)
    if len(properties) == 0:
        # cannot find in db, use scraper to fetch
        zpids = zillow_web_scraper_client.get_zpid_by_city_state() # rename
        for zpid in zpids:
            property_detail = zillow_web_scraper_client.get_property_by_zpid(zpid)
            properties.append(property_detail)
        # update db
        storeUpdates(properties)
    return properties

"""Find property by zipcode"""
def findProperyByZipcode(zipcode):
    db = mongodb_client.getDB()
    properties = list(db[PROPERTY_TABLE_NAME].find({'zipcode': zipcode, 'is_for_sale': True}))
    return properties

"""Find property by city state"""
def findProperyByCityState(city, state):
    db = mongodb_client.getDB()
    # use regexp to do case-insensitive search
    properties = list(db[PROPERTY_TABLE_NAME]\
                    .find({ 'city': re.compile(city, re.IGNORECASE),\
                            'state': re.compile(state, re.IGNORECASE),\
                            'is_for_sale': True}))
    return properties

"""Update doc in db"""
def storeUpdates(properties):
    print "updating properties in db after searching..."
    db = mongodb_client.getDB()
    for perperty_detail in properties:
        zpid = property_detail['zpid']
        property_detail['last_update'] = time.time()
        db[PROPERTY_TABLE_NAME].replace_one({'zpid': zpid}, property_detail, upsert=True)
