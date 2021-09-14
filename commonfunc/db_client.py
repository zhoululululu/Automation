# -*- coding: utf-8 -*-
"""
Created on 2021/5/20 9:08
@File  : db_client.py
@author: zhoul
@Desc  :
"""
import pymysql
from config.get_config import Config
from sshtunnel import SSHTunnelForwarder


class MysqlClient:

    def __init__(self, env):
        """
        对数据库建立连接
        :param env: 环境
        :param sortation: 分拣中心
        """

        self.config = Config("sql")
        self.c = self.config.get_sql_info(env)
        if env != "pro_oc":
            self.conn = pymysql.connect(
                host=self.c["db_host"],
                user=self.c["user_name"],
                password=self.c["user_pwd"],
                db=self.c["db"],
                port=self.c["db_port"],
            )
        else:
            # 连接ssh
            server = SSHTunnelForwarder(
                (self.c["ssh_host"], self.c["ssh_port"]),  # ssh IP和port
                ssh_password=self.c["ssh_user"],  # ssh 密码
                ssh_username=self.c["ssh_password"],  # ssh账号
                remote_bind_address=('127.0.0.1', 3306),
                local_bind_address=('1.1.1.1', 3306))
            # 启动服务
            server.start()
            self.conn = pymysql.connect(
                host=self.c["db_host"],
                user=self.c["user_name"],
                password=self.c["user_pwd"],
                db=self.c["db"],
                port=self.c["db_port"],
            )
        self.cursor = self.conn.cursor()  # 游标，用来执行数据库

    def change_db(self, db):
        """
        切换数据库
        :param db:
        :return:
        """
        self.conn.select_db(db)

    def execute_sql(self, sql=None):
        """
        执行数据库语句
        :param sql: sql语句
        :return:
        """
        try:
            # 为了避免连接被服务器关闭,检测进行重连
            self.conn.ping(reconnect=True)
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise Exception
        return result

    def execute_many(self, query, values):
        """
        :param query: insert into table(field1,field2) values(%s,%s)
        :param values: [(field1_value1,field2_value2),(field1_value3,field2_value4)]
        :return:
        """
        try:
            # 为了避免连接被服务器关闭,检测进行重连
            self.conn.ping(reconnect=True)
            num = len(values)
            n = 0
            with self.conn.cursor() as cursor:
                while n < num:
                    cursor.executemany(query, values[n:n + 1000])
                    self.conn.commit()
                    n += 1000
        except Exception:
            self.conn.rollback()
            raise Exception

    def close_all(self):
        self.conn.close()
