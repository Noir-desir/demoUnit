#!/user/bin/env python
# _*_ coding:utf-8 _*_
"""
@Created Time: 2018/1/19 15:12:01
@author: jiangzeyu5
"""

from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://www.runoob.com/') #c菜鸟教程

input = browser.find_element_by_id('s')
input.send_keys('python')
browser.close()





