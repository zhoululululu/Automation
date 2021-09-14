# -*- coding: utf-8 -*-
# @Time    : 2021/4/30 16:21
# @Author  : Zhou
# @File    : setdiff.py
# @Software: PyCharm
import json


def setdiff():
    post_code_pre = sorted(
        set(["010", "011", "012", "013", "014"]))
    post_code = []
    for i in range(0, 1000):
        if i < 10:
            post_code.append('00' + str(i))
        elif i < 100:
            post_code.append('0' + str(i))
        else:
            post_code.append('' + str(i))
    print(sorted(list(set(post_code) - set(post_code_pre))))


def get_diff2(list1, list2):
    print(sorted(list(set(list1) - set(list2))))

def get_test1():
    print('{:.2%}'.format(31 / 33))
get_test1()
