# proxies = {
#     "http": "http://proxy:12qwaszx@{}".format(proxy),
#
#     "https": "http://proxy:12qwaszx@{}".format(proxy)
# }

import requests
from feapder.utils.log import log
from feapder.db.redisdb import RedisDB
import time



class proxy_pool:

    def __init__(self,
                 redis_key,
                 restart_time = 5):
        self._redis = RedisDB()
        self.redis_key = redis_key
        self.restart_time = restart_time

    def run(self):
        self.start_time = time.time()
        while True:
            log.info(time.time())
            if time.time() - self.start_time > self.restart_time:
                # 这里实现
                return
        # res = requests.get('http://120.25.205.123:8888/user/apeproxy2?')
        # proxy_list = res.json()['data'][1]['proxy']
        # self._redis.sadd(self.redis_key, proxy_list)

    def clear(self, redis_key):
        try:
            self._redis.delete(redis_key)
        except Exception as e:
            log.error(e)


    def proxy_to_redis(self):
        res = requests.get('http://120.25.205.123:8888/user/apeproxy2?')
        proxy_list = res.json()['data'][1]['proxy']
        self._redis.sadd(self.redis_key, proxy_list)

    def get_proxy(self):
        return self._redis.sget(self.redis_key)[0]

    def remove_proxy(self, value):
        log.info(self.proxy_count)
        self._redis.srem(self.redis_key, value)
        log.info(self.proxy_count)



    @property
    def proxy_count(self):
        return self._redis.sget_count(self.redis_key)



a = proxy_pool(redis_key='proxytest')
b = a.get_proxy()
log.info(b)
a.remove_proxy(b)





