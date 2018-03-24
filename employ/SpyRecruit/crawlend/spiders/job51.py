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

from employ.SpyRecruit.crawlend.items import CrawlendItem, FirmItem
from employ.SpyRecruit.crawlend.settings import IS_ONLY_TODAY, KEYWORD
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
        # 寻找 内容为‘下一页’的a标签
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
            # 寻找 存在XX属性 的a标签 这里爬去的是职位链接
            soup_a = soup.find_all('a',
                                   attrs={'target': True, 'title': True,
                                          'href': True, 'onmousedown': True, 'adid': False})
            for item in soup_a:
                href = item.get('href')
                if check_href(href) and href.startswith('http'):
                    yield Request(href, callback=self.parse_detail,
                                  dont_filter=True, headers={'Referer': 'http://search.51job.com/'})

    def parse_detail(self, response):

        item = {}
        offer = CrawlendItem()
        firm = FirmItem()
        soup = bs4.BeautifulSoup(response.body, 'lxml')
        offer['url'] = response.url
        offer['resource'] = '前程无忧'

        # 职位名称，公司信息
        # ‘class’是python关键字所以用‘class_’
        # strip=True 过滤字符后面的空格
        soup_cn = soup.find('div', class_='cn')
        offer['name'] = soup_cn.find('h1').get_text(strip=True)
        offer['work_place'] = soup_cn.find('span', class_='lname').get_text(strip=True)
        firm['work_place'] = offer['work_place']

        # 薪水
        # 正则式：[万千]匹配'万'或者'千';(\d+\.?\d*)匹配小数格式
        p_salary_1 = re._compile(r'(\d+\.?\d*)-(\d+\.?\d*)[万千]')
        str_salary = soup_cn.find('strong').get_text(strip=True)
        r = re.match(p_salary_1, str_salary)
        # 数据单位统一处理
        if r:
            if '万' in str_salary:
                lst_r = [float(i) * 10000 for i in r.groups()]
            else:
                lst_r = [float(i) * 1000 for i in r.groups()]
            offer['salary_from'], offer['salary_to'] = lst_r
        else:
            offer['is_negotiable'] = True

        # 公司名
        firm['firm_name'] = soup_cn.find('p', class_='cname').get_text(strip=True)
        # 行业规模
        soup_firm_msg = soup_cn.find('p', class_='msg ltype').
