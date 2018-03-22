#! usr/bin/python
# _*_ coding=utf-8 _*_
'''
@time: 2018/3/21 16:31
@author: jiangzeyu5
'''

import re
import datetime
import bs4

import scrapy
from scrapy.http import Request

from ..items import CrawlendItem, FirmItem
from ..settings import IS_ONLY_TODAY, KEYWORD
from employ.background.models import Recruit


class Job51Spider(scrapy.Spider):
    # 继承Spider
    name = 'job51'
    allowed_urls = ['jobs.51job.com']
    start_urls = []
    if IS_ONLY_TODAY:
        urls = [
            'http://search.51job.com/list/020000%252C010000%252C030200%252C040000%252C080200,000000,0000,00,0,99,{},2,1.html'.format(
                KEYWORD),
            'http://search.51job.com/list/070200%252C090200%252C180200%252C200200%252C070300,000000,0000,00,0,99,{},2,1.html'.format(
                KEYWORD)
        ]  # 1.北上广深杭；2.南京成都武汉西安苏州
    else:
        urls = [
            'http://search.51job.com/list/020000%252C010000%252C030200%252C040000%252C080200,000000,0000,00,9,99,{},2,1.html'.format(
            KEYWORD),
            'http://search.51job.com/list/070200%252C090200%252C180200%252C200200%252C070300,000000,0000,00,9,99,{},2,1.html'.format(
            KEYWORD)
        ]  # 1.北上广深杭；2.南京成都武汉西安苏州

    start_urls += urls

    def parse(self, response):

        def check_href(url):
            try:
                r = Recruit.objects.get(url=url)
                return False
            except:
                return True
        soup = bs4.BeautifulSoup(response.body, 'lxml')
        # 下一页
        # 寻找内容为‘下一页’的a标签
        soup_next = soup.find('a', text='下一页')
        if not soup_next:
            yield Request(response.url, callback=self.parse, dont_filter=True,
                          headers={'Referer': 'http://search.51job.com/'})
        else:
            if soup_next:

                url = soup_next.get('href')
                yield Request(url, callback=self.parse, dont_filter=True,
                              headers={'Referer': 'http://search.51job.com/'})
            # 职位列表
            # 寻找 存在XX属性 的a标签
            soup_a = soup.find_all('a',
                                   attrs={'target': True, 'title': True,
                                          'href': True, 'onmousedown': True, 'adid': False})
            for item in soup_a:
                href = item.get('href')
                if check_href(href) and href.startswith('http'):
                    yield Request(href, callback=self.parse_detail,
                                  dont_filter=True, headers={'Referer': 'http://search.51job.com/'})