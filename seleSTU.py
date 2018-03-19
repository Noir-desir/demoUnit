#!/user/bin/env python
# _*_ coding:utf-8 _*_
"""
@Created Time: 2018/1/19 15:12:01
@author: jiangzeyu5
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import *
import time

browser = webdriver.Chrome()
browser.get('http://www.runoob.com/') #c菜鸟教程
browser.maximize_window()
'''输入内容'''
input = browser.find_element_by_id('s')
input.send_keys('python')
input.send_keys(Keys.ENTER)               #输入enter
time.sleep(5)
'''标签页窗口切换'''
handles = browser.window_handles
browser.switch_to_window(handles[1])   #1为最新窗口，2为次新窗口，0为最初的窗口：0、3、2、1
'''点击更多'''
more = browser.find_element(By.XPATH, '//a[contains(text(),"更多……")]')
more.click()
time.sleep(5)
'''鼠标悬停'''

browser.close()
