#! usr/bin/python
# _*_ coding=utf-8 _*_
'''
@time: 2018/4/26 9:37
@author: jiangzeyu5
'''

import re
import bs4
import datetime
import json

import scrapy
# from employ.SpyRecruit.crawlend.settings import IS_ONLY_TODAY, KEYWORD
from scrapy.http import Request

class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawlend.middlewares.UAMiddleWare': 546
        },
        'DOWNLOAD_DELAY': 3
    }
    init_url = 'https://m.lagou.com/search.json?city=%E5%85%A8%E5%9B%BD&positionName={0}&pageNo={1}&pageSize=15'
    pagecount = 0

# 网页URL拼接
    def start_requests(self):
        self.pagecount += 1
        url = self.init_url.format(KEYWORD, self.pagecount)
        yield Request(url, callback=self.parse, dont_filter=True)


    def parse(self, response):
        json_data = json.loads(response.body_as_unicode())
        items = json_data['content']['data']['page']['result']
        if not items:
            return
        else:
            self.pagecount += 1
            url = self.init_url.format(KEYWORD, self.pagecount)
            yield Request(url, callback=self.parse, dont_filter=True)
        for item in items:
            print(item)

            # if IS_ONLY_TODAY and '今天' not in item['createTime']:
            #     continue

        url = 'https://www.lagou.com/jobs/{}.html'.format(item['positionId'])
        yield Request(url, callback=self.parse_lagou, headers={'Referer': 'https://www.lagou.com/'})


if __name__ == '__main__':
    lagou = LagouSpider()
    a = lagou.start_requests()
    print(lagou.parse(a))