# -*- coding: utf-8 -*-
"""
Created on 2021/5/19 22:44
@File  : email_tool.py
@author: zhoul
@Desc  :
"""

import yagmail, os
from commonfunc.log import Log

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def send_email(setting):
    """
    入参一个字典
    :param user: 发件人邮箱
    :param password: 邮箱授权码
    :param host: 发件人使用的邮箱服务 例如：smtp.163.com
    :param contents: 内容
    :param addressees: 收件人列表
    :param title: 邮件标题
    :param enclosures: 附件列表
    :return:
    """
    yag = yagmail.SMTP(setting['user'], setting['password'], setting['host'])
    # path = PATH(setting['enclosures'][0])

    # 发送邮件
    yag.send(setting['addressees'], setting['title'], setting['contents'], setting['enclosures'])
    # 关闭服务
    yag.close()
    LOG.info('Email sent successfully！')
