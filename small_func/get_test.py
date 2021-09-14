# -*- coding: utf-8 -*- 
"""
Created on 2021/7/9 16:03 
@File  : get_test.py
@author: zhoul
@Desc  :
"""

import pandas
from commonfunc.db_client import MysqlClient


class GetTest:

    def get_test(self):
        rdc = MysqlClient()
        oc = MysqlClient()
        test_data = pandas.read_csv("20210706155718_WNS_6368_01.csv")
        tracking_number = test_data["TrackingNumber"]
        serial_number = test_data["SerialNumber"]
        rdc.execute_sql()

    def get_csv(self):
        l1 = ['EE30000090534900001040003C0D', 'EE30000090535040001040003E0D', 'EE30000090535160001040003F0D',
              'EE30000090535290001040003G0D', 'EE30000090535310001040003G0D', 'EE30000090535430001040003F0D',
              'EE30000090535550001040003D0D', 'EE30000090535680001040003G0D', 'EE30000090535700001040003D0D',
              'EE30000090535820001040003F0D']
        l2 = ['CNCPP210812172027176747676', 'CNCPP210812172304176741481', 'CNCPP210812172539176749331',
              'CNCPP210812172813176742991', 'CNCPP210812173048176748368', 'CNCPP210812173322176747146',
              'CNCPP210812173556176741723', 'CNCPP210812173830176751027', 'CNCPP210812174105176742276',
              'CNCPP210812174340176744076']
        l3 = ['A0300098790DHA1080020SHA0', 'A0300098800DHA1080020SHA0', 'A0300098810DHA1080020SHA0',
              'A0300098820DHA1080020SHA0', 'A0300098830DHA1080020SHA0', 'A0300098840DHA1080020SHA0',
              'A0300098850DHA1080020SHA0', 'A0300098860DHA1080020SHA0', 'A0300098870DHA1080020SHA0',
              'A0300098880DHA1080020SHA0']

        result = pandas.DataFrame({"tracking_number": l1, "last_mile_tracking_number": l2, "bag_id": l3})
        result.to_csv("num.csv")

    def str_1(self):
        test_data, test_result = [], []
        f = open("tracking_number.txt", "r", encoding="UTF-8")
        for line in f.readlines():
            test_data.append(line.strip("\n"))
        for i in test_data:
            test_result.append(i[:15])
        csv_result = pandas.DataFrame({"reference_number": test_result})
        csv_result.to_csv("reference_number.csv")

    def compare_zipcode(self):
        test_data1, test_data2, test_data3, result = [], [], [], []
        f = open("法国邮编.txt ", "r", encoding="UTF-8")
        for line in f.readlines():
            test_data1 = line.split("$|^")
        ex_data = pandas.read_csv("邮编白名单去重.csv")
        test_data1 = list(map(int, test_data1))
        test_data2 = ex_data["zipcode"].tolist()
        union_data = set(test_data1) & set(test_data2)


if __name__ == '__main__':
    GetTest().compare_zipcode()
