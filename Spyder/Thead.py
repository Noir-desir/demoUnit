#! usr/bin/python
# _*_ coding=utf-8 _*_
'''
@time: 2018/3/20 17:46
@author: jiangzeyu5
'''

import requests
from lxml import etree
from time import time
from threading import Thread                                 #多线程

url = 'https://movie.douban.com/top250'


def parse(url):
    '''多线程案例'''
    response = requests.get(url)
    page = response.content
    html = etree.HTML(page)

    xpath_movie = '//*[@id="content"]/div/div[1]/ol/li'
    xpath_title = './/span[@class="title"]'
    xpath_pages = '//*[@id="content"]/div/div[1]/div[2]/a'

    pages = html.xpath(xpath_pages)
    fetch_list = []
    result = []
    '''解析首页，将内容返回result'''
    for element_movie in html.xpath(xpath_movie):
        result.append(element_movie)
    '''解析页码，拼接url'''
    for p in pages:
        fetch_list.append(url + p.get('href'))

    def fetch_content(url):
        response = requests.get(url)
        page = response.content
        html = etree.HTML(page)

        for element_movie in html.xpath(xpath_movie):
            result.append(element_movie)
    '''线程设置启动'''
    threads = []
    for url in fetch_list:
        t = Thread(target=fetch_content, args=[url])
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    for i, movie in enumerate(result,1):
        title = movie.find(xpath_title).text
        print(i,title)


def main():
    start = time()
    parse(url)
    end = time()
    print ('Cost {} seconds'.format(end - start))

if __name__ == '__main__':
    main()