# -*- coding: utf-8 -*-
"""
Created on 2022-04-06 11:46:37
---------
@summary:
---------
@author: 20040854
"""

import feapder
from feapder.utils.log import log
import time
import feapder.setting as setting


class TestSpider(feapder.AirSpider):
    def start_requests(self):
        page = 1
        yield feapder.Request("post",
                              page=page,
                              Count=0)

    def download_midware(self, request):
        # orderno = "DT20220405153754GXHfsDSg"
        # secret = "18f6894490d1958f6914b69004140fa1"
        # ip = "dynamic.xiongmaodaili.com"
        # port = "8088"
        # ip_port = ip + ":" + port

        # timestamp = str(int(time.time()))  # 计算时间戳
        # txt = ''
        # txt = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp
        # md5_string = hashlib.md5(txt.encode()).hexdigest()  # 计算sign
        # sign = md5_string.upper()  # 转换成大写
        # auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp + "&change=true"
        # request.proxies = {"https": "http://" + ip_port}
        # request.headers = {
        #     "Xiongmao-Proxy-Authorization": auth
        # }
        request.cookies = {
            "sessionid": "0hxo02udu9kfxwdldrtrxj5c55rei7qi"
        }
        request.url = "https://www.python-spider.com/api/challenge4"
        request.data = {
            "page": request.page
        }
        return request


    def parse(self, request, response):
        data = response.json['data']
        for i in data:
            request.Count += int(i.get('value'))
        # log.info(request.Count)
        if request.page == 1:
            for now_page in range(2, 101):
                yield feapder.Request("post",
                                    page=now_page,
                                    Count=request.Count,
                                    request_sync=True
                                      )
            log.error(request.Count)



if __name__ == "__main__":
    TestSpider().start()
