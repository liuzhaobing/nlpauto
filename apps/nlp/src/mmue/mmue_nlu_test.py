# -*- coding:utf-8 -*-
import requests

from utils.handler import Handlers


def nlu_debug_info(query, context=""):
    payload = {
        "traceid": "123",
        "agentid": "1",
        "query": query,
        "context": context,
        "robot_name": ""
    }
    response = requests.request(method="POST", url="http://172.16.23.15:30375/nlp-sdk/nlu/intent-recognize",
                                json=payload)
    data = response.json()["data"]
    return {
        "query": query,
        "domainname": data["domainname"],
        "intentname": data["intentname"],
        "parameters": data["parameters"],
        "entity_trie": data["debugInfo"]["entity_trie"],
        "ner_trie": data["debugInfo"]["ner_entity"]
    }


def run_case():
    cases = ['speak slower',
             'to reduce the volume',
             'how much is the current volume',
             'speed up your speech',
             'increase in the volume',
             '静音',
             'resume normal speech rate',
             'keep quiet',
             'mute off',
             '小声点',
             '你好小声点',
             '推行模式',
             '小声一点',
             '小声一点',
             '小声点小声点',
             '你现在电量多少',
             '你有多少电量',
             '你还有电吗',
             '你还有多少电量',
             '你还有多少电',
             '你有多少电',
             '你还有多少电量啊',
             '小声点',
             '小声一点',
             '当前电量',
             '你还有多少电',
             '你的电量是多少',
             '你现在还有多少电啊',
             '你现在有多少电',
             '电量还剩多少',
             '还有多少电',
             '有多少电',
             '查询当前电量',
             '查询电量',
             '你的电量有多少',
             '现在电量是多少',
             '现在有多少电',
             '你要干什么',
             '你还有多少电呀',
             '你还有多少电小维小维',
             '显示电量',
             '你的电量还剩多少啊',
             '你好小声点小声点',
             '小声一点',
             '小声一点儿',
             '小声点',
             '小声点儿',
             ]
    results = []
    for case in cases:
        result = nlu_debug_info(query=case)
        results.append(result)
    return results


if __name__ == '__main__':
    results_now = run_case()
    Handlers.write_list_map_as_excel(list_map=results_now, excel_writer=r"C:\Users\admin\Desktop\system_regex.xlsx",
                                     sheet_name="Sheet1", index=False)
