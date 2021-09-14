# -*- coding: utf-8 -*- 
"""
Created on 2021/5/26 10:04 
@File  : scorpio_package.py
@author: zhoul
@Desc  :
"""
from commonfunc.db_client import MysqlClient


class ScorpioPackage(object):

    def __init__(self, trucking_number, env, rdc):
        """
        初始化数据库相关内容，传入需要做
        :param trucking_number:
        """
        self.trucking_number = trucking_number
        self.aq_conn = MysqlClient(env + "_aq")
        if rdc == "dg":
            self.rdc_conn = MysqlClient(env + "_dg")
        elif rdc == "jx":
            self.rdc_conn = MysqlClient(env + "_jx")


    def check_rdc_waybill_route_expected(self):
        """
        查询订单预期路由，若有预期路由则证明该订单开始交运
        :return:
        """
