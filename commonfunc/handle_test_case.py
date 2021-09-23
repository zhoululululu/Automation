# -*- coding: utf-8 -*- 
"""
Created on 2021/7/2 13:43 
@File  : handle_test_case.py
@author: zhoul
@Desc  :
"""
import jsonpath
from commonfunc.json_path_finder import JsonPathFinder, get_paths
from commonfunc.get_faker import CreatData
from commonfunc.get_logging import Logging
from commonfunc.datetime_tool import DateTimeTool
from commonfunc.yaml_manage import YamlManage
import os
import pandas

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]

logging = Logging()


class HandleTestCase(object):
    def __init__(self):
        self.result_as = []
        self.get_all_tracking_num()

    def handle_special(self, env, key, data=None):
        """
        通过key值，选择不同的处理方式
        :param env:
        :param key:
        :param data:
        :return:
        """
        func_key = key.split("$")[1].split("+")[0]
        func_value = key.split("$")[1].split("+")[1]
        if func_key == "uuid":
            return CreatData.get_uuid(data)
        if func_key.split("+")[0] == "varchar":
            return CreatData.get_varchar(int(func_value))
        if func_key.split("+")[0] == "chinese":
            return CreatData.get_chinese(int(func_value))
        if func_key.split("+")[0] == "num":
            return CreatData.get_num(int(func_value))
        if func_key in ["punctuation"]:
            return CreatData.get_punctuation(data)
        if func_key == "country":
            return CreatData.get_currency(env, func_value, data)
        if func_key == "trackingNumber":
            # return CreatData.get_tracking_number(env, func_value, data)
            return self.get_tracking_num()
        if func_key == "timeStamp":
            if func_value == "13":
                return DateTimeTool.get_now_time_stamp_with_millisecond()
            elif func_value == "10":
                return DateTimeTool.get_now_time_stamp_with_second()
        if func_key == "orderData":
            return DateTimeTool.get_order_time()
        else:
            return data

    def get_relation_value(self, data, key_list: list, point_list: list):
        result_list, exp_data, sheet_data = [], "", {}
        for sheet in data:
            if sheet != "case_manage":
                sheet_data[sheet] = data.get(sheet).fillna("").to_dict(orient="list")
        logging.info("读取api_manage外的所有sheet内容为： %s" % sheet_data)
        for i in range(len(key_list)):
            sheet_name, field = key_list[i][1:].split(".")
            try:
                exp_data = sheet_data.get(sheet_name).get(point_list[i])[
                    sheet_data.get(sheet_name).get("key").index(field)]
            except Exception as e:
                exp_data.append("")
                self.logging.error("")
            result_list.append(exp_data)
        return result_list

    # @classmethod
    # def get_deal_params(cls, env, origin_params):
    #     if origin_params != "" and "$" in origin_params:
    #         params_list = eval(origin_params)
    #         paths = get_paths(eval(origin_params))
    #         for path in paths:
    #             result = eval(origin_params)
    #             for p in path:
    #                 result = result[p]
    #                 if p == path[-1] and type(result) not in [int, float]:
    #                     if "$" in result:
    #                         params_list = HandleTestCase.handle_special(env, result, params_list)
    #
    #
    #         logging.info("params处理成功：%s -> %s" % (str(origin_params), params_list))
    #     else:
    #         params_list = origin_params
    #
    #     return params_list
    def get_deal_params(self, env, origin_params):
        if origin_params != "":
            params_list = eval(origin_params)  # 先将str转json
            if "$" in origin_params:  # 如果发现在原先传入的body中含有$
                paths = get_paths(eval(origin_params))  # 获取body所有的路径
                for path in paths:
                    result = params_list
                    for p in path:
                        result = result[p]
                        if p == path[-1] and type(result) not in [int, float, list]:
                            if result is not None:
                                if "$" in result and "+" in result:
                                    handle_result = self.handle_special(env, result, params_list)
                                    if "country" in result:
                                        params_list = handle_result
                                    else:
                                        # pre_dict = {p: handle_result}
                                        params_list = self.change_value_test(params_list, p, handle_result)
                logging.info("params处理成功：%s -> %s" % (str(origin_params), params_list))
        else:
            params_list = origin_params
        return params_list

    def change_value_test(self, json_dict, k, v):
        """
        替换json值
        :param json_dict: 需要进行修改的json值
        :param k: 要替换的key
        :param v: 要替换的value
        :return:
        """
        if isinstance(json_dict, list):  # 判断json_dict是否为list
            for j_dict in json_dict:  # 遍历list的值，一一进入
                self.change_value_test(j_dict, k, v)  # 继续递归
        elif isinstance(json_dict, dict):  # 判断json_dict是否为dict
            for key in json_dict:  # 遍历
                if key == k:  # 找到
                    json_dict[key] = v  # 替换
                elif isinstance(json_dict[key], (dict, list)):  # 或满足dict或json，继续递归遍历
                    self.change_value_test(json_dict[key], k, v)
        return json_dict

    # def change_value(self, json_dict, new_dict):
    #     for l, m in new_dict.items():
    #         for k, v in json_dict.items():
    #             if k == l:
    #                 json_dict[k] = new_dict[l]
    #             elif type(v) == dict:
    #                 for j, z in v.items():
    #                     if j == l:
    #                         v[j] = new_dict[l]
    #                     if type(z) == list:
    #                         for m in range(len(z)):
    #                             for a, b in z[m].items():
    #                                 if a == l:
    #                                     z[m][a] = new_dict[l]
    #                                 elif type(b) == list:
    #                                     for n in range(len(b)):
    #                                         for a, o in b[n].items():
    #                                             if a == l:
    #                                                 b[n][a] = new_dict[l]
    #
    #     return json_dict

    def collection_data(self, test_case_id, collection_data, test_data, result):
        """
        收集请求结果参数，写在yaml中，格式为case_id: key, value
        :param test_data:
        :param test_case_id:
        :param collection_data:
        :param result:
        :return:
        """
        ym_writer = YamlManage(rootPath + "\\data\\collection_data.yaml")
        for path in collection_data:
            re = result
            for p in path:
                re = re[p]
                if p == path[-1]:
                    ym_writer.write_yaml(test_case_id, p, re)

    def get_all_tracking_num(self):
        testdata = pandas.read_excel(rootPath + "\\data\\as\\as-order.xlsx", sheet_name="EPAQSCT-IL-EXP")
        tracking_num = testdata.跟踪号码.tolist()
        static = testdata.状态.tolist()
        for i in range(len(static)):
            self.result_as.append({tracking_num[i]: static[i]})
        print(self.result_as)
        return self.result_as

    def get_tracking_num(self):
        # for i in self.result_as:
        #     if "未使用" in i.values():
        #         print(list(i.keys())[list(i.values()).index("未使用")])
        #         return list(i.keys())[list(i.values()).index("未使用")]

        return str(CreatData.get_num(int(13)))

    def update_tracking_num(self, tracking_number):
        # for i in self.result_as:
        #     if tracking_number in i.keys():
        #         i[tracking_number] = "已使用"
        #         break
        pass

    def update_tracking_file(self, tracking_number):
        # for i in self.result_as:
        #     if tracking_number in i.keys():
        #         i[tracking_number] = "已使用"
        #         break
        pass



# if __name__ == '__main__':
#     qqq = HandleTestCase()
#     test = '{"data":{"hoauBagId":"$chinese+20","packageInfoList":[{"trackingNumber":"$trackingNumber+","orderReference":"$num+10","itemInfoList":[{"skuDesc":"$varchar+10","skuDescCn":"$chinese+10"}]}]}}'
#     print(qqq.get_deal_params("test", test))
