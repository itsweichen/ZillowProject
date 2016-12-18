import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import redis_client

AUTOCOMPLETE_KEY = "autocomplete"
PROPERTY_TABLE_NAME = "property"

db = mongodb_client.getDB()
redis = redis_client.getRedis()

# Read all City and States into Redis
properties = db[PROPERTY_TABLE_NAME].find()

print "Writing autocomplete to Redis..."

for property in properties:
    city = property['city']
    state = property['state']
    redis.zadd(AUTOCOMPLETE_KEY, "%s, %s" % (city, state), 0)

print "Autocomplete done!"
