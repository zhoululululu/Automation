# -*- coding: utf-8 -*- 
"""
Created on 2021/7/2 11:26 
@File  : test_interface.py
@author: zhoul
@Desc  :
"""

import os
from commonfunc.file_manage import FileManage
from commonfunc.datetime_tool import DateTimeTool
import pytest
import allure
from api.request_client import RequestClient
from commonfunc.assert_tool import AssertTool
from commonfunc.handle_test_case import HandleTestCase
import pandas

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class TestInterface(object):
    global file_name, all_data, test_case
    # file_name = rootPath + "\\data\\" + "as\\ascendia-case.xlsx"
    file_name = rootPath + "\\data\\" + "cne\\cne-case.xlsx"
    all_data = FileManage.file_to_dict(file_name)
    test_case = all_data.get("case_manage").fillna("").values

    def setup_class(self):
        """
        :return:
        """
        exp_data = {}
        url_data = all_data.get("url_manage").fillna("")

        self.handle = HandleTestCase()
        for idx, item in url_data.iterrows():
            exp_data[item["status"]] = [str(item["env"]), str(item["url"])]
        data = [exp_data.get(k) for k in exp_data if k == 1]
        for i in range(len(data)):
            self.env = data[i][0]
            self.url = data[i][1]
        self.req = RequestClient(self.url)
        self.des_list, self.data_list, self.result_list = [], [], []

    @pytest.mark.parametrize(
        "test_case_id, model, description, path, port, method, header, params_type,data, json_value,params, file_key, request_file_name, collection_return_data, collect_file, ignore_data, check_data, check_type, exp_data, work_status",
        test_case)  # 参数初始化
    @allure.story("confirmShipment")  # story描述
    @allure.suite("{model}")  # suite描述
    @allure.title("No.{test_case_id}-{description}")  # title描述
    @pytest.mark.flaky(returns=0)  # 标记失败后重新运行次数
    @pytest.mark.confirmShipment
    def test_api(self, test_case_id, model, description, path, port, method, header, params_type, data, json_value,
                 params,
                 file_key, request_file_name, collection_return_data, collect_file, ignore_data, check_data, check_type,
                 exp_data, work_status):
        if work_status:
            [path, port, headers] = self.handle.get_relation_value(all_data, [path, port, header],
                                                                   ["path", "port", "header"])
            result = self.req.get_request(path, port, method, headers=headers,
                                          params=self.handle.get_deal_params(self.env, params),
                                          json_value=self.handle.get_deal_params(self.env, json_value),
                                          data=self.handle.get_deal_params(self.env, data),
                                          file_key=file_key, file_value=request_file_name)
            self.des_list.append(description)
            self.data_list.append(self.handle.get_deal_params(self.env, json_value))
            self.result_list.append(result)
            if '"code":0' in result:
                self.handle.update_tracking_num(
                    self.handle.get_deal_params(self.env, json_value)["data"]["packageInfoList"][0][
                        "trackingNumber"])
            AssertTool().compare_dict(result, exp_data, ignore_data, check_data)
            if collection_return_data != "":
                pass

    def teardown_class(self):
        """
        数据导出
        :return:
        """
        data_result = pandas.DataFrame(
            {"description": self.des_list, "data": self.data_list, "result": self.result_list})
        data_result.to_excel(
            rootPath + "\\testresults\\resultfile\\" + str(
                DateTimeTool.get_now_time_stamp_with_millisecond()) + "result.xls")
        # pass