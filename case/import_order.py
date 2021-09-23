# -*- coding: utf-8 -*- 
"""
Created on 2021/5/26 15:22 
@File  : import_order.py
@author: zhoul
@Desc  :
"""
import os
from api.request_client import RequestClient
from commonfunc.get_logging import Logging

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
from datetime import date, datetime, timedelta


class ImportOrder(object):

    def __init__(self, url, is_id, file, num, country):
        """
        初始化订单导入所需要的的参数值
        :param is_id: isid
        :param file: 导入订单文件
        :param num: 导入数量
        :param country: 导入国家
        """
        self.logging = Logging()
        self.is_id = is_id
        self.file = file
        self.num = num
        self.country = country
        self.request = RequestClient(url)

    def import_order(self):
        """
        订单导入接口，分为两步:上传文件，提交请求
        get_request参数如下:url, method, headers=None, data=None, params=None, file_key=None, file_value=None
        :return:
        """
        # 定义order1参数
        data1 = {
            "orderSource": "1",
            "ebayId": "test",
            "uid": "ANONYMOUS",
            "isId": self.is_id
        }
        # 定义order2参数
        data2 = {
            "orderSource": 1,
            "country": self.country,
            "ebayId": "test",
            "importSum": self.num,
            "uid": "ANONYMOUS",
            "isId": self.is_id
        }

        self.logging.info("is上传文件，接口请求数据：%s" % data1)
        # 第一步：点击上传订单
        response1 = self.request.get_request(
            port="", path="/v1/frontend/importOrder",
            method="post",
            data=data1,
            headers='{"Content-Type": "form-data"}', file_key="file", file_value=self.file)

        print(response1)
        self.logging.info("is上传文件，接口返回数据：%s" % response1)
        # 第二步，提交定单
        if "success" in str(response1):
            self.logging.info("is提交导入，接口请求数据：%s" % data2)
            response2 = self.request.get_request(
                port="", path="/v1/frontend/importOrder2",
                method="post",
                json_value=data2,
                headers='{"Content-Type": "application/json"}', file_value="")
            print(response2)
            self.logging.info("is提交导入，接口返回数据：%s" % response2)


if __name__ == '__main__':
    # 2839139448256143,http://52.175.52.220
    # 8772502972352061,http://isdedis.eastasia.cloudapp.azure.com:18080
    env = "stage"
    if env == "test":
        url = "http://isdedis.eastasia.cloudapp.azure.com:18080"
        isid = "2220040455552376" #2220040455552376,8772502972352061
    elif env == "pre":
        url = "http://52.175.52.220"
        isid = "2668758785280976"
    elif env == "stage":
        url = "https://stage.edisebay.com"
        isid = "2835151170368532"
        #
    ImportOrder(url, isid, rootPath + "\\data\\order.xlsx",
                4, "ES").import_order()
