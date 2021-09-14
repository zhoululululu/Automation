# -*- coding: utf-8 -*-
"""
Created on 2021/5/19 22:46
@File  : sleep_tool.py
@author: zhoul
@Desc  :
"""
import time
from commonfunc.get_logging import Logging
from sql.sql_statement import RDCSqlStatement
import os

logger = Logging()


class SleepTool:

    def __init__(self):
        pass

    @classmethod
    def wait_for_tracking_number(cls, env, sortation, tracking_number):
        num = 0
        status = False
        while 1:
            check_racking_number = RDCSqlStatement(env, sortation).select_t_waybill(tracking_number)
            if check_racking_number != "":
                status = True
                print("订单已到达指定分拣中心->%s,订单准备完成，开始下一步流程..." % tracking_number)
                break
            elif num > 30:
                logger.error("订单同步分拣中心失败，请检查系统!!!")

                break
            else:
                time.sleep(30)
                logger.info("订单未到达分拣中心，继续请求中...")
                num += 1
        return status

    @classmethod
    def wait_for_time(cls, second):
        pass

    @classmethod
    def execute_frequency(cls, second):
        pass
