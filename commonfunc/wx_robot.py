# -*- coding: utf-8 -*- 
"""
Created on 2021/9/13 13:53 
@File  : wx_robot.py
@author: zhoul
@Desc  :
"""

from api.request_client import RequestClient
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


class WeChat:

    def __init__(self):
        self.request = RequestClient("https://qyapi.weixin.qq.com")
        self.header = '{"Content-Type": "application/json"}'

        self.path1 = "/cgi-bin/webhook/send?key=474e9964-db83-4cc1-87b3-758be14da3e7"
        self.path2 = "/cgi-bin/webhook/upload_media?key=474e9964-db83-4cc1-87b3-758be14da3e7&type=file"

    @staticmethod
    def message(project, total, passing, succeed, failing, error_list):
        """
        需要发送到企业微信的文案信息
        :param project:         项目名称
        :param total:           总计
        :param passing:         通过率
        :param succeed:         通过数
        :param failing:         失败数
        :param skip:            跳过数
        :param error:           错误数
        :param error_list:     错误例子
        :param file:            测试文件
        :return:                返回data信息
        """

        data = {
            "msgtype": "markdown",  # 消息类型，此时固定为markdown
            "markdown": {
                "content": "# **（定时任务）自动化测试反馈**\n#### **请注意及时跟进！**\n"
                           "> 接口名称：<font color=\"info\">%s</font> \n"
                           "> 测试用例总数：<font color=\"info\">%s条</font>；测试用例通过率：<font color=\"info\">%s</font>\n"
                           "> **--------------------运行详情--------------------**\n"
                           "> **成功数：**<font color=\"info\">%s</font>\n**失败数：**<font color=\"warning\">%s</font>\n"
                           "> **--------------------错误用例--------------------**\n" % (
                               project, total, passing, succeed, failing)}}
        for i in error_list:
            error_record = "> **路向：**<font color=\"warning\">%s</font>\n" % i
            data["markdown"]["content"] += error_record
            print(data["markdown"]["content"])
        data["markdown"]["content"] += "> ##### **具体测试结果详见以下文件**"

        return data

    def send_message(self, project, total, passing, succeed, failing, error_list, file):
        """
        发送文案信息
        :param project:         项目名称
        :param total:           总计
        :param passing:         通过率
        :param succeed:         通过数
        :param failing:         失败数
        :param skip:            跳过数
        :param error:           错误数
        :param file:
        :param error_list:
        :return:
        """
        send_result_data = self.message(project, total, passing, succeed, failing, error_list)
        print(send_result_data)
        upload_file_data = {'file': open(file, 'rb')}
        # 获取企业微信群机器人的url, 使用的python第三方库requests库发送的请求
        # 发送请求报告
        res = self.request.get_request(path=self.path1, port="", method="post", json_value=send_result_data,
                                       headers=self.header,
                                       file_value='')
        # # 上传测试报告文件
        media_id = self.request.get_request(path=self.path2, port="", method="post", json_value="{}",
                                            headers=self.header,
                                            file_value=file, file_key="file")['media_id']
        #
        send_file_data = {"msgtype": "file", "file": {"media_id": media_id}}
        # # 发送测试报告文件
        send_file = self.request.get_request(path=self.path1, port="", method="post", json_value=send_file_data,
                                             headers=self.header,
                                             file_value='')

        return send_file

# if __name__ == '__main__':
#     lulu_robot = WeChat()
#     path = "/cgi-bin/webhook/send?key=474e9964-db83-4cc1-87b3-758be14da3e7"
#     path2 = "/cgi-bin/webhook/upload_media?key=474e9964-db83-4cc1-87b3-758be14da3e7&type=file"
#     file = rootPath + "\\testresults\\resultfile\\validation\\0913_validation_result.xls"
#     lulu_robot.send_message("validation", "33", "{:.2%}""".format(31 / 33), "31", "2", "0", "0", ["US美国路向", "SK斯洛伐克路向"],
#                             file)
