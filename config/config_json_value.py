# -*- coding: utf-8 -*- 
"""
Created on 2021/7/8 13:35 
@File  : config_json_value.py
@author: zhoul
@Desc  :
"""
from config.get_config import Config
from sql.sql_statement import OCSqlStatement, RDCSqlStatement, TaurusSqlStatement
from commonfunc.datetime_tool import DateTimeTool
import json
from case.generate_tracking_number import GenerateTrackingNumber


class ConfigJsonValue(object):

    def __init__(self, env, sortation, service_id, country, battery, tracking_num):
        """
        初始化
        :param env: 环境
        :param service_id: 订单的服务：ES标准，EE经济等等
        :param config_type: 读取yaml的参数：json为读取json参数
        """
        self.env = env
        self.sortation = sortation
        self.service_id = service_id
        self.country = country
        self.battery = battery
        self.config = Config("json").get_json_value(country)  # 获取特定国家对应的收件人信息
        self.url_config = Config("url").get_urls(env, sortation)
        self.sql_config = Config("sql").get_sql_info(env, sortation)
        self.oc_cursor = OCSqlStatement(env)
        self.rdc_cursor = RDCSqlStatement(sortation, env)
        self.ts_cursor = TaurusSqlStatement(self.env)
        self.tracking_number = tracking_num  # GenerateTrackingNumber().generate_tracking_num(self.env, self.service_id)[0]

    def get_ship_order_data(self, package_total_weight, sku_value):
        """
        封装IS下单参数
        :param country: 国家
        :param package_total_weight: 包裹重量
        :param sku_value: 申报价格
        :param battery: 是否带电；1带电，其余不带电
        :return: 下单参数
        """
        currency = self.ts_cursor.taurus_code(self.country)  # 获取国家的货币
        # 对下单参数进行封装操作
        final_ship_order_data = eval(
            self.config["ship_order"] % (
                self.sql_config["is_id"], self.sql_config["is_id"], self.url_config["drop_site_id"],
                self.sql_config["seller_addr_id"],
                self.country, self.config["consignee_state"], self.config["consignee_city"],
                self.config["address"],
                self.config["address2"], self.config["consignee_zip_code"],
                self.tracking_number,
                self.service_id, package_total_weight, currency, sku_value, currency))
        # 额外操作: 如果带电的话，目前暂不支持多商品
        if self.battery == "1":
            final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0]["batteryType"] = "PI969SEC2"
            final_ship_order_data["data"]["packageInfoList"][0]["itemInfoList"][0]["elecQuaID"] = "5371610785472"
        return self.tracking_number, final_ship_order_data

    def get_b_post_data(self, sortation_code):
        """
        封装比邮大包号接口参数
        :param sortation_code: 分拣中心
        :return: 下单参数
        """
        b_post_data = eval(
            self.config["get_last_mile_bag"] % (
                sortation_code, DateTimeTool.get_now_time(), DateTimeTool.get_now_time()))

        return b_post_data

    def get_letter_data(self, sortation_code):
        """
        封装打标接口参数
        :param sortation_code: 分拣中心
        :return: 下单参数
        """
        # 二话不说,先判断分拣中心是东莞还是非东莞,封装letter_data,因为入参有略微不同
        letter_data = eval(
            self.config["get_letter_dg"] % (
                sortation_code, self.tracking_number, DateTimeTool.get_now_time())) if sortation_code == "05" else eval(
            self.config["get_letter_not_dg"] % (sortation_code, self.tracking_number, DateTimeTool.get_now_time(),
                                                DateTimeTool.get_now_time()))
        return self.tracking_number, letter_data

    def get_label_data(self, sortation_code, package_weight):
        """
        封装分拣换单接口参数
        :param sortation_code: 分拣中心
        :param package_weight: 包裹重量
        :return: 下单参数
        """
        # 同样二话不说,先判断分拣中心是东莞还是非东莞,封装label_data,因为入参有略微不同
        label_data = eval(
            self.config["get_label_dg"] % (
                DateTimeTool.get_now_time(), package_weight, self.tracking_number)) if sortation_code == "05" else eval(
            self.config["get_label_not_dg"] % (
                DateTimeTool.get_now_time(), package_weight, self.tracking_number, sortation_code,
                DateTimeTool.get_now_time()))
        return self.tracking_number, label_data

    def get_bu_bag_data(self, sortation_code, bag_real_weight, first_sorting_result, sorting_result,
                        last_mile_tracking_number, b_post_id=None):
        """
        封装分拣换单接口参数，不过暂时不做多小包结包，后期在优化吧
        :param sortation_code: 分拣中心
        :param bag_real_weight: 包裹重量
        :param first_sorting_result: 初分垛口
        :param sorting_result: 细分垛口
        :param last_mile_tracking_number: 尾程面单号
        :param b_post_id: 比邮大包号
        :return: 下单参数
        """
        # 先封装参数
        status = False
        bu_bag_data = eval(
            self.config["bu_bag"] % (
                sortation_code, bag_real_weight, self.battery, first_sorting_result, sorting_result,
                DateTimeTool.get_now_time(), last_mile_tracking_number, DateTimeTool.get_now_time()))
        # 如果是美国且是嘉兴仓的订单，需要加入mawb参数
        if self.country == "US" and sortation_code == "08":
            bu_bag_data["data"]["mawb"] = self.rdc_cursor.get_mawb(sorting_result)
        last_mile_bag_id = self.rdc_cursor.select_bpost(sorting_result)
        if last_mile_bag_id in ("UBIEUSEMI", "UBICASEMI"):
            status = True
            print("比邮大包,需要走比邮建包流程...")
            bu_bag_data["data"]["lastMileBagId"] = b_post_id  # 赋值比邮大包号
        return bu_bag_data, status

    def get_bag_weight_data(self, bag_real_weight, bag_id):
        """
        封装负重接口参数
        :param bag_real_weight: 包裹重量
        :param bag_id: 大包号
        :return: 负重接口参数
        """
        bag_weight_data = eval(self.config["bag_weight"] % (bag_real_weight, bag_id, DateTimeTool.get_now_time()))
        return bag_weight_data

    def get_out_package_data(self, bag_id):
        """
        封装出库接口参数
        :param bag_id: 大包号
        :return: 负重接口参数
        """
        out_package_data = eval(
            self.config["out_package"] % (
                bag_id, DateTimeTool.get_now_time(), DateTimeTool.get_now_time_stamp_with_second(),
                DateTimeTool.get_now_time(), DateTimeTool.get_how_days_after(1), DateTimeTool.get_now_time()))
        return out_package_data

#
# if __name__ == '__main__':
#     # env, sortation, service_id, country, battery, config_type="json"
#     #     # ConfigJsonValue("test", "ES", "GB").get_letter_data("05")
#     #     ConfigJsonValue("test", "ES", "GB", "1").get_out_package_data("07")
#     # ConfigJsonValue("test", "ES", "US", "1").get_bu_bag_data("08", "100", "1", "51")
#     # ConfigJsonValue("test", "ES", "GB").get_label_data("08", "500")
#     ConfigJsonValue("test", 'dg', "ES", 'DE', '1').get_ship_order_data(100, 1)
