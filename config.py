# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 16:58:59 2017

@author: jiangzeyu5
"""
# "DispositionID":500107000003012017122509433615884
import json
import runmethod

t = runmethod.RunMethod()
def literature():
    for NotificationID in range(500000022016120217485613001,500000022016120217485613010):
        NotificationID = str(NotificationID)
        data={"DispositionNotificationObject":[{"NotificationID":NotificationID,"DispositionID":"500107000003012017122509433615884","Title":"告警测试","TriggerTime":"20171228185501","CntObjectID":"","MotorVehicleObject":{"MotorVehicleID":"6000000001","PlateNo":"渝A12345","StorageUrl1":"http://10.196.134.157:8088/image/vrb2/i2/ab32993885354fa98467203641dd6e5c/00022?key=38af&offset=1230167852&high=372348","TollgateID":"00005001051210000001","StorageUrl2":"http://10.196.134.157:8088/image/vrb2/i2/ab32993885354fa98467203641dd6e5c/00022?key=38b0&offset=1230540280&high=3264","PlateClass":"1","PlateColor":"1","PassTime":"20170109115500","LaneNo":"1","VehicleClass":"1","VehicleBrand":"1","Speed":"99","Direction":"1","VehicleBrand":"3","VehicleStyles":"2016"}}]}
        json_data = json.dumps(data)
        return json_data
    print(type(data),type(json_data))



if __name__ == '__main__':
    literature()
    print(t.run_main('Post', 'http://10.100.60.114:8023/VIID/DispositionNotifications',literature()))
    # print(t.run_main('Post', 'http://10.100.60.114:8023/VIID/Dispositions', json_data))
