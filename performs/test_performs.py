# -*- coding: UTF-8 -*-
'''
Created on 2020/3/2
@File  : test_performs.py
@author: ZL
@Desc  :
'''

from locust import HttpLocust, TaskSet, task
import json


class UserBehavior(TaskSet):
    # """意图识别"""
    # @task(1)
    # def get_intent(self):
    #     sentence = "你们医院怎么样"
    #     self.client.get("/andrology_intent/v2?sentence={}".format(sentence))

    """相似度识别"""

    # @task(2)
    # def get_similary(self):
    #     sentence1 = "龟头刺痒"
    #     sentence2 = "龟头瘙痒"
    #     with self.client.get("/symptom_similarity/v1?symptom1={}&symptom2={}".format(sentence1, sentence2),
    #                          catch_response=True) as response:
    #         if response.status_code == 200:
    #             response.success()
    #         else:
    #             response.failure('Failed!')

    """项目识别"""
    # @task(3)
    # def get_similary(self):
    #     sentence1 = "龟头刺痒"
    #     sentence2 = "龟头瘙痒"
    #     self.client.get("/symptom_similarity/v1?symptom1={}&symptom2={}".format(sentence1, sentence2))

    # """NER实体识别"""
    # @task(4)
    # def get_similary(self):
    #     sentence1 = "龟头刺痒"
    #     sentence2 = "龟头瘙痒"
    #     self.client.get("/symptom_similarity/v1?symptom1={}&symptom2={}".format(sentence1, sentence2))
    #
    #
    # """NER实体识别"""
    # @task(4)
    # def get_similary(self):
    #     sentence1 = "我有点担心会恶化怎么办"
    #     self.client.get("/emotion_question_analyse/v1?client_utterance={}".format(sentence1))

    """es测试"""

    # @task(4)
    # def get_es_test(self):
    #     params = {
    #         "str1": ["多少钱啊"],
    #         "str2": ["这个多少钱"]
    #     }
    #     self.client.post(url="/without_bert_similarity/v2/sim", params=params)

    def test_and_re(self):
        params = {
            "sentence": "上学那会，以为黄色影像的影响，有手淫的习惯",
            "entity": {"cause": ["手淫"]}
        }
        response = self.client.get("/intention/v1", data=json.loads(params)).json()
        print(response)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 200
    max_wait = 500


if __name__ == "__main__":
    import os

    os.system("locust -f test_performs.py --host=http://10.0.210.249:8236")
