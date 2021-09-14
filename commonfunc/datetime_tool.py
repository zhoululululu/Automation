# -*- coding: utf-8 -*-
"""
Created on 2021/5/19 22:59
@File  : datetime_tool.py
@author: zhoul
@Desc  :
"""
import time
import datetime
import calendar
from datetime import date, timedelta


class DateTimeTool:
    @classmethod
    def get_now_time(cls, time_format='%Y-%m-%d %H:%M:%S'):
        """
        获取现在时间
        :param time_format:时间格式
        :return:获取特定时间格式的时间；默认格式为%Y-%m-%d %H:%M:%S，例如：2021-05-19 23:10:04
        """
        return datetime.datetime.now().strftime(time_format)

    @classmethod
    def get_order_time(cls, time_format='%Y-%m-%dT%H:%M:%S+0800'):
        """
        获取现在时间
        :param time_format:时间格式
        :return:获取特定时间格式的时间；默认格式为%Y-%m-%d %H:%M:%S，例如：2021-06-28T11:55:31+0800
        """
        return datetime.datetime.now().strftime(time_format)

    @classmethod
    def get_after_day_time(cls, time_format='%Y-%m-%d %H:%M:%S'):
        """
        获取明天的时间
        :param time_format:时间格式
        :return:获取特定时间格式的时间；默认格式为%Y-%m-%d %H:%M:%S，例如：2021-05-19 23:10:04
        """
        return (datetime.datetime.now() + timedelta(days=1)).strftime(time_format)

    @classmethod
    def get_now_date(cls, time_format='%Y-%m-%d'):
        """
        获取当前日期
        :param time_format:日期格式
        :return:获取特定日期格式的日期；默认格式为%Y-%m-%d，例如：2021-05-19
        """
        return datetime.date.today().strftime(time_format)

    @classmethod
    def get_now_time_stamp_with_second(cls):
        """
        获取10位时间戳
        :return: 时间戳，例如：1621436934
        """
        return int(time.time())

    @classmethod
    def get_now_time_stamp_with_millisecond(cls):
        """
        获取13位时间戳
        :return: 时间戳，例如：1621436985147
        """
        return int(round(time.time() * 1000))

    @classmethod
    def get_week_day(cls):
        """
        获得今天星期几，从1开始，1-7
        :return: 今日的星期数，例如：3
        """
        return datetime.datetime.now().weekday() + 1

    @classmethod
    def get_how_days_after(cls, how_days_ago=0, now_date_time_format='%Y-%m-%d %H:%M:%S'):
        """

        :param now_date_time:
        :param now_date_time_format:
        :param how_days_ago:
        :return:
        """
        now_date_time = datetime.datetime.strptime(cls.get_now_time(), now_date_time_format)
        result_date_time = now_date_time + datetime.timedelta(days=how_days_ago)
        return result_date_time

    @classmethod
    def date_time_to_str(cls, the_date_time, time_format='%Y-%m-%d'):
        """

        :param the_date_time:
        :param time_format:
        :return:
        """
        return the_date_time.strftime(time_format)

    @classmethod
    def str_to_date_time(cls, str, str_format):
        """

        :param str:
        :param str_format:
        :return:
        """
        dst_date_time = datetime.datetime.strptime(str, str_format)
        return dst_date_time

    @classmethod
    def get_how_years_ago(cls, now_date, how_years_ago=0, now_date_format='%Y-%m-%d'):
        """

        :param now_date:
        :param how_years_ago:
        :param now_date_format:
        :return:
        """
        result_date = cls.get_how_days_ago(now_date, now_date_format, how_years_ago * 366)
        return result_date

    @classmethod
    def get_current_month_first_day_or_last_day(cls, type=1):
        """获取当前月第一天或者最后一天日期
        Args:
            type (int, optional): 第一天:1，最后一天:-1
        Returns:
            [type]: [description]
        """
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        last_day = calendar.monthrange(year, month)[1]
        if type == 1:
            start = datetime.date(year, month, 1)
            return start
        if type == -1:
            end = datetime.date(year, month, last_day)
            return end


if __name__ == '__main__':
    print(DateTimeTool.get_how_days_after(1))
