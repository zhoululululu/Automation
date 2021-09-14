# -*- coding: utf-8 -*- 
"""
Created on 2021/9/8 16:18 
@File  : provide_api.py
@author: zhoul
@Desc  :
"""
import os
from flask import Flask, request, Response
from case.generate_tracking_number import GenerateTrackingNumber

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]

app = Flask(__name__)  # 创建一个服务，赋值给APP


@app.route('/getTrackingNumber', methods=['POST'])
def download():
    env = request.json.get("env")  # 获取接口请求中form-data的url参数传入的值
    product = request.json.get("product")  # 获取接口请求中form-data的url参数传入的值
    num = request.json.get("num")  # 获取接口请求中form-data的url参数传入的值
    tracking_number = GenerateTrackingNumber().generate_tracking_num(env, product, num=int(num))
    data = {"tracking_number_list": tracking_number}
    return data


app.run(host='0.0.0.0', port=8899, debug=True)
