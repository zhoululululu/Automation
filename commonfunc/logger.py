# -*- coding: UTF-8 -*-
'''
Created on 2021/7/12 16:38
@File  : get_logging.py
@author: zhoul
@Desc  :
'''
import os, sys
import logging

from commonfunc.yaml_manage import YamlManage

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class Logging:

    def __init__(self):
        logging_yaml = YamlManage(rootPath+"\\config\\log.yaml").get_all_data()
        logging.config.dictConfig(config=logging_yaml)


root = logging.getLogger()

# 子记录器的名字与配置文件中loggers字段内的保持一致
my_module = logging.getLogger("my_module")
print("rootlogger:", root.handlers)
print("selflogger", my_module.handlers)
# print("子记录器与根记录器的handler是否相同：", root.handlers[0] == my_module.handlers[0])
my_module.error("DUBUG")
root.info("INFO")
root.error('ERROR')
root.debug("rootDEBUG")
