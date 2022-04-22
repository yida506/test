# -*- coding: utf-8 -*-

"""
@author: lan

@contact: 将代理ip存入redis,采取集合的方式对proxy进行存储
实现内容:
1.代理删除,根据指定value删除redis中的代理
2.代理获取,根据时间刷新代理池
3.
@Created on: 2022/4/18
"""

import math
import time
from feapder.utils.log import log
import requests
from feapder.db.redisdb import RedisDB




class ProxyPool:

    def __init__(self,
                 rediskey='proxytest',
                 restart_time = 5
                 ):
        self._redis = RedisDB()
        self.rediskey = rediskey
        self.restart_time = restart_time
        self.clear(self.rediskey)
        self.proxy_to_redis(self.rediskey)
        log.debug(f'代理池构建成功目前有{self.proxy_count}条代理')

    def run(self):
        """
        将ip存入redis
        :return:
        """
        self.start_time = time.time()
        while True:
            if time.time() - self.start_time > self.restart_time:
                log.info('开始重置代理池')
                self.clear(self.rediskey)
                self.proxy_to_redis(self.rediskey)
                log.info(f'重置代理结束目前有{self.proxy_count}条代理')
                return


    def proxy_to_redis(self, rediskey):

        url = 'http://120.25.205.123:8888/user/apeproxy2?'
        res = requests.get(url)
        proxy_list = res.json()['data'][1]['proxy']
        self._redis.sadd(rediskey, proxy_list)


    def proxy_get(self):
        '''
        这里继承后要重写
        :return:
        '''
        log.debug(self.proxy_count)
        get_proxy = self._redis.sget(self.rediskey, is_pop=False)[0]
        self._redis.srem(self.rediskey, get_proxy)
        log.debug(self.proxy_count)



    @property
    def proxy_count(self):
        return self._redis.sget_count(self.rediskey)


    def remove_proxy(self, proxy):
        '''
        用于删除已失效的代理
        :param proxy:
        :return:
        '''
        log.debug(f'当前代理{proxy}不可用')
        self._redis.srem(self.rediskey, proxy)
        log.debug(f'代理已移除,'
                  f'redis中还余{self.proxy_count}条代理')

    def clear(self, rediskey):
        '''
        清空代理池
        :param rediskey:
        :return:
        '''
        log.info('正在清空代理池')
        try:
            self._redis.delete(rediskey)
        except Exception as e:
            log.error(e)



# proxies = {
#     "http": "http://proxy:12qwaszx@{}".format(proxy),
#     "https": "http://proxy:12qwaszx@{}".format(proxy)
# }


class ProxyPoolChild(ProxyPool):
    pass
    # def __init__(self
    #              ):
    #     super(ProxyPoolChild, self).__init__()




if __name__ == '__main__':
    a = ProxyPool()
    a.run()
    # b = ProxyPoolChild(restart_time=10)
    # b.run()




    # def a_new_decorator(a_func):
    #     def a():
    #         start_time = time.time()
    #         a_func()
    #         time.sleep(1)
    #         print(time.time()-start_time)
    #     return a
    #
    # @a_new_decorator
    # def a_function_requiring_decoration():
    #     print("I am the function which needs some decoration to remove my foul smell")
    #
    # a_function_requiring_decoration()






