# -*- coding:utf-8 -*-
import json


def check_dance():
    api_dance = proResult["session"]["variables"]["api_dance"]["value"]
    api_dance = json.loads(api_dance)
    if api_dance.__contains__("data"):
        data = api_dance["data"]
        if data.__contains__("canFlag"):
            if data["canFlag"]:
                return "can"
        if data.__contains__("danceList"):
            return "another"
        return "cannot"


proResult["session"]["variables"]["can_dance_this_time"] = {"key": "can_dance_this_time", "value": check_dance()}
