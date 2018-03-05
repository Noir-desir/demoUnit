# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 16:58:59 2017

@author: jiangzeyu5
"""


#{"DispositionNotificationObject":[{"NotificationID": "500000022016120217485614999","DispositionID":"500107000003012017122114351111735","Title":"告警测试","TriggerTime":"20171221150001","CntObjectID":"","MotorVehicleObject":{"MotorVehicleID":"6000000001","PlateNo":"渝A12345","StorageUrl1":"http://10.196.134.157:8088/image/vrb2/i2/ab32993885354fa98467203641dd6e5c/00022?key=38af&offset=1230167852&high=372348","TollgateID":"00005001051210000001","StorageUrl2":"http://10.196.134.157:8088/image/vrb2/i2/ab32993885354fa98467203641dd6e5c/00022?key=38b0&offset=1230540280&high=3264","PlateClass":"1","PlateColor":"1","PassTime":"20170109115500","LaneNo":"1","VehicleClass":"1","VehicleBrand":"1","Speed":"99","Direction":"1","VehicleBrand":"3","VehicleStyles":"2016"}}]}

import requests
import json
from requests.auth import HTTPBasicAuth

class RunMethod:
    # 参数必须按照url、data、header顺序传入
#post 接口主入口
    def post_main(self,url,data):
        res = None
        res = requests.post(url=url,data=data).json()
        return res
#get 接口主入口
    def get_main(self,url,data):
        res = None
        res = requests.get(url=url,data=data).json()
        return res
#调用postman
    def run_main(self, method, url= None, data = None):
        res = None
        if method == 'Post':
            res = self.post_main(url,data)
        else:
            res = self.get_main(url,data)
        return res

if __name__ == '__main__':
    t = RunMethod()
    data = {'type':'zhongtong',
            'postid':'473082149226',
            'temp':0.3346865154574279
            }
    print(type(data))
    print(t.run_main('Post','http://www.kuaidi100.com/query',data))




    #带headers 的请求
    # header={'user-identify':'50010012345031234567'}
    # data = {"DispositionObject":[{"Title":"车辆布控下级接口测试1","DispositionCategory":"3","TargetFeature":"(3=渝D2S035)","PriorityLevel":"1","BeginTime":"20171216000000","EndTime":"20171230 000000","OperateType":"0","DispositionRange":"2","Reason":"被盗车","ApplicantName":"admin","ApplicantOrg":"市局","ReceiveMobile":"18969196808","DispositionArea":"50010712345030000003"}]}
    # json_data = json.dumps(data)
    # res = requests.post(url='http://10.100.60.133:8023/VIID/Dispositions',data=json_data,headers=header).json()
    # print(res)

    #带密码的请求
    # res = requests.get(url='https://httpbin.org/basic-auth/user/passwd',auth=('user','passwd'))
    # print(res.text)

    #JSON To PYTHON
    # #data = {"DispositionObject": [
    #     {"DispositionID": "500000000000012017121909150119299", "Title": "车辆布控修改欧1", "DispositionCategory": "2",
    #      "TargetFeature": "(3=渝D2S031)", "PriorityLevel": "3", "BeginTime": "20171211000000",
    #      "EndTime": "20181230 000000", "OperateType": "0", "DispositionRange": "2", "Reason": "被盗车",
    #      "ApplicantName": "测试修改", "ApplicantOrg": "市局1", "ReceiveMobile": "18969196808",
    #      "DispositionArea": "50010712345030000003"}]}
    # data={'hello':'world'}
    # data = json.dumps(data)
    # res1 = requests.put(url='https://httpbin.org/put',data=data)
    # print(res1.text)

