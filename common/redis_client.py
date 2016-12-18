import redis

HOST_NAME = "localhost"
PORT_NAME = "6379"

r = redis.Redis(
    host=HOST_NAME,
    port=PORT_NAME)

def getRedis():
    return r
