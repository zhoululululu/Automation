# -*- coding: utf-8 -*-
"""
Created on 2021/5/19 22:46
@File  : jduge.py
@author: zhoul
@Desc  :
"""
from Common.Read_Case import Read_Info
from Common.Faker import *
import numpy as np
import pandas as pd
from Common.Encryption import Md5encode, DesEncode, Hash1Encode
import os
import re
import json
"""
封装数据用例读取判断类
eg:判断运行状态、判断局部、全局变量并完成变量替换
    判断是否是文件上传
"""

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


# 封装用于递归request_data元素的方法
def get_json_value_by_key(in_json, results=[]):
    if isinstance(in_json, dict):
        # 如果输入数据的格式为dict
        results = []
        for key in in_json.keys():  # 循环获取key
            data = in_json[key]
            get_json_value_by_key(data)  # 回归当前key对于的value

    elif isinstance(in_json, list) or isinstance(in_json, tuple):  # 如果输入数据格式为list或者tuple
        for data in in_json:  # 循环当前列表
            get_json_value_by_key(data)  # 回归列表的当前的元素
    else:
        results.append(in_json)

    return results


def get_targe_value_replace(request_body, coor):
    # 循环字典，获取键、值
    for key, values in request_body.items():
        # 判断值的type类型，如果是list,调用get_list() 函数，
        if isinstance(values, (list, tuple)):
            get_list_tuple(values, coor)
        # 如果是字典，调用自身
        elif isinstance(values, dict):
            get_targe_value_replace(values, coor)
        # 如果值不是list且是需要被替换的，就替换掉
        elif isinstance(values, str) and re.search(r'^\$', values):
            try:
                if coor[values] == None:
                    pass
                else:
                    request_body[key] = coor[values]
            except:
                LOG.info("Not found {} in correlation! correlation is {}".format(values, coor))
        else:
            pass
    return request_body


def get_list_tuple(values, coor):
    if values:
        for key in values:
            if isinstance(key, (list, tuple)):
                get_list_tuple(values, coor)
            else:
                get_targe_value_replace(key, coor)
    else:
        pass


class Judge:

    def __init__(self, File_name, Sheet_Name):
        self._Base_Path = PATH(File_name)
        self._Case_Data = Read_Info(self._Base_Path).Read_Excel(Sheet_Name)
        self.Run_Data = None
        self.Response = None
        self.Correlation = None
        # 创建用于储存关联变量的字典，并初始化session、token值
        self.CorrelationDict = {"${session}": None, "${token}": None}
        self.num = None
        self.api_purpose = None

    # 对不运行的用例进行过滤
    def Judge_Active(self):
        # 找出含有No值所在行索引列表
        index_ = self._Case_Data[(self._Case_Data.Active == 'No')].index.to_list()
        # 删除No的用例
        self.Run_Data = self._Case_Data.drop(index_, inplace=False)
        return self.Run_Data

    # 对request_data变量进行查找，并完成全局替换操作
    def Judge_Variable(self, ):
        # 遍历请求体的值
        import re
        for index, row in self.Run_Data.iterrows():
            new_data = row['Request_Data']
            # 查找用例中所有变量，并对变量是否存在进行判断
            variable = re.findall(r'\${.{0,30}[^"}]}', new_data)
            # 对变量是否为空进行判断
            if variable is not []:
                for var in variable:
                    # 当变量不在系统内置变量中时，直接跳过
                    if var not in Variables.keys():
                        # LOG.info('No.{} [{}] Not found {} in Variables! Variables is [{}]'.format(num,api_purpose,var,Variables))
                        pass
                    else:
                        # 获取变量实际值
                        old_var = eval(Variables[var])
                        # 对原有数值进行替换操作
                        new_data = new_data.replace(var, old_var)
                # dataframe值替换操作
                self.Run_Data.loc[index, 'Request_Data'] = new_data
        return self.Run_Data

    # 对文件路径中的反斜杠转化以及是否存在进行判断
    def Judge_File(self, num, api_purpose, Request_Data):
        # Request_Data必须是字典
        if 'file' in Request_Data.keys():
            file_path = Request_Data['file']['file_path']
            # file_path = file_path.replace('\\','/')
            # 判断文件路径是否存在
            if not os.path.exists(file_path):
                LOG.warning("No.[{}] Api_Purpose [{}] path:{} not found!".format(num, api_purpose, file_path))
        else:
            pass

    # 对用例加密格式进行判断，并数据进行加密
    def Judge_Encryption(self, Encryption, Encryption_Key, request_data):

        if Encryption == 'No':
            return request_data
        elif Encryption == 'MD5':
            # 对文件读取的Encryption_Key字段进行处理，1.中文分隔符转换为英文 2.过滤字符串中的空格键  3.以英文逗号分隔为列表
            keys = Encryption_Key.replace('，', ',').replace(" ", "").split(',')
            for key in keys:
                # 读取request_data中的指定值
                value = request_data[key]
                # 进行Md5编码
                md5_value = Md5encode(value)
                # 完成替换操作
                request_data[key] = md5_value
            return request_data
        elif Encryption == 'DES':
            # 对文件读取的Encryption_Key字段进行处理，1.中文分隔符转换为英文 2.过滤字符串中的空格键  3.以英文逗号分隔为列表
            keys = Encryption_Key.replace('，', ',').replace(" ", "").split(',')
            for key in keys:
                # 读取request_data中的指定值
                value = request_data[key]
                # 进行Md5编码
                des_value = DesEncode(value)
                # 完成替换操作
                request_data[key] = des_value
            return request_data

    # 在运行用例前对Correlation中前置token，session等参数进行判断取值
    def Extract_Correlation_Before(self, num, api_purpose, Correlation):
        # 赋值操作
        self.num = num
        self.api_purpose = api_purpose
        correlation_list = self.Judeg_Correlation(Correlation)
        # 对返回列表进行非空判断
        if correlation_list is not None:
            Correlation_ = Correlation
            # 对传入correlations进行遍历
            for i in range(len(correlation_list)):
                # 以等号切割
                param = correlation_list[i].split('=')
                # 以][切割
                keys = param[1][1:-1].split('][')
                if len(keys) == 1 and len(keys[0]) >= 22:
                    self.CorrelationDict[param[0]] = keys[0]
                    # 删除读取correlation中的值  #删除correlation中的第一个;
                    Correlation_ = Correlation.replace("{}=[{}]".format(param[0], keys[0]), '').replace(';', '', 1)
                if Correlation_ not in (None, np.nan, ''):
                    return Correlation_
                else:
                    return None
        else:
            return None

    # 在运行用例后对关联参数进行获取
    def Extract_Correlation_After(self, Correlation_1):
        # 调用Judge_Correlation对correlation的值进行判断
        correlation_list2 = self.Judeg_Correlation(Correlation_1)
        # 对返回列表进行非空判断
        if correlation_list2 is not None:
            try:
                for i in range(len(correlation_list2)):
                    # 以等号切割
                    param = correlation_list2[i].split('=')
                    # 以][切割
                    keys = param[1][1:-1].split('][')
                    value = self.Response
                    if value is None:
                        LOG.error('接口返回[Response]结果异常:{}'.format(value))
                        break
                    for key in keys:
                        try:
                            temp = value[int(key)]
                        except:
                            try:
                                temp = value[key]
                            except:
                                LOG.warning("{} not found in Response：{}！".format(key, value))
                                break
                        value = temp
                    self.CorrelationDict[param[0]] = value
                LOG.info("After replacement CorrelationDict is {}".format(self.CorrelationDict))
            except:
                LOG.warning("Interface return variable extraction failed")
        else:
            pass

    # 对Correlation中的值写入是否合法进行校验，并返回列表或者None
    def Judeg_Correlation(self, Correlation):
        # 非空判断
        if Correlation not in (None, ''):
            # 去除换行、回车符，并分割
            correlation_list = Correlation.replace('\r', '').split('\n')
            for j in range(len(correlation_list)):
                param = correlation_list[j].split('=')
                if len(param) == 2:
                    if param[1] == '' or not re.search(r'^\[', param[1]) or not re.search(r'\]$', param[1]):
                        LOG.warning(
                            "No.[{}] Api_Purpose[{}] Associated parameters format error, Please check [correlation] config!".format(
                                self.num, self.api_purpose))
            return correlation_list
        else:
            return None

    # def Replace_Correlation(self,request_data):
    #     #遍历请求体，对剩余存在以$开头的数值进行替换
    #     request_data_ = request_data.copy()
    #     for key in request_data_.keys():
    #         if key == 'file':
    #             pass
    #         else:
    #             for i in range(len(request_data_[key])):
    #                 value = request_data_[key][i]
    #                 if re.search(r'^\$',value):
    #                     try:
    #                         request_data_[key][i] = self.CorrelationDict[value]
    #                     except:
    #                         LOG.info("Not found {} in correlation! correlation is {}".format(value,self.CorrelationDict))
    #     return request_data_
    #
    # def Replace_Correlation(self,request_data):
    #     #遍历请求体，对剩余存在以$开头的数值进行替换
    #     request_data_ = request_data.copy()
    #     #递归请求请求体元素
    #     elements_type = {}
    #     elements = get_json_value_by_key(request_data_)
    #     for element in elements:
    #         if isinstance(element,str):
    #             if re.search(r'^\$',element):
    #                 try:
    #                     #对目标值是否是字符串进行判断
    #                     if isinstance(self.CorrelationDict[element],str):
    #                         request_data_ = str(request_data).replace(element,self.CorrelationDict[element])
    #                     else:
    #                         #对目标值进行转化替换
    #                         request_data_ = str(request_data).replace(element,str(self.CorrelationDict[element]))
    #                         #将目标值及数据类型存入字典，方便再次对数据类型做转换
    #                         elements_type[self.CorrelationDict[element]] = type(self.CorrelationDict[element])
    #                 except:
    #                     LOG.info("Not found {} in correlation! correlation is {}".format(element,self.CorrelationDict))
    #         else:
    #             continue
    #
    #     return request_data_,elements_type

    def Replace_Correlation(self, request_data):
        # 遍历请求体，对剩余存在以$开头的数值进行替换
        request_data_ = request_data.copy()
        request_body = get_targe_value_replace(request_data_, self.CorrelationDict)
        return request_body

        # for element in elements:
        #     if isinstance(element,str):
        #         if re.search(r'^\$',element):
        #             try:
        #                 #对目标值是否是字符串进行判断
        #                 if isinstance(self.CorrelationDict[element],str):
        #                     request_data_ = str(request_data).replace(element,self.CorrelationDict[element])
        #                 else:
        #                     #对目标值进行转化替换
        #                     request_data_ = str(request_data).replace(element,str(self.CorrelationDict[element]))
        #                     #将目标值及数据类型存入字典，方便再次对数据类型做转换
        #                     elements_type[self.CorrelationDict[element]] = type(self.CorrelationDict[element])
        #             except:
        #                 LOG.info("Not found {} in correlation! correlation is {}".format(element,self.CorrelationDict))
        #     else:
        #         continue
        #
        # return request_data_,elements_type
