# -*- coding:utf-8 -*-
"""
金闼展厅多轮需求
"""
import json
import random


def choose_joke():
    joke_store = json.loads(proResult["session"]["variables"]["joke_store"]["value"])
    now_store = json.loads(proResult["session"]["variables"]["now_store"]["value"])
    now_round = proResult["session"]["variables"]["now_round"]["value"]
    min_tmp = proResult["session"]["variables"]["min_temperature"]["value"]
    proResult["session"]["variables"]["joke_status"] = {"key": "joke_status", "value": "success"}

    sig = 1
    weather_question = ""
    if int(min_tmp) <= 15:
        sig = 1
        weather_question = "我来给您讲个小笑话暖和暖和好吗？"

    elif 15 < int(min_tmp) < 25:
        sig = 2
        weather_question = "我来给您讲一个和天气一样温暖的小故事好吗？"

    elif int(min_tmp) >= 25:
        sig = 3
        weather_question = "我来给您讲一个冷笑话冷静冷静好吗？"

    if int(now_round) > 1 and not now_store:
        proResult["session"]["variables"]["joke_status"]["value"] = "failure"
        return weather_question, ""

    if not now_store:
        joke_candidate = []
        for joke in joke_store:
            if joke["joke_type_en"] == sig:
                joke_candidate.append(joke)

        if not joke_candidate:
            now_joke = joke_store[random.randint(0, len(joke_store) - 1)]
        else:
            now_joke = joke_candidate[random.randint(0, len(joke_candidate) - 1)]

        joke_candidate.remove(now_joke)
        proResult["session"]["variables"]["now_store"] = {"key": "now_store",
                                                          "value": json.dumps(joke_candidate, ensure_ascii=False)}

        return weather_question, now_joke["joke_info"]

    now_joke = now_store[random.randint(0, len(now_store) - 1)]
    now_store.remove(now_joke)
    proResult["session"]["variables"]["now_store"] = {"key": "now_store",
                                                      "value": json.dumps(now_store, ensure_ascii=False)}

    return weather_question, now_joke["joke_info"]


q, a = choose_joke()
proResult["session"]["variables"]["weather_question"] = {"key": "weather_question", "value": q}
proResult["session"]["variables"]["now_joke"] = {"key": "now_joke", "value": a}
