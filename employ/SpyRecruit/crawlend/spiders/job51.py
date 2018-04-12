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
        soup_firm_msg = soup_cn.find('p', class_='msg ltype')
        str_msg = soup_firm_msg.string.replace('&nbsp;', '')
        nature, scale, indus = [i.strip() for i in str_msg.split('|')]

        # 企业性质
        # 编码规范化入库
        if '外企' in nature:
            firm['firm_nature'] = '2'
        elif '合资' in nature:
            firm['firm_nature'] = '3'
        elif '国企' in nature:
            firm['firm_nature'] = '1'
        elif '民营' in nature:
            firm['firm_nature'] = '4'
        elif '上市' in nature:
            firm['firm_nature'] = '7'
        else:
            firm['firm_nature'] = '5'

        # 企业规模
        p_scale = re.compile(r'\d+')
        lst_scale = re.findall(p_scale, scale)
        lst_scale = [int(i) for i in lst_scale]
        lst_scale.sort()
        if len(lst_scale) == 2:
            firm['firm_scale_from'], firm['firm_scale_to'] = lst_scale
        elif len(lst_scale) == 1:
            firm['firm_scale_from'] = lst_scale[0]

        # 行业
        firm['firm_industry'] = indus

        # 职位要求
        soup_job_qua = soup.find('div', class_= 'jtag inbox')
        soup_qua_div = soup_job_qua.find('div', class_='t1')
        soup_qua_span = soup_qua_div.find_all('span')
        # 正则式匹配经验年限
        p_exp = re.compile(r'\d+')
        # 正则式匹配发布时间
        p_date = re.compile(r'\d+-\d+')
        today = datetime.date.today()
        year_ = today.year
        for span in soup_qua_span:
            text = span.get_text(strip=True)
            # 处理经验
            if '经验' in text:
                r_exp = re.findall(p_exp, text)
                r_exp.sort()  # 排序
                if len(r_exp) == 2:
                    offer['years_of_work_from'], offer['years_of_work_to'] = r_exp
                elif len(r_exp) == 1:
                    offer['years_of_work_from'] = r_exp[0]
            # 学历
            if '高中' in text:
                offer['degree'] = '1'
            elif '大专' in text:
                offer['degree'] = '2'
            elif '本科' in text:
                offer['degree'] = '3'
            elif '研究生' in text:
                offer['degree'] = '4'
            elif '博士' in text:
                offer['degree'] = '5'
            # 招聘人数
            if '招聘':
                r_mem = re.findall(p_exp, text)
                if len(r_mem) == 1:
                    offer['member'] = r_mem[0]
            # 发布时间
            if '发布':
                r_date = re.findall(p_date, text)
                if r_date:
                    date_ = str(year_) + '-' + r_date[0]
                    offer['release'] = datetime.datetime.strptime(date_, "%Y-%m-%d").date()

        offer.setdefault('degree', '6')
        offer.setdefault('release', today)
        # 职位诱惑
        soup_r = soup_job_qua.find('p', class_='t2')
        if soup_r:
            offer['temptation'] = soup_r.get_text(';', strip=True)
        soup_qua = soup.find('div', class_='bmsg job_msg inbox')
        # 职位描述
        offer['description'] = soup_qua.get_text(strip=True).replace('举报', '').replace('分享', '')

        # 公司地址
        soup_loc_div = soup.find('div', class_='bmsg inbox')
        soup_loc_p = soup_loc_div.find('p', class_='fp')
        firm['firm_location'] = [i for i in soup_loc_p.stripped_strings][-1]

        # 公司简介
        soup_intro = soup.find('div', class_='tmsg inbox')
        firm['firm_introduction'] = soup_intro.get_text(strip=True)

        item['offer'] = offer
        item['firm'] = firm
        yield item

