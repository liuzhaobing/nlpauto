#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import random

import pymongo
import requests
import urllib3

from bson.objectid import ObjectId
from apps.nlp.src.common.smartvoice import SmartVoice
from conf.env import *
from utils.handler import Handlers

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Talk:
    def __init__(self,
                 agent_id="1500",
                 env="default",
                 base_url="https://mmue.region-dev-1.service.iamidata.com",
                 username="three",
                 password="123456"):
        self.headers = None
        self.token = None
        self.agent_id = agent_id
        self.env = env
        self.base_url = base_url
        self.username = username
        self.password = password

    def cov_request(self, method, url, *args, **kwargs):
        if not self.headers:
            self.headers = self.get_login_headers()
        return requests.request(method=method, url=self.base_url + url, headers=self.headers, verify=False,
                                timeout=120, *args, **kwargs)

    def login(self, username, password):
        url1 = "/mmue/api/login"
        response = requests.request(method="POST", url=self.base_url + url1, headers=self.headers, verify=False,
                                    json={"username": username, "pwd": password})
        self.token = response.json()["data"]["token"]
        return self.token

    def get_login_headers(self):
        if not self.token:
            self.login(self.username, self.password)
        headers = {
            "Authorization": self.token,
            "Referer": self.base_url + "/app/client",
            "Accept": "application/json, text/plain, */*",
            "Connection": "keep-alive",
            "Origin": self.base_url
        }
        return headers

    def talk(self, text):
        url1 = "/v1/sv/talk?agent_id={}&env={}&text={}".format(self.agent_id, self.env, text)
        start = Handlers.time_now_10s()
        res = self.cov_request(method="GET", url=url1)

        try:
            res = res.json()
        except:
            res = None

        try:
            dmkit_debuginfo = res["data"]["data"]["hitlog"]["dmkit_debuginfo"]
            traces = dmkit_debuginfo["traces"]
        except:
            traces = None

        if res:
            response = {
                "query": text,
                "source": res["data"]["data"]["source"],  # user_service/ConversationPoetry/GetNextPhrases
                "domain": res["data"]["data"]["hitlog"]["domain"],  # user_service/ConversationPoetry/GetNextPhrases
                "tts": res["data"]["data"]["tts"],
                "edg_cost": Handlers.time_now_10s() - start,
                "inner_cost": res["data"]["data"]["hitlog"]["cost"],
                "traces": traces,
                "traceId": res["data"]["data"]["hitlog"]["traceId"],
                "response": res
            }
        else:
            response = {
                "query": text,
                "source": None,
                "domain": None,
                "tts": None,
                "edg_cost": Handlers.time_now_10s() - start,
                "inner_cost": None,
                "traces": traces,
                "traceId": None,
                "response": res
            }
            try:
                response["tts"] = res["data"]["data"]["tts"]
            except:
                response["tts"] = None

        return response

    def split_string_for_text(self, string):
        """创建意图的payload 先对正则语句进行切割"""
        # TODO 此时      string = "唱一首@sys.entity.singer:Singer的@sys.entity.song:Name"
        string_list = string.split("@")  # 先用@切割成列表
        # TODO 此时 string_list = ['唱一首', 'sys.entity.singer:Singer的', 'sys.entity.song:Name']
        for one in string_list:
            # 遍历列表，如果列表元素中包含中文英文和标点符号，则进一步处理
            if Handlers.is_contain_chinese(one) and Handlers.is_contain_english(one) and Handlers.is_contain_character(
                    one):
                index = string_list.index(one)  # 获取到此元素的索引

                # 将该元素的中文与其他内容分开
                en, ch = "", ""
                for o in one:
                    if Handlers.is_contain_english(o) or Handlers.is_contain_character(o):
                        en += o
                    else:
                        ch += o

                # 根据该元素的第一个字符来确定插入顺序
                if Handlers.is_contain_chinese(one[0]):
                    string_list.insert(index, ch)
                    string_list.insert(index + 1, en)
                else:
                    string_list.insert(index, en)
                    string_list.insert(index + 1, ch)

                string_list.remove(one)
            else:
                pass
        # TODO 此时 string_list = ['唱一首', 'sys.entity.singer:Singer', '的', 'sys.entity.song:Name']
        for i in range(len(string_list)):
            if "sys" in string_list[i]:
                string_list[i] = "@" + string_list[i]
        # TODO 此时 string_list = ['唱一首', '@sys.entity.singer:Singer', '的', '@sys.entity.song:Name']
        return string_list

    def replace_entity(self, query, corpus_info):
        final_query = ""
        query_str_list = self.split_string_for_text(query)
        for entity in query_str_list:
            if "sys" in entity:
                final_query += random.choice(corpus_info[entity])
            else:
                final_query += entity
        return final_query


class TalkTest(Talk):
    task_results = []
    task_cases = []

    def get_test_cases(self, case_json, corpus_json):
        """从配置文件中组合case 形成case集"""
        self.case_info = Handlers.load_json(case_json)
        self.corpus_info = Handlers.load_json(corpus_json)

        domain = self.case_info[0]["domain"]
        for intent in self.case_info[0]["intents"]:
            intent_name = intent["intent_name"]
            intent_text = Handlers.list_duplicate_removal(intent["intent_text"])
            for query in intent_text:
                query = self.replace_entity(query, self.corpus_info)
                case = {
                    "question": query,
                    "source": "user_service",
                    "domain": domain,
                    "intent": intent_name,
                }
                self.task_cases.append(case)

        return self.task_cases

    def testing(self):
        """根据case集 调用接口/v1/sv/talk测试"""
        for case in self.task_cases:
            res = self.talk(case["question"])

            result = {
                "question": case["question"],
                "source": case["source"],
                "act_source": res["source"],
                "domain": case["domain"],
                "act_domain": res["domain"],
                "intent": case["intent"],
                "act_intent": None,
                "tts": None,
                "traceId": res["traceId"],
                "traces": json.dumps(res["traces"], ensure_ascii=False),
                "edg_cost": res["edg_cost"],
                "inner_cost": res["inner_cost"]
            }
            try:
                result["act_intent"] = res["tts"][0]["action"]["param"]["intent"]
            except:
                result["act_intent"] = None
            try:
                result["tts"] = res["tts"][0]["text"]
            except:
                pass

            self.task_results.append(result)

        return self.task_results

    def reporter(self):
        """测试结果写入excel"""
        file_name = Handlers.time_strf_now() + ".xlsx"
        Handlers.write_list_map_as_excel(self.task_results, excel_writer=file_name, sheet_name="Sheet1", index=False)

    def record(self, task_name="poetry_conversation", task_type="conversation"):
        """测试数据写入MongoDB"""
        con = pymongo.MongoClient("mongodb://root:123456@10.12.32.30:27017")
        db = con[MG_DB]
        col_task = db[MG_COL_TASK]  # 记录测试任务
        col_rl = db[MG_COL_RL]  # 记录关系
        col_cases = db[MG_COL_CASES]  # 记录测试用例
        col_results = db[MG_COL_RESULTS]  # 记录测试结果

        if col_task.find_one({"name": task_name, "type": task_type}):
            task_id = col_task.find_one({"name": task_name})["_id"]
        else:
            _id = col_task.insert_one({"name": task_name,
                                       "type": task_type})
            task_id = _id.inserted_id

        _id = col_cases.insert_one({"cases": self.task_cases})
        cases_id = _id.inserted_id

        result_ids = []
        for result in self.task_results:
            _id = col_results.insert_one({"result": result})
            result_id = _id.inserted_id
            result_ids.append(str(result_id))

        tm = Handlers.time_strf_now()

        col_rl.insert_one({"task_id": str(task_id),
                           "cases_id": str(cases_id),
                           "result_id": result_ids,
                           "execute_time": tm})

    # sv接口对比测试
    def get_test_cases_sv(self):
        con = pymongo.MongoClient("mongodb://root:123456@10.12.32.30:27017")
        db = con[MG_DB]
        col_task = db[MG_COL_TASK]  # 记录测试任务
        col_rl = db[MG_COL_RL]  # 记录关系
        col_cases = db[MG_COL_CASES]  # 记录测试用例
        col_results = db[MG_COL_RESULTS]  # 记录测试结果

        task_name = "poetry_conversation"
        task_type = "sv"

        if col_task.find_one({"name": task_name}):
            task_id = col_task.find_one({"name": task_name})["_id"]

            if col_rl.find_one({"task_id": str(task_id)}):
                case_id = col_rl.find_one({"task_id": str(task_id)})["cases_id"]

                if col_cases.find_one({"_id": ObjectId(str(case_id))}):
                    self.task_cases = col_cases.find_one({"_id": ObjectId(str(case_id))})["cases"]
                    return self.task_cases

    def testing_sv(self):
        t = SmartVoice(agent_id=self.agent_id, base_url="http://172.16.23.85:30950",
                       login_user="admin@cloudminds", login_passwd="Smartvoice1506")
        for case in self.task_cases:
            res, edg_cost, inner_cost = t.send_qa(case["question"])
            result = {
                "question": case["question"],
                "source": case["source"],
                "act_source": res["source"],
                "domain": case["domain"],
                "act_domain": res["hitlog"]["domain"],
                "intent": case["intent"],
                "act_intent": res["hitlog"]["intent"],
                "tts": res["tts"][0]["text"],
                "traceId": res["hitlog"]["traceId"],
                "traces": None,
                "edg_cost": edg_cost,
                "inner_cost": inner_cost
            }
            self.task_results.append(result)

        return self.task_results


def conversation_mission(agent_id, domain):
    ng_file = "data/sv_" + domain + ".json"
    corpus_file = "data/corpus_" + domain + ".json"
    r = TalkTest(agent_id=agent_id)
    r.get_test_cases(case_json=ng_file, corpus_json=corpus_file)
    r.testing()
    r.reporter()
    # r.record()


def conversation_mission_sv():
    t = TalkTest(agent_id="1500")
    t.get_test_cases_sv()
    t.testing_sv()
    t.reporter()
    t.record(task_type="sv")


if __name__ == '__main__':
    # conversation_mission_sv()
    conversation_mission("1509", "times")
