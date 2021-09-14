# -*- coding: utf-8 -*- 
"""
Created on 2021/7/7 12:03 
@File  : generate_tracking_number.py
@author: zhoul
@Desc  : 主要用于生成物流追踪单
"""
import random
from sql.sql_statement import OCSqlStatement
import pandas
from commonfunc.datetime_tool import DateTimeTool
from commonfunc.get_logging import Logging
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]

logger = Logging()


class GenerateTrackingNumber(object):

    def __init__(self):
        self.first_sorting_crenel = {1: "01", 2: "02", 3: "03", 4: "04"}  # 初分定义
        self.first_sorting_version = ["A", "B", "C", "D", "E", "F", "G"]
        self.weights = [9, 7, 5, 3, 1, 8, 6, 4, 2]
        self.begin = 4
        self.digit = 9
        self.weight_avg = 9
        self.verify_num = 8
        self.last_mile_code = "00"

    @staticmethod
    def get_sql_result(env):
        mysql = OCSqlStatement(env)
        flow_num = mysql.header_num()
        max_num = mysql.get_max_num()
        return flow_num, max_num

    @staticmethod
    def get_generate_product_code(service_code):
        """
        产品code：EM，ES，EE，EX
        :param service_code:
        :return:
        """
        return service_code

    def get_verify_code_generate(self, flow_num, max_num):
        """
        使用12位流水号，生成1位验证位
        :param max_num:
        :param flow_num:
        :return:
        """
        if flow_num <= max_num:
            int_sum = 0
            for i in range(self.digit):
                int_sum = int_sum + (int(flow_num[i + self.begin - 1:i + self.begin]) * self.weights[i])
            verify_code = (int_sum % self.weight_avg + self.verify_num) % 10
            return flow_num + str(verify_code)
        else:
            logger.error('号段不足，请及时更新！')
            raise Exception('号段不足，请及时更新！')

    @staticmethod
    def get_last_mile_code(last_mile_code):
        """
        2位尾程供应商
        :param last_mile_code:
        :return:
        """
        return str(last_mile_code)

    @staticmethod
    def get_validation_param_dto(sortation_code='01'):
        """
        获取2位分拣中心
        :param sortation_code: 分拣中心
        :return:
        """
        return str(sortation_code)

    def get_first_sorting_version_code(self):
        """
        获取初分版本号
        :return:
        """
        code = random.choice(self.first_sorting_version)
        return str(code)

    def get_first_sorting_result(self, last_country):
        """
        获取2位初分垛口
        :param last_country:
        :return:
        """
        if last_country in ['NG', 'IB', 'UP']:
            return self.first_sorting_crenel[1]
        elif last_country == 'UB':
            return self.first_sorting_crenel[2]
        elif last_country == 'OW':
            return self.first_sorting_crenel[3]
        else:
            return self.first_sorting_crenel[4]

    @staticmethod
    def get_generate_sorting_crenel_code(product_code):
        """
        获取细分垛口号
        :param product_code: 产品code
        :return:
        """
        if "ES" == product_code:
            return "0001"
        elif "EX" == product_code:
            return "0002"
        elif "EE" == product_code:
            return "0003"
        else:
            return "0003"

    @staticmethod
    def get_sorting_version_code(sorting_version_code=0):
        """
        获取细分版本号
        :param sorting_version_code:
        :return:
        """
        return str(sorting_version_code)

    @staticmethod
    def get_charge(ch=0):
        """
        获取1位带电标识 A不带电，B带电
        :param ch:
        :return:
        """
        if ch == 0:
            return 'D'
        else:
            return 'N'

    def generate_tracking_num(self, env, service_id, num=1):
        """
        规则如下：
        # 2位通过产品ID获取 product_code
        # 12位流水号 1位生成验证位verify_code
        # 2位尾程供应商 last_mile_code
        # 2位分拣中心 sorting_center_code
        # 2位初分垛口 first_sorting_crenel_code
        # 4位细分垛口 sorting_crenel_code
        # 1位初分版本号 first_sorting_version_code
        # 1位细分分版本号     sorting_version_code = '0'
        # 1位带电标识 不带电，N带电 charge
        :return: tracking_number_list
        """
        tracking_number_list = []
        for i in range(num):
            # 以下一系列操作为获取trackingNumber所需的规则条件
            flow_num, max_num = self.get_sql_result(env)
            product_code = self.get_generate_product_code(service_id)  # 2位通过产品ID获取 product_code
            verify_code = self.get_verify_code_generate(flow_num, max_num)  # 12位流水号 1位生成验证位verify_code
            sorting_center_code = self.get_validation_param_dto()  # 2位分拣中心 sorting_center_code
            first_sorting_crenel_code = self.get_first_sorting_result(3)  # 2位初分垛口 first_sorting_crenel_code
            sorting_crenel_code = self.get_generate_sorting_crenel_code(service_id)  # 4位细分垛口 sorting_crenel_code
            first_sorting_version_code = self.get_first_sorting_version_code()  # 1位初分版本号 first_sorting_version_code
            sorting_version_code = self.get_sorting_version_code()  # 1位细分分版本号     sorting_version_code = '0'
            charge = self.get_charge()  # 1位带电标识 不带电，N带电 charge
            # 拼接trackingNumber
            tracking_number = product_code + verify_code + self.last_mile_code + sorting_center_code + first_sorting_crenel_code + sorting_crenel_code + first_sorting_version_code + sorting_version_code + charge
            tracking_number_list.append(tracking_number)
            OCSqlStatement(env).update_num(tracking_number, "test_ZL", flow_num)
            logger.info("生成为头程号段为 : %s" % tracking_number)
            logger.info("生成为订单号为 : %s" % flow_num)
        return tracking_number_list

#
# if __name__ == '__main__':
# #     # 入参分别为：env,rdc,service_type,num
#     tracking_number = GenerateTrackingNumber().generate_tracking_num('test', "ES", num=1)
#     print(tracking_number)
    # 生成tracking-numbers文件
    # pandas.DataFrame({"trackingNumber": tracking_number}).to_csv(
    #     rootPath + "\\testresults\\trackingnumber\\" + str(
    #         DateTimeTool.get_now_time(time_format='%Y-%m-%d-%H-%M-%S')) + "-tracking-numbers.csv")
