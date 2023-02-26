# -*- coding:utf-8 -*-
import json
"""
演示多轮 AI写诗部分
"""


def compose_poem_string():
    try:
        now_poem = proResult["session"]["variables"]["api_poetry"]["value"]
        now_poem_data = json.loads(now_poem)["data"]

        poem_string = ""
        i = True
        for d in now_poem_data:
            poem_string += d
            if i:
                poem_string += "，"
                i = False
            else:
                poem_string += "。"
                i = True
        proResult["session"]["variables"]["now_poem"] = {"key": "now_poem", "value": poem_string}
        proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
    except:
        proResult["session"]["variables"]["success"] = {"key": "success", "value": "false"}


compose_poem_string()
