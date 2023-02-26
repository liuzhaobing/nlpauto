# -*- coding:utf-8 -*-
import json
import random

"""
多轮 关于当下
"""


def convert_temperature(temperature_str):
    """温度转换 -3 转为 零下3度   30 转为 30度"""
    if "-" in temperature_str:
        return "零下" + temperature_str[1:] + "度"
    return temperature_str + "度"


def return_get_weather_answer_string():
    weather_list = json.loads(proResult["session"]["variables"]["api_weather"]["value"])["weather"]
    location = weather_list[0]["location"]
    cond_txt_d = weather_list[0]["condTxtD"]
    cond_txt_n = weather_list[0]["condTxtN"]
    tmp_min = weather_list[0]["temperatureMin"]
    tmp_max = weather_list[0]["temperatureMax"]
    wind_dir = weather_list[0]["windDirection"]
    wind_sc = weather_list[0]["windSpeed"]
    uv_index = weather_list[0]["uvIntensity"]
    date = weather_list[0]["date"]
    humidity = weather_list[0]["humidity"]

    temp1 = location + "，" + date + "天气" + cond_txt_d
    if cond_txt_d != cond_txt_n:
        temp1 += "转" + cond_txt_n
    temp1 += "，" + convert_temperature(tmp_min) + "至" + convert_temperature(tmp_max) + "，"

    if "雨" in cond_txt_d + cond_txt_n:
        temp2 = ["出门记得带把伞哦", "这两天就别洗车咯", "穿双防水的鞋吧"]
        return temp1 + temp2[random.randint(0, len(temp2) - 1)]

    if "雪" in cond_txt_d + cond_txt_n:
        temp2 = ["出门记得带双手套", "出门记得穿双防滑的鞋", "叫上朋友来家吃火锅吧"]
        return temp1 + temp2[random.randint(0, len(temp2) - 1)]

    if int(wind_sc.split("-")[1]) >= 7:
        temp2 = ["外面风呼呼的，请尽量减少外出", "外面风超大，你可小心别被吹跑了。"]
        return temp1 + temp2[random.randint(0, len(temp2) - 1)]

    tmp_min_num = int(tmp_min)
    tmp_max_num = int(tmp_max)

    if tmp_min_num < 0:
        temp2 = ["别在室外呆太久哦，小心冻成冰棍", "出门的话建议您随身带片暖宝宝"]
        return temp1 + temp2[random.randint(0, len(temp2) - 1)]

    if 0 <= tmp_min_num < 8:
        temp2 = ["天气寒冷，请注意保暖", "若不穿秋裤，后果请自负"]
        return temp1 + temp2[random.randint(0, len(temp2) - 1)]
    if 8 <= tmp_max_num < 15:
        wind_sc_num = int(wind_sc.split("-")[1])
        if 1 <= wind_sc_num <= 4:
            temp2 = ["天气变化多端，注意别感冒啦", "很适合来一杯香甜的热拿铁呢"]
            return temp1 + temp2[random.randint(0, len(temp2) - 1)]

        if wind_sc_num >= 5:
            temp2 = ["穿件酷酷的风衣出门吧", "外面妖风阵阵，记得添加衣物哦"]
            return temp1 + temp2[random.randint(0, len(temp2) - 1)]

    if 15 <= tmp_max_num < 23:
        temp2 = ["很适合出门夜跑呢", "温度适宜，适合外出游玩"]
        return temp1 + temp2[random.randint(0, len(temp2) - 1)]

    if 23 <= tmp_max_num < 30:
        temp2 = ["约上朋友出去野个餐吧", "切记不要贪凉，感冒了我会心疼的"]
        return temp1 + temp2[random.randint(0, len(temp2) - 1)]

    if tmp_max_num >= 30 and int(uv_index) > 5:
        temp2 = ["紫外线强烈注意防晒哦", "紫外线强烈戴顶帽子出门吧"]
        return temp1 + temp2[random.randint(0, len(temp2) - 1)]

    if tmp_max_num >= 30 and int(uv_index) <= 5:
        temp2 = ["天热记得多多补充水分哦", "天气闷热穿件透气的衬衣吧"]
        return temp1 + temp2[random.randint(0, len(temp2) - 1)]

    return temp1


def redefine_movie():
    try:
        api_movie = json.loads(proResult["session"]["variables"]["api_movie"]["value"])
        for i in range(len(api_movie["movie_infos"])):
            try:
                api_movie["movie_infos"][i]["movie_title"] = api_movie["movie_infos"][i]["movie_title"].split(" ")[0]
            except:
                pass
            try:
                api_movie["movie_infos"][i]["director"] = "、".join(api_movie["movie_infos"][i]["director"].split(" / "))
            except:
                pass
            try:
                api_movie["movie_infos"][i]["screenwriter"] = "、".join(api_movie["movie_infos"][i]["screenwriter"].split(" / ")[:3])
            except:
                pass
            try:
                api_movie["movie_infos"][i]["actor"] = "、".join(api_movie["movie_infos"][i]["actor"].split(" / ")[:3])
            except:
                pass
            try:
                api_movie["movie_infos"][i]["movie_type"] = "、".join(api_movie["movie_infos"][i]["movie_type"].split(" / ")[:2])
            except:
                pass
        proResult["session"]["variables"]["api_movie"]["value"] = json.dumps(api_movie)
    except:
        pass


proResult["session"]["variables"]["tomorrow_weather"] = {"key": "tomorrow_weather",
                                                         "value": return_get_weather_answer_string()}
