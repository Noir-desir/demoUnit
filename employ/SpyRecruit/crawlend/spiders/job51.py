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
    name = 'job51'
    allowed_urls = []
    start_urls = []
    if IS_ONLY_TODAY:
        urls = ['http://search.51job.com/list/020000%252C010000%252C030200%252C040000%252C080200,000000,0000,00,0,99,{},2,1.html'.format(
                KEYWORD),
            'http://search.51job.com/list/070200%252C090200%252C180200%252C200200%252C070300,000000,0000,00,0,99,{},2,1.html'.format(
                KEYWORD)

        ]


