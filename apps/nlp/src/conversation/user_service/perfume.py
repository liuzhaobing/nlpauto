# -*- coding:utf-8 -*-

"""
香水推荐 数据处理
"""
import json
import random


def check_title():
    proResult["session"]["variables"]["success"] = {"key": "success", "value": "false"}
    if not proResult["session"]["variables"].__contains__("api_media"):
        return False
    try:
        if len(proResult["session"]["variables"]["api_media"]["value"]) < 5:
            return False
        api_media = json.loads(proResult["session"]["variables"]["api_media"]["value"])
    except:
        return False

    meidas = api_media["medias"]

    media = meidas[random.randint(0, len(meidas) - 1)]
    api_titles = media["title"].split("||")
    media["title"] = api_titles[0]
    media["description"] = api_titles[1]
    proResult["session"]["variables"]["now_production_info"] = {"key": "now_production_info",
                                                                "value": json.dumps(media, ensure_ascii=False)}
    proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
    return True


check_title()
