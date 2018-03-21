#! usr/bin/python
# _*_ coding=utf-8 _*_
'''
@time: 2018/3/21 14:04
@author: jiangzeyu5
'''

import requests
from lxml import etree
from time import time
from concurrent.futures import ProcessPoolExecutor     #多进程

url = 'https://movie.douban.com/top250'

def fetch_content(url):
    page = requests.get(url).content
    return page

def parse(url):
    page = fetch_content(url)
    html = etree.HTML(page)

    fetch_list = []
    result = []
    xpath_movie = '//*[@id="content"]/div/div[1]/ol/li'
    xpath_title = './/span[@class="title"]'
    xpath_pages = '//*[@id="content"]/div/div[1]/div[2]/a'

    pages = html.xpath(xpath_pages)

    for p in pages:
        fetch_list.append(url+p.get('href'))  #得到href里面的链接参数

    for element_movie in html.xpath(xpath_movie):
        result.append(element_movie)

    with ProcessPoolExecutor(max_workers=4) as executor:
        for page in executor.map(fetch_content,fetch_list):
            html = etree.HTML(page)
            for element_movie in html.xpath(xpath_movie):
                result.append(element_movie)

    for i, movie in enumerate(result, 0):
        title = movie.find(xpath_title).text
        print(i, title)

def main():
    start = time()
    parse(url)
    end = time()
    print ('Cost {} seconds'.format(end - start))

if __name__ == '__main__':
    main()