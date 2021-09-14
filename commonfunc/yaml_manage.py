# -*- coding: utf-8 -*- 
"""
Created on 2021/5/26 13:50 
@File  : yaml_manage.py
@author: zhoul
@Desc  :
"""
import os
from ruamel import yaml

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class YamlManage:

    def __init__(self, file):
        self.file = file
        with open(file, encoding='utf-8') as file:
            self.data = yaml.load(file.read(), Loader=yaml.Loader)

    def get_all_data(self):
        return self.data

    def read_yaml(self, title, key=None):
        if key is None:
            return self.data.get(title)
        if type(key) == str:
            return self.data.get(title).get(key)
        else:
            result = self.data.get(title)
            for i in key:
                result = result.get(i)
            return result

    def write_yaml(self, title, key, value):
        """
        yaml写入，data为dict类型{},进行修改或者续写
        :param title:
        :param key:
        :param value:
        :return:
        """
        dict_re = {title: {key: value}}
        if self.data is not None:
            if title not in self.data.keys():
                self.data = dict(self.data, **dict_re)
            else:
                self.data[title][key] = value
        else:
            self.data = dict_re
        with open(self.file, "w", encoding="utf-8") as file:
            yaml.dump(self.data, file, Dumper=yaml.RoundTripDumper)
