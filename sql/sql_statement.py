# -*- coding: utf-8 -*- 
"""
Created on 2021/7/7 14:07 
@File  : sql_statement.py
@author: zhoul
@desc  : 日常操作所需的sql语句
"""

from commonfunc.db_client import MysqlClient
from commonfunc.datetime_tool import DateTimeTool
from commonfunc.get_logging import Logging

logger = Logging()


class OCSqlStatement(object):

    def __init__(self, env):
        """
        连接数据库
        :param env:
        """
        self.cursor = MysqlClient(env)

    def get_dis_list(self, station_code):
        """
        查校验的地区编码
        :param station_code: 地区编码
        :return:
        """
        select_address_code = (
                "select station_province,station_city,station_area from t_vendor_station "
                "where station_code= '%s' and is_active=1 limit 1;" % station_code)
        return self.cursor.execute_sql(sql=select_address_code)[0][0]

    def check_product(self, tracking_number):
        """
        检查产品计算是否有错
        :param tracking_number: 物流单号
        :return:
        """
        confirm_shipment_error = (
                "select error_reason from t_waybill_confirm_shipment_error where tracking_number='%s';" % tracking_number)
        shipment_error_result = self.cursor.execute_sql(sql=confirm_shipment_error)[0][0]
        product_error = (
                "select error_reason from t_waybill_product_error  where tracking_number='%s';" % tracking_number)
        product_error_result = self.cursor.execute_sql(sql=product_error)[0][0]
        if shipment_error_result:
            return "shipment_error：'%s'" % shipment_error_result
        elif product_error_result:
            return "product_error:'%s'" % product_error_result
        else:
            pass

    def get_max_num(self):
        """
        获取号段最大值???
        :return:
        """
        select_list_num = "select listnum from t_test_num where is_active =1 order by listnum desc limit 1"
        return self.cursor.execute_sql(sql=select_list_num)[0][0]

    def header_num(self):
        """
        获取头程号段
        :return:
        """
        select_list_num = "select listnum from t_test_num where is_active =1 order by listnum asc limit 1"
        return self.cursor.execute_sql(sql=select_list_num)[0][0]

    def update_num(self, tracking_number, sys_user, list_num):
        """
        更新号段表
        :param tracking_number:物流订单号
        :param sys_user: 操作人
        :param list_num: 号段
        :return:
        """
        sql_update = (
                "update t_test_num set tracking_number='%s',sysuser='%s',modify_time='%s',is_active=0 where listnum ='%s'" % (
            tracking_number, sys_user, DateTimeTool.get_after_day_time(), list_num))
        self.cursor.execute_sql(sql=sql_update)

    def insert_num(self, va1, va2):
        """
        插入新号段,va1,va2为号段范围
        :param va1: 号段范围
        :param va2:号段范围
        :return:
        """
        for i in range(va1, va2 + 1):
            sql_insert = "insert into t_test_num (listnum,is_active) values ('%s', '%s')" % (i, 1)
            self.cursor.execute_sql(sql=sql_insert)


class TaurusSqlStatement(object):

    def __init__(self, env):
        """
        连接数据库
        :param env:
        """
        self.cursor = MysqlClient("taurus_" + env)

    def taurus_code(self, country):
        """
        获取货币代码
        :param country: 国家
        :return:
        """
        select_currency_code = (
                "select currency_code from t_fin_base_currency where is_active =1 and currency_country='%s'" % country)
        return self.cursor.execute_sql(sql=select_currency_code)[0][0]


class RDCSqlStatement(object):

    def __init__(self, sortation, env):
        """
        连接数据库
        :param env:
        """
        self.cursor = MysqlClient(sortation + "_" + env)

    def select_t_waybill(self, tracking_number):
        """
        检查订单是否到达RDC
        :param tracking_number: 物流订单号
        :return:
        """
        check_racking_number = ("select tracking_number from t_waybill where tracking_number='%s'" % tracking_number)
        result = self.cursor.execute_sql(sql=check_racking_number)
        return result[0][0] if result != () else ""

    def select_bpost(self, sorting_result):
        """
        检查是否为比邮包
        :param sorting_result: 细分结果
        :return:
        """
        last_mile_bag_id = "select last_mile_vendor_service_code from t_sort_dock_logic where sorting_result='%s' and is_active=1" % sorting_result
        result = self.cursor.execute_sql(last_mile_bag_id)
        return result[0][0] if result != () else ""

    def insert_ccei_product(self, tracking_number, hs_code):
        """
        ccei申报处理
        :param tracking_number:物流订单号
        :param hs_code:
        :return:
        """
        sku = ("select id,transaction_id from t_waybill_item where tracking_number='%s'" % tracking_number)
        result = self.cursor.execute_sql(sql=sku)[0]
        ccei_product = (
                "insert into t_ccei_product_name ( id ,tracking_number,item_id ,goods_long_name ,hs_code ,is_active ,"
                "message_id ,create_time ,create_user_code ,modify_time ,modify_user_code ) values ('%s',"
                " '%s', '%s', NULL, '%s', '357281381081944064',"
                "'1', '2020-07-08 11:25:02', 'SYSTEM', '2020-07-08 12:05:01', 'SYSTEM')" % (
                    result[0], tracking_number, result[1], hs_code))
        self.cursor.execute_sql(sql=ccei_product)
        return print("插入ccei_product成功")

    def insert_ccei_declare(self, tracing_number):
        """
        长短品名处理
        :param tracing_number:物流订单号
        :return:
        """
        sku = ("select id,transaction_id from t_waybill_item where tracking_number=''%s''" % tracing_number)
        result = self.cursor.execute_sql(sql=sku)[0]
        ccei_declare = (
                "insert into `t_ccei_declare` (`id`, `tracking_number`, `item_id`, `contraband`, `contraband_note`, "
                "`ipr`, `ipr_note`, `goods_short_name`, `goods_long_name`, `goods_cn_name`, `message_id`, `result_type`,"
                " `is_active`, `create_time`, `create_user_code`, `modify_time`, `modify_user_code`) values "
                "('%s', '%s', '%s', '1',"
                " '', '1', '', 'CCEI-短品名', '', 'CCEI-测试6', '2948173', NULL, '1', '2020-07-26 15:59:01',"
                " 'SYSTEM', '2020-07-26 15:59:01', 'SYSTEM')" % (result[0], tracing_number, result[1]))
        self.cursor.execute_sql(sql=ccei_declare)
        return print("插入ccei_declare成功")

    def select_t_scan_package(self, tracking_number):
        """
        查询建包数据
        :param tracking_number: 物流订单号
        :return:
        """
        package = ("select waybill.package_properties,package.first_sorting_result,package.sorting_result,"
                   "package.lastmile_tracking_number,package.weight,consignee.consignee_country from t_waybill waybill"
                   "left join t_scan_package package on waybill.tracking_number = package.tracking_number and "
                   "package.is_active = 1 and waybill.is_active = 1 left join t_waybill_consignee consignee on "
                   "package.tracking_number = consignee.tracking_number and consignee.is_active = 1 "
                   "where waybill.tracking_number='%s';" % tracking_number)
        return self.cursor.execute_sql(package)[0]

    def select_t_scan_package_weight(self, tracking_number):
        """
        搜索负重相关
        :param tracking_number:物流订单号
        :return:
        """
        bag_weight = (
                "select lastmile_bag_no,weight from t_scan_package where tracking_number='%s' and is_active=1;" % tracking_number)
        return self.cursor.execute_sql(sql=bag_weight)[0]

    def select_out_bag(self, tracking_number_list):
        """
        搜索出库数据
        :param tracking_number_list:物流订单号(列表)
        :return:
        """
        out_bag = (
                "select bag_no,bag_weight,bag_real_weight,destination,destination_code,customs_vendor_code,dest_port_code,"
                "lastmile_service_code,lastmile_vendor_code,line_haul_vendor_code,origin_port_code from t_last_mile_bag "
                "where bag_no in "
                "( select distinct lastmile_bag_no from t_scan_package where tracking_number in %s)" % tracking_number_list)
        return self.cursor.execute_sql(sql=out_bag)[0]

    def select_batch_id(self, tracking_number):
        """
        查询出库交接单
        :param tracking_number:物流订单号(列表)
        :return:
        """
        out_bag = (
                "select distinct bag.batch_id from t_scan_package package left join t_out_bound_batch_package bag on	"
                "package.lastmile_bag_no=bag.package_no "
                "where package.is_active=1 and bag.is_active=1 and package.tracking_number in %s" % tracking_number)
        print(self.cursor.execute_sql(sql=out_bag)[0][0])
        return self.cursor.execute_sql(sql=out_bag)[0][0]

    def get_mawb(self, db, sorting_result):
        """
        查询嘉兴符合要求的主单号
        :param sorting_result:
        :return:
        """
        self.cursor.change_db(db)
        dock_info = ("select lastmile_vendor_code,dest_port_code,customs_vendor_code from t_last_mile_bag_logic"
                     " where is_active=1 and sortation_code ='08' and dock_no ='%s';" % sorting_result)
        dock_info_result = self.cursor.execute_sql(sql=dock_info)[0]
        mawb = ("select mawb from t_acas_inspect_mawb_config where FIND_IN_SET('%s',last_mile_vendor_code) and "
                "destination_port_code='%s' and customs_vendor_code='%s' and sortation_code ='08' and no_associated <>'0'"
                " and is_active=1 LIMIT 1;" % (dock_info_result[0], dock_info_result[1], dock_info_result[2]))
        result_mawb = self.cursor.execute_sql(sql=mawb)[0][0]
        if result_mawb:
            logger.info("找到符合要求的主单：%s" % result_mawb)
            print("找到符合要求的主单：" + result_mawb)
            return result_mawb
        else:
            logger.error("未找到符合要求的主单，主单要求:尾程供应商'%s'，目的口岸'%s'，清关供应商'%s'" % (
                dock_info_result[0], dock_info_result[1], dock_info_result[2]))
            print("未找到符合要求的主单，主单要求:尾程供应商'%s'，目的口岸'%s'，清关供应商'%s'" % (
                dock_info_result[0], dock_info_result[1], dock_info_result[2]))
