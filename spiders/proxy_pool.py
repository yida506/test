# -*- coding: utf-8 -*-

"""
@author: lan

@contact:
将代理ip存入redis,采取集合的方式对proxy进行存储
实现内容:
1.代理池创建,每次运行代理池,重新去拉去所需代理
2.代理删除,根据指定value删除redis中的代理
3.代理获取,根据时间刷新代理池
4.自动刷新,根据一定的时间间隔,批量更新代理池


@Created on: 2022/4/18
"""




import time
from feapder.utils.log import log
import requests
from feapder.db.redisdb import RedisDB








class ProxyPool:

    def __init__(self,
                 rediskey='proxytest',
                 restart_time=120,
                 restart_interval=20,
                 max_proxy_size=100
                 ):
        '''

        :param rediskey: redis中的键值
        :param restart_time: 代理池刷新最大间隔
        :param restart_interval: 代理池刷新最小间隔
        :param max_proxy_size: 代理池的最大数量
        '''
        self.start_time = time.time()
        self._redis = RedisDB()  #使用feapder自带的redis封装,连接在setting中配置
        self.rediskey = rediskey
        self.restart_time = restart_time
        self.restart_interval = restart_interval
        self.max_proxy_size = max_proxy_size
        self.proxy_to_redis(self.rediskey)
        log.debug(f'代理池构建成功')


    def run(self):
        """

        :return:
        """
        # 常驻前需要清空代理池
        self.clear()
        while True:
            if self.proxy_count < self.max_proxy_size:
                log.error('代理数量过少,开始添加代理')
                self.proxy_to_redis(self.rediskey)

            if self.proxy_count == 0:
                log.debug('代理池为空,开始重置代理')
                self.proxy_delay()
                self.proxy_to_redis(self.rediskey)
            # 重置
            if time.time() - self.start_time > self.restart_time:
                self.clear(self.rediskey)
                self.proxy_to_redis(self.rediskey)
                log.info(f'重置代理结束目前有{self.proxy_count}条代理')
                return

            time.sleep(1)

    def proxy_delay(self):
        if time.time() - self.start_time < self.restart_interval:
            log.error('加载过快')
            time.sleep(1)


    def proxy_to_redis(self, rediskey):
        if time.time() - self.start_time > self.restart_interval:
            proxy_list = self.get_out_proxy()
            self._redis.sadd(rediskey, proxy_list)
            self.start_time = time.time()
            log.debug(f'目前有{self.proxy_count}条代理')


    def get_out_proxy(self):
        '''
        获取代理的列表
        :return: 返回的代理列表[27.191.64.227:6666,27.191.64.227:8888]这种形式
        '''
        url = 'http://api.xiequ.cn/VAD/GetIp.aspx?act=get&uid=86749&vkey=934BFAEF5BD64E655BF1956A98C60303&num=10&time=30&plat=0&re=0&type=0&so=1&ow=1&spl=1&addr=&db=1'
        res = requests.get(url)
        data = res.json()['data']
        proxy_list = [str(ip['IP']) + ':' + str(ip['Port']) for ip in data]
        return proxy_list


    def proxy_get(self):
        '''
        :return: 返回一个代理ip 124.113.193.27:8000这种形式,实际使用需要拼接,也可以重写
        '''
        # log.debug(self.proxy_count)
        if self.proxy_count > 0:
            proxy = self._redis.sget(self.rediskey, is_pop=False)[0]
            log.debug(self.proxy_count)
            return proxy


    @property
    def proxy_count(self):
        # 代理池中的数量
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

    def clear(self):
        '''
        清空代理池
        :param rediskey:
        :return:
        '''
        log.debug('正在清空代理池')
        try:
            self._redis.delete(self.rediskey)
        except Exception as e:
            log.error(e)






if __name__ == '__main__':
    a = ProxyPool(restart_time=120)
    a.run()
    # a.clear()
    # a.proxy_get()












