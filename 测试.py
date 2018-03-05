#!/user/bin/env python
# _*_ coding:utf-8 _*_
"""
@Created Time: 2018/1/22 17:12:14
@author: jiangzeyu5
"""

#  a = 1
# def fun(a):
#     a = 2
# fun(a)     #所有的变量都可以理解是内存中一个对象的“引用”
# print(a)   #类型是属于对象的，而不是变量。
#            #而对象有两种,“可更改”（list,dict）与“不可更改”（strings, tuples, 和numbers）对象。

# Python中单下划线和双下划线：
# __foo__:一种约定,Python内部的名字,用来区别其他用户自定义的命名,以防冲突.
# _foo:一种约定,用来指定变量私有.程序员用来指定私有变量的一种方式.
# __foo:这个有真正的意义:解析器用_classname__foo来代替这个名字,以区别和其他类相同的命名.

# def print_ever(*args):
#     for count, thing in enumerate(args,0):
#         #enumerate将其组成一个索引序列，利用它可以同时获得索引和值,可以设置从1计数
#         print('{0}{0},{1}'.format(count, thing))
#
# print_ever('apple','banana','orange')