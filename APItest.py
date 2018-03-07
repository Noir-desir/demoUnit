# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 16:58:59 2017

@author: jiangzeyu5
"""
import requests

class APIbox():
    def __init__(self, method=None, url=None):
        self._method = method
        self._url = url
        self.reqMethod()

    def reqMethod(self, **kwargs):
        res = requests.get(url=self._url, params=kwargs).json()
        return res




if __name__ == '__main__':
    mtime = APIbox(method='GET', url='https://api-m.mtime.cn/PageSubArea/HotPlayMovies.api/')
    data = {'locationId':'280'}
    print(mtime.reqMethod(params=data))




