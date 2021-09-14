# -*- coding: utf-8 -*- 
"""
Created on 2021/7/7 17:42 
@File  : rdc_flow.py
@author: zhoul
@Desc  :
"""
import time

from config.config_json_value import ConfigJsonValue
from api.request_client import RequestClient
from config.get_config import Config
import json
from sql.sql_statement import RDCSqlStatement
from commonfunc.sleep_tool import SleepTool
from commonfunc.get_logging import Logging

logger = Logging()


class RdcFlow:
    def __init__(self, env, sortation, service_id, ship_country, battery, tracking_num):
        self.env, self.sortation, self.battery = env, sortation, battery
        self.urls = Config("url").get_urls(env, sortation)
        self.sortation_code = self.urls["sortation_code"]
        self.json_config = ConfigJsonValue(self.env, self.sortation, service_id, ship_country, self.battery,
                                           tracking_num)
        self.headers = '{"Content-Type": "application/json; charset=UTF-8"}'  # 由于rdc所有的操作都是post-json,直接预设header
        self.bag_id, self.first_sorting_result, self.sorting_result, self.b_post_id, self.last_mile_tracking_number = "", "", "", "", ""
        self.rdc_cursor = RDCSqlStatement(sortation, env)
        self.status = False

    def ship_order(self, package_total_weight, sku_value):
        """
        IS下单
        :param package_total_weight: 包裹重量
        :param sku_value: 商品申报金额
        :return:
        """
        re_tracking_number, ship_order_data = self.json_config.get_ship_order_data(
            package_total_weight,
            sku_value)
        ship_order_response = RequestClient(self.urls["ship_order"]).get_simple_request("post", ship_order_data,
                                                                                        headers=self.headers)

        logger.info("IS下单订单 : %s" % re_tracking_number)
        logger.info("IS下单入参 : %s" % ship_order_data)
        logger.info("IS下单结果 : %s" % ship_order_response)

        # logger.info("******************IS同步订单至RDC中******************")
        # self.status = SleepTool.wait_for_tracking_number(self.sortation, self.env, re_tracking_number)
        # if self.status is True:
        #     logger.info("******************IS同步订单至RDC成功******************")
        # else:
        #     logger.info("******************IS同步订单至RDC失败******************")

        return re_tracking_number

    def get_letter(self):
        """
        打标
        :return:
        """
        re_tracking_number, letter_data = self.json_config.get_letter_data(self.sortation_code)
        get_letter_response = RequestClient(self.urls["get_letter"]).get_simple_request("post", letter_data,
                                                                                        headers=self.headers)

        logger.info("打标订单 : %s" % re_tracking_number)
        logger.info("打标入参 : %s" % letter_data)
        logger.info("打标结果 : %s" % get_letter_response)

    def get_label(self, package_weight):
        """
        换单
        :param package_weight:
        :return:
        """
        re_tracking_number, label_data = self.json_config.get_label_data(self.sortation_code, package_weight)
        get_label_response = RequestClient(self.urls["get_label"]).get_simple_request("post", label_data,
                                                                                      headers=self.headers,
                                                                                      timeout=999999)

        logger.info("换单订单 : %s" % re_tracking_number)
        logger.info("换单入参 : %s" % label_data)
        logger.info("换单结果 : %s" % get_label_response)

        # 还需要对结果进行收集，收集first_sorting_result,sorting_result,last_mile_tracking_number等(后续流程需要)
        if self.sortation == "dg":
            self.first_sorting_result = get_label_response["result"]["firstSortingResult"]
            self.sorting_result = get_label_response["result"]["sortingResult"]
            self.last_mile_tracking_number = get_label_response["result"]["lastmileTrackingNumber"]
        else:
            self.first_sorting_result = get_label_response["data"]["firstSortingResult"]
            self.sorting_result = get_label_response["data"]["sortingResult"]
            self.last_mile_tracking_number = get_label_response["data"]["lastmileTrackingNumber"]

        logger.info("收集参数 : {firstSortingResult: %s }" % self.first_sorting_result)
        logger.info("收集参数 : {sortingResult:%s }" % self.sorting_result)
        logger.info("收集参数 : {lastmileTrackingNumber: %s }" % self.last_mile_tracking_number)
        return self.last_mile_tracking_number

    def get_b_post(self):
        b_post = self.json_config.get_b_post_data(self.sortation_code)
        get_b_post_response = RequestClient(self.urls["get_last_mile_bag"]).get_simple_request("post", b_post,
                                                                                               headers=self.headers)

        logger.info("获取比邮号入参 : %s" % b_post)
        logger.info("获取比邮号结果 : %s" % get_b_post_response)

        return get_b_post_response

    def bu_bag(self, bag_real_weight):
        """
        建包; 需要分拣后的初分垛口，细分垛口，尾程面单号
        :param bag_real_weight:
        :return:
        """
        bu_bag_data, status = self.json_config.get_bu_bag_data(self.sortation_code, bag_real_weight,
                                                               self.first_sorting_result,
                                                               self.sorting_result,
                                                               self.last_mile_tracking_number)
        if status is True:
            logger.info("该订单需要获取比邮号，准备进行比邮大包号获取")
            b_post_data = self.get_b_post()["data"]["lastMileBagIdStart"]
            logger.info("获取比邮号入参 : %s" % b_post_data)
            bu_bag_data["data"]["lastMileBagId"] = b_post_data
        bu_bag_response = RequestClient(self.urls["bu_bag"]).get_simple_request("post", bu_bag_data,
                                                                                headers=self.headers)

        logger.info("建包订单 : %s" % self.last_mile_tracking_number)
        logger.info("建包入参 : %s" % bu_bag_data)
        logger.info("建包结果 : %s" % bu_bag_response)
        # 收集bag_id信息啦,准备负重出库！
        if self.sortation == "dg":
            self.bag_id = bu_bag_response["data"]["bagId"]
        else:
            self.bag_id = bu_bag_response["data"]["bagId"]
        return self.bag_id

    def real_weight(self, bag_real_weight):
        """
        负重; 需要建包后的bag_id
        :param bag_real_weight: 实际重量
        :return:
        """
        if self.sortation == "dg":
            real_weight_data = self.json_config.get_bag_weight_data(bag_real_weight, self.bag_id)
            real_weight_response = RequestClient(self.urls["bag_weight"]).get_simple_request("post", real_weight_data,
                                                                                             headers=self.headers)
            logger.info("负重订单 : %s" % self.bag_id)
            logger.info("负重入参 : %s" % real_weight_data)
            logger.info("负重结果 : %s" % real_weight_response)
        else:
            logger.info("嘉兴订单无需负重")
            pass

    def out_package(self):
        """
        出库
        :return:
        """
        out_package_data = self.json_config.get_out_package_data(self.bag_id)
        out_package_response = RequestClient(self.urls["out_package"]).get_simple_request("post", out_package_data,
                                                                                          headers=self.headers)
        logger.info("出库订单 : %s" % self.bag_id)
        logger.info("出库入参 : %s" % out_package_data)
        logger.info("出库结果 : %s" % out_package_response)

    def test_run(self):
        last_tracking_num, bag_list, exp = [], [], []
        tracking_list = ['ES10000210984420001010001D0N', 'ES10000210984300001010001A0N', 'ES10000210984280001010001A0N',
                         'ES10000210984150001010001D0N']

        for i in tracking_list:
            rdc_flow = RdcFlow("pre", "dg", "ES", "IL", "0", i)
            last_mile_tracking_number = rdc_flow.get_label(200)
            last_tracking_num.append(last_mile_tracking_number)
            bag_id = rdc_flow.bu_bag(200)
            bag_list.append(bag_id)
            rdc_flow.real_weight(200)
            rdc_flow.out_package()
            exp.append({last_mile_tracking_number: i})
        print(tracking_list)
        print(last_tracking_num)
        print(bag_list)
        print(exp)

    def test_run_all(self):
        num = 1
        tracking_list, last_tracking_num, bag_list, exp = [], [], [], []
        for i in range(num):
            print(i)
            rdc_flow = RdcFlow("pre", "dg", "ES", "IL", "0")
            tracking_number = rdc_flow.ship_order(100, 1)
            tracking_list.append(tracking_number)
            rdc_flow.get_letter()
            if rdc_flow.status is True:
                last_mile_tracking_number = rdc_flow.get_label(200)
                last_tracking_num.append(last_mile_tracking_number)
                bag_id = rdc_flow.bu_bag(200)
                bag_list.append(bag_id)
                rdc_flow.real_weight(200)
                rdc_flow.out_package()
            else:
                logger.info("订单同步失败，请检查订单")
            exp.append({last_mile_tracking_number: tracking_number})
        print(tracking_list)
        print(last_tracking_num)
        print(bag_list)
        print(exp)


if __name__ == '__main__':
    num = 6
    tracking_list, last_tracking_num, bag_list, exp = ['ES30000090543410001040001D0D'], [], [], []
    for i in range(len(tracking_list)):
        rdc_flow = RdcFlow("pre", "jx", "ES", "SE", "0", tracking_list[i])
        # tracking_number = rdc_flow.ship_order(100, 1)
        # tracking_list.append(tracking_number)
        # rdc_flow.get_letter()
        # if rdc_flow.status is True:
        last_mile_tracking_number = rdc_flow.get_label(2000)
        last_tracking_num.append(last_mile_tracking_number)
        time.sleep(1)
        bag_id = rdc_flow.bu_bag(2000)
        bag_list.append(bag_id)
        rdc_flow.real_weight(2000)
        rdc_flow.out_package()
        # else:
        #     logger.info("订单同步失败，请检查订单")
        # exp.append({last_mile_tracking_number: tracking_number})
    print(tracking_list)
    print(last_tracking_num)
    print(bag_list)
    print(exp)
