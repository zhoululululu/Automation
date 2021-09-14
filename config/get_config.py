# -*- coding: UTF-8 -*-
"""
Created on 2020/2/29
@File  : get_config.py
@author: zhoul
@Desc  :
"""

import os

from commonfunc.yaml_manage import YamlManage

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class Config(object):
    def __init__(self, type):
        """
        初始化config，读取config文件
        """
        if type == "email":
            self.file_path = rootPath + "\\config\\config.yaml"
        elif type == "url":
            self.file_path = rootPath + "\\config\\http_config.yaml"
        elif type == "sql":
            self.file_path = rootPath + "\\config\\mysql_config.yaml"
        elif type == "json":
            self.file_path = rootPath + "\\config\\json.yaml"
        self.config = YamlManage(self.file_path)
        self.conf = {}

    def get_email_info(self):
        """
        获取email的各种参数配置值
        """
        self.conf['service'] = self.config.read_yaml(self.file_path, "Email", "service")
        self.conf['version'] = self.config.read_yaml(self.file_path, "Email", "version")
        self.conf['tester'] = self.config.read_yaml(self.file_path, "Email", "tester")
        self.conf['remark'] = self.config.read_yaml(self.file_path, "Email", "remark")
        self.conf['is_send'] = self.config.read_yaml(self.file_path, "Email", "is_send")
        self.conf['user'] = self.config.read_yaml(self.file_path, "Email", "user")
        self.conf['password'] = self.config.read_yaml(self.file_path, "Email", "password")
        self.conf['host'] = self.config.read_yaml(self.file_path, "Email", "host")
        self.conf['rec_users'] = self.config.read_yaml(self.file_path, "Email", "rec_users")
        self.conf['title'] = self.config.read_yaml(self.file_path, "Email", "title")
        return self.conf

    def get_sql_info(self, env, sortation="dg"):
        """
        获取mql数据库的各种参数配置值
        :param sortation:
        :param env:the env which you choose
        :return:
        """
        if env in ["test", "pre", "stage"]:
            self.conf["sys_user"] = self.config.read_yaml("author")
            self.conf['url'] = self.config.read_yaml(env, "url")
            self.conf['collection_type'] = self.config.read_yaml(env, [sortation, "collection_type"])
            self.conf['drop_id'] = self.config.read_yaml(env, [sortation, "drop_id"])
            self.conf['is_id'] = self.config.read_yaml(env, "isId")
            self.conf['seller_addr_id'] = self.config.read_yaml(env, "seller_addr_id")
        elif env in ["pro_oc"]:
            self.conf["ssh_host"] = self.config.read_yaml(env, "ssh_host")
            self.conf['ssh_port'] = self.config.read_yaml(env, "ssh_port")
            self.conf['ssh_user'] = self.config.read_yaml(env, "ssh_user")
            self.conf['ssh_password'] = self.config.read_yaml(env, "ssh_password")
        else:
            self.conf["sys_user"], self.conf['url'], self.conf['collection_type'], self.conf['drop_id'], self.conf[
                'is_id'], self.conf['seller_addr_id'], self.conf['validation'] = "", "", "", "", "", "", ""
        self.conf['db_host'] = self.config.read_yaml(env, "host")
        self.conf['db_port'] = self.config.read_yaml(env, "port")
        self.conf['user_name'] = self.config.read_yaml(env, "user")
        self.conf['user_pwd'] = self.config.read_yaml(env, "password")
        self.conf['db'] = self.config.read_yaml(env, "database")
        return self.conf

    def get_json_value(self, country):
        """
        获取order-flow相关的
        :param country:国家
        :return:
        """
        self.conf['ship_order'] = self.config.read_yaml("ship_order")
        self.conf['get_letter_dg'] = self.config.read_yaml("get_letter_dg")
        self.conf['get_letter_not_dg'] = self.config.read_yaml("get_letter_not_dg")
        self.conf['get_label_dg'] = self.config.read_yaml("get_label_dg")
        self.conf['get_label_not_dg'] = self.config.read_yaml("get_label_not_dg")
        self.conf['bu_bag'] = self.config.read_yaml("bu_bag")
        self.conf['get_last_mile_bag'] = self.config.read_yaml("get_last_mile_bag")
        self.conf['bag_weight'] = self.config.read_yaml("bag_weight")
        self.conf['out_package'] = self.config.read_yaml("out_package")
        self.conf['consignee_state'] = self.config.read_yaml("consignee", [country, "consigneeState"])
        self.conf['consignee_city'] = self.config.read_yaml("consignee", [country, "consigneeCity"])
        self.conf['consignee_zip_code'] = self.config.read_yaml("consignee", [country, "consigneeZipCode"])
        self.conf['address'] = self.config.read_yaml("consignee", [country, "address"])
        self.conf['address2'] = self.config.read_yaml("consignee", [country, "address2"])
        return self.conf

    def get_urls(self, env, sortation):
        self.conf['validation_url'] = self.config.read_yaml(sortation + "_" + env, "validation_url")
        self.conf['ship_order'] = self.config.read_yaml(sortation + "_" + env, "ship_order")
        self.conf['sortation_code'] = self.config.read_yaml(sortation + "_" + env, "sort_code")
        self.conf['drop_site_id'] = self.config.read_yaml(sortation + "_" + env, "drop_site_id")
        self.conf['drop_site_id'] = self.config.read_yaml(sortation + "_" + env, "drop_site_id")
        self.conf['get_letter'] = self.config.read_yaml(sortation + "_" + env, "get_letter")
        self.conf['get_label'] = self.config.read_yaml(sortation + "_" + env, "get_label")
        self.conf['bu_bag'] = self.config.read_yaml(sortation + "_" + env, "bu_bag")
        self.conf['get_last_mile_bag'] = self.config.read_yaml(sortation + "_" + env, "get_last_mile_bag")
        self.conf['bag_weight'] = self.config.read_yaml(sortation + "_" + env, "bag_weight")
        self.conf['out_package'] = self.config.read_yaml(sortation + "_" + env, "out_package")

        return self.conf

#
# if __name__ == '__main__':
#     demo = Config("url")
#     print(demo.get_urls("test", "dg"))
