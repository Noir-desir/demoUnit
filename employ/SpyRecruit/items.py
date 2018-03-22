#! usr/bin/python
# _*_ coding=utf-8 _*_
'''
@time: 2018/3/22 10:32
@author: jiangzeyu5
'''

import scrapy
from scrapy_djangoitem import DjangoItem
from background.models import Recruit, Firm, Proxy


class CrawlendItem(DjangoItem):
    # 为你的项目定义标准字段
    django_model = Recruit


class FirmItem(DjangoItem):
    django_model = Firm


class ProxyItem(DjangoItem):
    django_model = Proxy

