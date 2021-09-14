# -*- coding: utf-8 -*- 
"""
Created on 2021/5/20 9:32 
@File  : response_client.py
@author: zhoul
@Desc  :
"""


class HttpResponseResult:
    def __init__(self):
        self.status_code = None
        self.body = None
        self.cookies = None
        self.headers = None
