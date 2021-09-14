# -*- coding: utf-8 -*- 
"""
Created on 2021/8/20 9:49 
@File  : check_sql.py
@author: zhoul
@Desc  :
"""

import pymysql
from commonfunc.db_client import MysqlClient


class CheckSql(object):

    def __init__(self):
        self.test_data = []
        f = open("线上生产单.txt", "r", encoding="UTF-8")
        for line in f.readlines():
            self.test_data.append(line.strip("\n"))
        self.cursor = MysqlClient("pro_oc")

    def check_aq(self):
        pass


if __name__ == '__main__':
    CheckSql()
