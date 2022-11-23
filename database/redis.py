import redis

def redisConnection():
    POOL = redis.ConnectionPool(host='redisengineering.redis.cache.windows.net', port=6379,password='QrtfUtgtqvZ5JmQlySiqJc3PkyHttrufqAzCaMMPbNg=')
    r = redis.StrictRedis(connection_pool=POOL, charset="utf-8", decode_responses=True)
    return r