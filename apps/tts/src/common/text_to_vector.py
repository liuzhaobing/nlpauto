#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import requests

from utils.handler import Handlers


class TextToVector:

    @staticmethod
    def run(texts):
        """# 将多个文本 转向量"""
        resp = requests.post(url="http://nlp-api.bj-fit-86:32189/nlp-sdk/qqsim/sentence",
                             headers={'Content-Type': 'application/json'},
                             json={"trace_id": Handlers.uuid_str(), "agent_id": "1", "robot_ name": "",
                                   "texts": texts})

        res = json.loads(resp.content)
        json_context = res["data"]
        return json_context
