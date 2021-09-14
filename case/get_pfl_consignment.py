# -*- coding: utf-8 -*- 
"""
Created on 2021/9/7 13:54 
@File  : get_pfl_consignment.py
@author: zhoul
@Desc  :
"""
from commonfunc.encrypt_tool import EncryptTool
from commonfunc.datetime_tool import DateTimeTool


class PFLConsignment:

    def __init__(self):
        self.path='/api/v2/Consignment'
        self.apiKey = '0639285a-0ec4-11ec-82a8-0242ac130003'
        self.secretKey = 'c276a773-7ec5-4e6c-8d80-95f21ec858e0'
        self.headers = {
            "ApiKey": self.apiKey,
            "Authorization": "",
            "TimeStamp": DateTimeTool.get_now_time_stamp_with_second()
        }

    def get_consignment(self, body):
        pass