# -*- coding: utf-8 -*-
"""
Created on 2021/5/20 9:10
@File  : request_client.py
@author: zhoul
@Desc  :
"""
import os
from commonfunc.get_logging import Logging
from requests_toolbelt import MultipartEncoder
import requests
import mimetypes
import json


class RequestClient:

    def __init__(self, url):
        self.url = url
        self.session = requests.session()

    @staticmethod
    def update_header(data, file_key, file_value):
        data = {} if data is None else data
        data[file_key] = (
            os.path.basename(file_value), open(file_value, 'rb'), mimetypes.guess_type(file_value.split("/")[-1])[0])
        m = MultipartEncoder(
            fields=data,
        )
        return m.content_type, m

    def get_request(self, path, port, method, headers=None, data=None, json_value=None, params=None,
                    file_key=None, file_value=None, **kwargs):
        """
        :param path:
        :param port:
        :param method:
        :param headers:
        :param data:
        :param json_value:
        :param params:
        :param file_key:
        :param file_value:
        :return:
        """

        headers = json.loads(headers) if type(headers) != dict else headers
        if file_value != "":
            headers["Content-Type"], data = self.update_header(data, file_key, file_value)
        r = self.session.request(url=self.url + path if str(port) == "" else self.url + ":" + str(port) + path,
                                 method=method,
                                 headers=headers,
                                 params=params if params != "" else None,
                                 data=data if data != "" else None,
                                 json=json_value if json_value != "" else None,
                                 timeout=9999, **kwargs)
        return self._deal_response_result(r).body

    def get_simple_request(self, method, json_value=None, headers=None, **kwargs):
        """
        :param method:
        :param headers:
        :param json_value:
        :return:
        """
        headers = json.loads(headers)
        r = self.session.request(url=self.url, method=method, json=json_value, headers=headers, **kwargs)
        return self._deal_response_result(r).body

    @staticmethod
    def _deal_response_result(r, _encoding="UTF-8"):
        """
        将请求结果封装到HttpResponseResult
        :param r: requests请求响应
        :return:
        """
        http_response_result = HttpResponseResult()
        http_response_result.status_code = r.status_code
        http_response_result.headers = r.headers
        http_response_result.cookies = r.cookies
        http_response_result.body = json.loads(r.content)
        return http_response_result


class HttpResponseResult(object):
    def __init__(self):
        self.status_code = None
        self.body = None
        self.cookies = None
        self.headers = None
