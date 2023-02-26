#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import requests
from utils.handler import Handlers


class IntentRecognize:
    @staticmethod
    def run(url, context, query, agentid, traceid, robot_name):
        if not traceid:
            traceid = Handlers.uuid_str()

        start = Handlers.time_now_10s()
        response = requests.post(url=url, headers={'Content-Type': 'application/json'},
                                 json={"traceid": traceid,
                                       "agentid": agentid,
                                       "query": query,
                                       "context": context,
                                       "robot_name": robot_name}, timeout=10)
        edg_cost = (Handlers.time_now_10s() - start) * 1000
        res = json.loads(response.content)
        return res, edg_cost
