#! usr/bin/python
# _*_ coding=utf-8 _*_
'''
@time: 2018/2/26 14:39
@author: jiangzeyu5
'''


class person():
    def __init__(self, name, gender, birth, **kw):
        self.name = name
        self.gender = gender
        self.birth = birth
        for k, w in kw.items():
            setattr(self, k, w)

    def sayhi(self):
        print('my name is', self.name)

xiaoming = person('Xiao Ming', 'Male', '1991-1-1',job='student',tel='18089355',stdid='15010')

xiaohong = person('Xiao Hong', 'Female', '1992-2-2')
print(xiaoming.name)
print(xiaohong.birth)
print(xiaoming.job)
print(xiaoming.tel)
print(xiaoming.stdid)
print(xiaoming.sayhi())