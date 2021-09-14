# -*- coding: utf-8 -*-
"""
Created on 2021/5/19 22:46
@File  : get_faker.py
@author: zhoul
@Desc  :
"""
import numbers
import random
import string
import uuid
from case.generate_tracking_number import GenerateTrackingNumber
from faker import Faker
from sql.sql_statement import TaurusSqlStatement

fake = Faker(locale='zh_CN')


class CreatData(Faker):
    # 汉字编码的范围
    ch_start = 0x4E00
    ch_end = 0x9FA5

    @classmethod
    def get_person_name(cls):
        """
        随机生成人名
        :return:
        """
        name = fake.name()
        return name

    @classmethod
    def get_id_no(cls):
        """
        随机生成身份证号
        :return:
        """
        id_no = fake.ssn()
        return id_no

    @classmethod
    def get_phone_no(cls):
        """
        随机生成手机号
        :return:
        """
        phone = fake.phone_number()
        return phone

    @classmethod
    def get_email(cls):
        """
        随机生成邮箱地址
        :return:
        """
        email = fake.email()
        return email

    @classmethod
    def get_province(cls):
        """
        随机生成省份
        :return:
        """
        province = fake.province()
        return province

    @classmethod
    def get_address(cls):
        """
        随机生成地址 eg：海南省上海市朝阳邱路y座 175208
        :return:
        """
        address = fake.address()
        return address

    @classmethod
    def get_three_no(cls):
        """
        随机生成三位数
        :return:
        """
        three_number = fake.random_number(digits=3)
        return three_number

    @classmethod
    def get_varchar(cls, str_len: int):
        """
        生成一个指定长度的随机字符串，str_len为字符串长度
        :param str_len:
        """
        str_list = [random.choice(string.digits + string.ascii_letters) for i in range(str_len)]
        random_str = ''.join(str_list)
        return random_str

    @classmethod
    def get_num(cls, num_len: int):
        """
        生成一个指定长度的随机数字串，num_len为数字串长度
        :param num_len:
        """
        num_list = [str(random.randint(0, 9)) for i in range(num_len)]
        random_num = ''.join(num_list)
        return int(random_num)

    @classmethod
    def get_uuid(cls, source):
        """
        字符串加上uuid
        :param source:
        :return:
        """
        return source + '_' + str(uuid.uuid4())

    @classmethod
    def get_punctuation(cls, source):
        """
        字符串加上加上特殊字符
        :param source:
        :return:
        """
        return source + '_' + string.punctuation

    @classmethod
    def get_chinese(cls, ch_num):
        """
        字符串加上加上特殊字符
        :param ch_num:
        :return:
        """
        ch_list = [chr(random.randint(int(cls.ch_start), int(cls.ch_end))) for i in range(ch_num)]
        ch_result = ''.join(ch_list)
        print(ch_result)
        return ch_result

    @classmethod
    def get_currency(cls, env, key, data):
        """
        获取国家货币
        :param env: 环境
        :param key:
        :param data:
        :return:
        """
        cursor = TaurusSqlStatement(env)
        currency = cursor.taurus_code(key)
        data["data"]["consigneeCountry"] = key
        for i in data["data"]["packageInfoList"]:
            i["currency"] = currency
            for j in i["itemInfoList"]:
                j["currency"] = currency
        return data

    @classmethod
    def get_tracking_number(cls, env, service_code, data):
        """
        获取物流追踪号trackingNumber
        :param data:
        :param env:
        :param service_code:
        :return:
        """
        # 入参分别为：env,service_type,num
        for i in data["data"]["packageInfoList"]:
            tracking_number = GenerateTrackingNumber().generate_tracking_num(env, service_code)
            i["trackingNumber"] = tracking_number[0]
        return data


# if __name__ == '__main__':
#     test = str({
#         "timeStamp": 1625131909816,
#         "messageId": "bad2e885076b4147921e6307971e4",
#         "data": {
#             "isId": "2839139448256143",
#             "isMasterId": "2839139448256143",
#             "orderCreatedDate": "2021-07-05T17:31:49+0800",
#             "collectionType": "0",
#             "dropSiteId": "RFD321",
#             "sellerAddrId": "518",
#             "consigneeFullName": "Fabiola Peçanha",
#             "consigneePhone": "0000",
#             "consigneeCountry": "$country+GB",
#             "consigneeState": "Germany",
#             "consigneeCity": "Berlin",
#             "consigneeAddr1": "Willdenowstr. 9",
#             "consigneeAddr2": "",
#             "consigneeZipCode": "13353",
#             "incoterm": 0,
#             "lengthUnit": "0",
#             "weightUnit": "0",
#             "packageInfoList": [
#                 {
#                     "trackingNumber": "ES30000085485130001010001E0N",
#                     "serviceId": "EE",
#                     "packageTotalWeight": 2000.00,
#                     "packageLength": 10.00,
#                     "packageWidth": 10.00,
#                     "packageHeight": 10.00,
#                     "insurancedValue": 2.0,
#                     "currency": "EUR",
#                     "itemInfoList": [
#                         {
#                             "sku": "1623996116735",
#                             "skuDescCn": "尺子",
#                             "skuDesc": "rule",
#                             "skuWeight": 2000.00,
#                             "skuValue": 10.00,
#                             "currency": "EUR",
#                             "transactionId": "1623996116735-1623996116735",
#                             "quantity": 1,
#                             "link": "http://www.ebay.com/itm/1623996116735",
#                             "txnUnitPrice": 1.82,
#                             "txnQty": 1,
#                             "skuListingDesc": "Tissue paper"
#                         }
#                     ],
#                     "packageDesc": "rule",
#                     "packageDescCn": "尺子",
#                     "packageId": "930093704194457692"
#                 }
#             ],
#             "sendProvinceName": "广东省",
#             "deliveryTime": "Jul 1, 2021 5:31:49 PM"
#         }
#     })
#     CreatData.get_currency("GB", test)
if __name__ == '__main__':
    print(CreatData().get_chinese(12))
