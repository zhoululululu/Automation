# -*- coding: utf-8 -*- 
"""
Created on 2021/7/6 16:56 
@File  : json_path_finder.py
@author: zhoul
@Desc  :
"""

import json
import operator
from functools import reduce
import collections
from commonfunc.get_logging import Logging

logger = Logging()


class JsonPathFinder:
    def __init__(self, json_str):
        self.data = json.loads(json_str)

    def iter_node(self, rows, road_step, target):
        if isinstance(rows, dict):
            key_value_iter = (x for x in rows.items())
        elif isinstance(rows, list):
            key_value_iter = (x for x in enumerate(rows))
        else:
            return
        for key, value in key_value_iter:
            current_path = road_step.copy()
            current_path.append(key)
            if key == target:
                yield current_path
            if isinstance(value, (dict, list)):
                yield from self.iter_node(value, current_path, target)

    @classmethod
    def json_path_value(cls, json_dict, path):
        try:
            num = 1
            paths = path.split(".")
            result_dict = {}
            for p in paths:
                if num == 1:
                    result_dict = json_dict[p + ""]
                    num = num + 1
                else:
                    result_dict = result_dict[p + ""]
                    num = num + 1
            return result_dict
        except Exception as e:
            logger.error("get value from path failure and the exception is " + str(e))
            return None

    def find_one(self, key: str) -> list:
        path_iter = self.iter_node(self.data, [], key)
        for path in path_iter:
            return path
        return []

    def find_all(self, key: str) -> list:
        path_iter = self.iter_node(self.data, [], key)
        return list(path_iter)


# copy的
def get_paths(source):
    paths = []
    if isinstance(source, collections.MutableMapping):  # found a dict-like structure...
        for k, v in source.items():  # iterate over it; Python 2.x: source.iteritems()
            paths.append([k])  # add the current child path
            paths += [[k] + x for x in get_paths(v)]  # get sub-paths, extend with the current
    # else, check if a list-like structure, remove if you don't want list paths included
    elif isinstance(source, collections.Sequence) and not isinstance(source, str):
        #                          Python 2.x: use basestring instead of str ^
        for i, v in enumerate(source):
            paths.append([i])
            paths += [[i] + x for x in get_paths(v)]  # get sub-paths, extend with the current
    return paths
