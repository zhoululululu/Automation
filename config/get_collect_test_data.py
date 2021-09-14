# -*- coding: UTF-8 -*-
"""
Created on 2020/2/29
@File  : get_collect_test_data.py
@author: zhoul
@Desc  :
"""

import os
from commonfunc.get_logging import Logging
from commonfunc.yaml_manage import YamlManage

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class GetCollectTestData(object):
    def __init__(self):
        """
        初始化config，读取config文件
        """
        self.logging = Logging()
        self.file_path = rootPath + "\\config\\test_data.yaml"
        self.config = YamlManage(self.file_path)
        self.conf = {}

    def get_is_test_data(self):
        """
        获取email的各种参数配置值
        """
        self.conf['is_id'] = self.config.read_yaml("IS", "is_id")
        self.conf['token'] = self.config.read_yaml("IS", "token")
        self.conf['cookie'] = self.config.read_yaml("IS", "cookie")
        return self.conf

    def set_is_test_data(self, title, key, value):
        """
        修改yaml数据
        """
        try:
            self.config.write_yaml(title, key, value)
            self.logging.info("%s 文件修改成功  title为：%s，key为：%s，value修改为： %s" % (self.file_path, title, key, value))
        except Exception as e:
            self.logging.error("%s 文件修改失败  请检查title或key值" % (self.file_path))
            raise e
