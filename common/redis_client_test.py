import redis_client

redis = redis_client.getRedis()

redis.set('foo', 'bar')

print redis.get('foo')
