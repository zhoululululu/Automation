# -*- coding: utf-8 -*- 
"""
Created on 2021/7/2 13:57 
@File  : assert_tool.py
@author: zhoul
@Desc  :
"""
import re
import filecmp
import os
import jsonpath
import json


class AssertTool(object):
    @classmethod
    def is_regular_match(cls, source_str, regular_str):
        """
        判断字符串是否符合正则表达式，正则表达式的内容包含正则关键字需用\进行转移
        :param source_str:
        :param regular_str:
        :return:
        """
        if re.match(regular_str, source_str):
            return True
        else:
            return False

    @classmethod
    def is_files_equal(cls, file_path1, file_path2):
        """
        比较两个文件内容是否一样
        :param file_path1:
        :param file_path2:
        :return:
        """
        if filecmp.cmp(file_path1, file_path2):
            return True
        else:
            return False

    @classmethod
    def is_fles_size_equal(cls, file_path1, file_path2):
        """
        比较两个文件大小是否一致
        :param file_path2:
        :param file_path1:
        :return:
        """
        size1 = os.path.getsize(file_path1)
        size2 = os.path.getsize(file_path2)
        if size1 == size2:
            return True
        else:
            return False

    @classmethod
    def compare_dict(cls, act_value, exp_value, ignore=None, retain=None):
        """
        校验结果
        :param act_value: 实际的接口返回结果
        :param exp_value: 预期的接口返回结果
        :param ignore: 需要忽略的json key值（注意哦，这一单忽略，就遍历只要碰见这个key值就忽略）
        :param retain: 需要校验的值
        :return:
        """
        print(act_value)
        try:
            if retain != "":
                value = []
                if retain == ".":
                    pass
                else:
                    for i in (eval(retain)):
                        print(jsonpath.jsonpath(act_value, i))
                        value.append(jsonpath.jsonpath(act_value, i))
                    act_value = value
                    exp_value = eval(exp_value)
            else:
                act_value = json.loads(act_value)
                exp_value = json.loads(exp_value)
                for key in eval(ignore):
                    if act_value.__contains__(key):
                        act_value.__delitem__(key)
                        exp_value.__delitem__(key)
            print('act_value: ', act_value)
            print('exp_value: ', exp_value)
            if act_value == exp_value:
                assert True
            else:
                assert False
        except Exception as e:
            assert False, "校验出错"


# if __name__ == '__main__':
#     AssertTool.compare_dict({"sysErro": False, "validationResults": [
#         {"freightDTO": {"currency": "CNY", "freight": 15.0100}, "result": True, "serviceId": "EE", "sysErro": False},
#         {"freightDTO": {"currency": "CNY", "freight": 10.9300}, "result": True, "serviceId": "ES", "sysErro": False},
#         {"erroMessageCn": "超出物流服务范围 – 请核查订单信息匹配以下受限范围：尺寸限制/重量限制/申报金额限制/派送区域",
#          "erroMessageEn": "Out of logistic service scope, please double check your order if comply with the service standards: Dimension Limit, Weight Limit, Cargo Value Limit, and Delivery Area coverage.",
#          "result": False, "serviceId": "EX", "sysErro": False},
#         {"erroMessageCn": "超出物流服务范围 – 请核查订单信息匹配以下受限范围：尺寸限制/重量限制/申报金额限制/派送区域",
#          "erroMessageEn": "Out of logistic service scope, please double check your order if comply with the service standards: Dimension Limit, Weight Limit, Cargo Value Limit, and Delivery Area coverage.",
#          "result": False, "serviceId": "EM", "sysErro": False}]},"[[True, True], ['EE'], ['ES']]", retain='["$.validationResults[0:2:1].result","$.validationResults[0].serviceId","$.validationResults[1].serviceId"]'
#                             )
