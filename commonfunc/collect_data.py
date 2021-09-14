# -*- coding: utf-8 -*- 
"""
Created on 2021/9/3 17:19 
@File  : collect_data.py
@author: zhoul
@Desc  : 收集/读取数据
"""
from jsonpath import jsonpath


class CollectData:

    def __init__(self):
        pass

    def get_json_data(self):
        test_json = {
            "sysErro": False,
            "validationResults": [
                {
                    "freightDTO": {
                        "currency": "CNY",
                        "freight": 2.2100
                    },
                    "result": True,
                    "serviceId": "EE",
                    "sysErro": False
                },
                {
                    "freightDTO": {
                        "currency": "CNY",
                        "freight": 3.4400
                    },
                    "result": True,
                    "serviceId": "ES",
                    "sysErro": False
                },
                {
                    "erroMessageCn": "超出物流服务范围 – 请核查订单信息匹配以下受限范围：尺寸限制/重量限制/申报金额限制/派送区域",
                    "erroMessageEn": "Out of logistic service scope, please double check your order if comply with the service standards: Dimension Limit, Weight Limit, Cargo Value Limit, and Delivery Area coverage.",
                    "result": False,
                    "serviceId": "EX",
                    "sysErro": False
                },
                {
                    "erroMessageCn": "超出物流服务范围 – 请核查订单信息匹配以下受限范围：尺寸限制/重量限制/申报金额限制/派送区域",
                    "erroMessageEn": "Out of logistic service scope, please double check your order if comply with the service standards: Dimension Limit, Weight Limit, Cargo Value Limit, and Delivery Area coverage.",
                    "result": False,
                    "serviceId": "EM",
                    "sysErro": False
                }
            ]
        }
        collect  = ["$.validationResults[0:2:1].result","$.validationResults[0].serviceId","$.validationResults[1].serviceId"]
        for i in collect:
            print(jsonpath(test_json, i))


if __name__ == '__main__':
    CollectData().get_json_data()
