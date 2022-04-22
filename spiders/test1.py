# -*- coding: utf-8 -*-
"""
Created on 2022-04-21 09:22:24
---------
@summary:
---------
@author: 20040854
"""

import feapder


class Test1(feapder.AirSpider):
    def start_requests(self):
        yield feapder.Request("https://www.baidu.com")

    def parse(self, request, response):
        print(response)


if __name__ == "__main__":
    Test1().start()