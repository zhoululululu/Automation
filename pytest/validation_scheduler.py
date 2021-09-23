# -*- coding: utf-8 -*- 
"""
Created on 2021/9/22 15:23 
@File  : validation_scheduler.py
@author: zhoul
@Desc  :
"""
from apscheduler.schedulers.blocking import BlockingScheduler
import pytest
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


def job_func():
    pytest.main(['-s', '-q', '--alluredir', rootPath + '/testresults/pytestresult/data', "-m=validation"])


scheduler = BlockingScheduler()
# 每天触发
# 在 2021-09-22 15:40:00 ~ 2022-09-22 15:40:00' 之间, 每天执行一次 job_func 方法 #days
scheduler.add_job(job_func, 'interval', days=1, start_date='2021-09-23 09:00:00', end_date='2022-09-22 09:00:00')

scheduler.start()
