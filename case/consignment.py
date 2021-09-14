# -*- coding: utf-8 -*- 
"""
Created on 2021/5/26 16:38 
@File  : consignment.py
@author: zhoul
@Desc  :
"""
import json
from config.get_collect_test_data import GetCollectTestData
from api.request_client import RequestClient
from commonfunc.get_logging import Logging


class Consignment(object):
    def __init__(self):
        self.logging = Logging()
        self.yaml_data = GetCollectTestData()
        self.session = RequestClient()
        self.login_is()
        self.config = self.yaml_data.get_is_test_data()
        self.cookie, self.token, self.is_id = self.config["cookie"], self.config["token"], self.config["is_id"]
        self.header = {"Content-Type": "application/json", "Connection": "keep-alive", "Cookie": self.cookie,
                       "token": self.token, "language": "zh-cn"}
        self.trucking_number, self.order_data, self.package_data = [], [], []

    def login_is(self):
        header = {"Content-Type": "application/json", "Connection": "keep-alive"}
        login_data = {"userName": "609200751@qq.com",
                      "password": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"}
        self.logging.info("is登录接口，接口请求数据： %s" % login_data)
        login_response = self.session.get_request(
            url="http://isdedis.eastasia.cloudapp.azure.com:18080/v1/frontend/login",
            method="post",
            json=login_data,
            headers=header).body
        self.logging.info("is登录成功，接口返回数据：%s" % login_response)
        self.yaml_data.set_is_test_data("IS", "cookie", "_token=" + json.loads(login_response).get("result"))
        self.yaml_data.set_is_test_data("IS", "token", json.loads(login_response).get("result"))

    def query_order(self, country, num):
        query_data = {"pageNumber": 1, "pageSize": 10, "orderColumn": 3, "buyerUserId": "", "recordNumber": "",
                      "itemId": "",
                      "skuId": "", "paymentStatus": "COMPLETE", "orderStatus": "", "sellerIsId": "", "sellerUserId": "",
                      "startCreateTime": "", "endCreateTime": "", "startPaymentTime": "", "endPaymentTime": "",
                      "shippingCountry": country, "folderId": ""}
        self.logging.info("is查询已支付订单，接口请求数据： %s" % query_data)
        query_order_response = self.session.get_request(
            url="http://isdedis.eastasia.cloudapp.azure.com:18080/v1/frontend/order/queryOrderList",
            method="post",
            json=query_data,
            headers=self.header).body
        self.logging.info("is查询已支付订单，接口返回数据： %s" % query_order_response)
        order_list = json.loads(query_order_response)["data"]["list"]
        if num <= len(order_list):
            for i in range(num):
                self.order_data.append(
                    {"orderId": order_list[i]["orderId"],
                     "orderLineItemList": [order_list[i]["items"][0]["orderLineItem"]]})
                self.logging.info("is查询已支付订单，接口返回所需order_data数据： %s" % self.order_data)
            self.yaml_data.set_is_test_data("IS", "order_data", self.order_data)
        else:
            self.logging.error("所需要的创建的包裹数量%s 大于查询结果数量%s，请手动检查" % (num, len(order_list)))

    def creat_package(self, country, num):
        self.query_order(country, num)
        creat_package_data = {"isId": str(self.is_id),
                              "data": self.order_data}
        self.logging.info("is创建包裹，接口请求数据： %s" % creat_package_data)
        query_order_response = self.session.get_request(
            url="http://isdedis.eastasia.cloudapp.azure.com:18080/v1/frontend/order/orderManagement/createPackage",
            method="post",
            json=creat_package_data,
            headers=self.header).body
        self.logging.info("is创建包裹，接口返回数据： %s" % query_order_response)

    def query_package(self, country, num):
        test.creat_package(country, num)
        query_order_package_data = {"shipToCountry": country,
                                    "sellerEbayId": "", "buyerEbayId": "", "orderId": "", "itemId": "",
                                    "skuNo": "", "isSingle": "ALL", "isBaterry": 0, "superTrackingCode": "",
                                    "isPrinted": "ALL", "isShipped": "ALL", "declareStatus": "",
                                    "buyerServiceGrade": "ALL", "sendDate": "", "status": "SELECTED_SHIPPING",
                                    "preferenceId": "", "pageNo": 1, "pageSize": 10, "logisticsServiceType": 0,
                                    "sorting": "createTimeDESC", "packageStatus": "ALL", "folderId": ""}
        self.logging.info("is查询包裹，接口请求数据： %s" % query_order_package_data)
        query_package_response = self.session.get_request(
            url="http://isdedis.eastasia.cloudapp.azure.com:18080/v1/frontend/packages",
            method="get",
            params=query_order_package_data,
            headers=self.header).body
        package_list = json.loads(query_package_response)["result"]["dataList"]
        if num <= len(package_list):
            for i in range(num):
                self.package_data.append(
                    {"packageIds": [package_list[i]["packageId"]]})
            self.logging.info("is查询包裹，接口返回所需packageIds数据： %s" % self.package_data)
            self.yaml_data.set_is_test_data("IS", "package_data", self.package_data)
        else:
            self.logging.error("所需要的创建的包裹数量%s 大于查询结果数量%s，请手动检查" % (num, len(package_list)))
        self.logging.info("is查询包裹，接口返回数据： %s" % query_package_response)

    def change_receiver_address(self):
        package_id = "910895603325337661"
        change_receiver_address = {"packageId": package_id, "receiverName": "xMan 43",
                                   "receiverCountry": "US", "receiverCountryName": "UnitedStates",
                                   "receiverProvince": "NewYork", "receiverProvinceName": "NewYork",
                                   "receiverCity": "Lancaster", "receiverCounty": "null",
                                   "receiverAddress1": "27 Sawgrass Lane", "receiverAddress2": "address2",
                                   "receiverZipCode": "14086", "receiverPhone": "11231234566", "version": 1}

        self.logging.info("is修改收货地址，接口请求数据： %s" % change_receiver_address)
        query_package_response = self.session.get_request(
            url="http://isdedis.eastasia.cloudapp.azure.com:18080/v1/frontend/package/receiveraddress",
            method="put",
            json=change_receiver_address,
            headers=self.header).body
        self.logging.info("is修改收货地址，接口返回数据： %s" % query_package_response)

    def select_product(self):
        {"packageIds": ["910895688325529661"], "productId": "ES", "version": 0}
        # http://isdedis.eastasia.cloudapp.azure.com:18080/v1/frontend/packages/product/select


if __name__ == '__main__':
    test = Consignment()
    test.change_receiver_address()
