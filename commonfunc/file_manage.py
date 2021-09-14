# -*- coding: utf-8 -*- 
"""
Created on 2021/5/20 9:10 
@File  : file_manage.py
@author: zhoul
@Desc  :
"""

import json
import pandas
import os
from commonfunc.get_logging import Logging

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]

logger = Logging()


class FileManage:

    @staticmethod
    def file_to_dict(path, sheet_name=None):
        test_data = []
        form = str(path).split(".")[-1]
        try:
            if form == "txt":
                f = open(path, "r", encoding="UTF-8")
                for line in f.readlines():
                    test_data.append(line.strip("\n"))

            elif form == "csv":
                test_data = pandas.read_csv(path, encoding="utf-8")

            elif form == "xls" or form == "xlsx":
                test_data = pandas.read_excel(path, sheet_name=sheet_name, dtype=object)
                return test_data

            elif form == "json":
                with open(path, mode='r', encoding='utf-8') as f2:
                    test_data = json.load(f2)

        except Exception as e:
            print(e)
        return test_data

    @classmethod
    def check_file(cls, file_path):
        if not os.path.exists(file_path):
            logger.error("请求参数文件不存在,请检查文件： %s" % file_path)
            return True
        else:
            return False
