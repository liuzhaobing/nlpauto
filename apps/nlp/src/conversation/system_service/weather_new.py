# -*- coding:utf-8 -*-
"""weather_new 技能下所有意图的统一回复处理"""
import json
import time
import random

# 根据实际情况修改/填写对应的词槽名，手动修改即可
slot_country = "country"
slot_province = "province"
slot_city = "city"
slot_date = "date"
slot_duration = "duration"
default_answer = "天气很好~"

weather_list = []
weather_info = {}
api_weather = {}

# 提取api响应信息
if proResult.__contains__("extra"):
    if proResult["extra"].__contains__("api_info"):
        if proResult["extra"]["api_info"].__contains__("response"):
            api_weather = json.loads(proResult["extra"]["api_info"]["response"])
            """按日期查询天气api"""
            if api_weather.__contains__("weather"):
                weather_list = api_weather["weather"]
            """查询现在天气api"""
            if api_weather.__contains__("lifeStyle"):
                weather_list = api_weather["lifeStyle"]
            """按天查空气指数"""
            if api_weather.__contains__("pollutions"):
                weather_list = api_weather["pollutions"]
            """按现在查询空气指数"""
            if api_weather.__contains__("pm25"):
                weather_info = api_weather

# 提取当前轮意图
current_intent = proResult["quresult"]["intent"]


# 获取时间date_origin
def get_date_str():
    date = ""
    if proResult["quresult"].__contains__("slots"):
        if proResult["quresult"]["slots"].__contains__(slot_date):
            date = proResult["quresult"]["slots"][slot_date]["origin"]

    if proResult["quresult"].__contains__("slots"):
        if proResult["quresult"]["slots"].__contains__(slot_duration):
            date = proResult["quresult"]["slots"][slot_duration]["origin"]

    if not date or date == "":
        date = convert_date(weather_list[0]["date"])
    return date


def convert_date(date_str):
    """2022-08-08转为[今天, 明天, 后天, 2022年8月8日]其中一个"""
    if not date_str or date_str == "":
        return ""

    y, m, d = date_str[:4], date_str[5:7], date_str[-2:]

    date_time = int(y + m + d)
    now_time = int(time.strftime("%Y%m%d"))

    interval_days = date_time - now_time

    if interval_days == 0:
        return "今天"
    if interval_days == 1:
        return "明天"
    if interval_days == 2:
        return "后天"

    new_m, new_d = m, d
    if int(m) < 10:
        new_m = m[1]
    if int(d) < 10:
        new_d = d[1]

    return y + "年" + new_m + "月" + new_d + "日"


def convert_temperature(temperature_str):
    """温度转换 -3 转为 零下3度   30 转为 30度"""
    if "-" in temperature_str:
        return "零下" + temperature_str[1:] + "度"
    return temperature_str + "度"


def get_pollution():
    """
    按天查空气指数api
    执行pollution相关回复，包括以下意图：

        GetPollution, GetPollution_Followup,

    """
    # Step1 检查api查询结果是否为空
    if not weather_list:
        proResult["session"]["variables"]["status"] = {"key": "status", "value": "failure"}
        return default_answer

    location = weather_list[0]["location"]
    aqi_str = weather_list[0]["aqi"]
    aqi_num = int(aqi_str)
    date = get_date_str()

    # Step2 组装端侧需要的raw_data
    raw_data = {
        "location": location,
        "pub_time": api_weather["pubtime"] if api_weather.__contains__("pubtime") else "",
        "source": api_weather["source"] if api_weather.__contains__("source") else "",
        "air_forecast": []
    }
    for data in weather_list:
        raw_data["air_forecast"].append({
            "aqi": data["aqi"] if api_weather.__contains__("aqi") else "",
            "date": data["date"] if api_weather.__contains__("date") else "",
            "main": data["main"] if api_weather.__contains__("main") else "",
            "qlty": data["qlty"] if api_weather.__contains__("qlty") else ""
        })

    proResult["session"]["variables"]["raw_data"] = {"key": "raw_data",
                                                     "value": json.dumps(raw_data, ensure_ascii=False)}
    # GetPollution和GetPollution_Followup的回答
    if current_intent in ["GetPollution", "GetPollution_Followup"]:
        if len(weather_list) > 1:
            temp = location
            for weather in weather_list:
                temp += convert_date(weather["date"]) + "，空气" + weather["qlty"] + "，空气质量指数" + \
                        weather["aqi"] + "，主要污染物为" + weather["main"] + "。"
            return temp

        temp1 = location + "，" + date + "，" + "空气质量指数" + aqi_str
        if 0 <= aqi_num <= 50:
            temp2 = ["空气很好", "空气很清新"]
            return temp1 + "，" + temp2[random.randint(0, len(temp2) - 1)] + "，尽情享受户外活动吧。"
        if 51 <= aqi_num <= 100:
            temp2 = ["空气良好", "空气还不错"]
            return temp1 + "，" + temp2[random.randint(0, len(temp2) - 1)] + "，出门散散步吧。"
        if 101 <= aqi_num <= 150:
            temp2 = ["空气轻度污染", "空气有点脏脏的呢"]
            return temp1 + "，" + temp2[random.randint(0, len(temp2) - 1)] + "，请尽量减少外出。"
        if 151 <= aqi_num <= 200:
            temp2 = ["空气中度污染", "空气比较差"]
            return temp1 + "，" + temp2[random.randint(0, len(temp2) - 1)] + "，不要在户外进行高强度的运动哦。"
        if 201 <= aqi_num <= 300:
            temp2 = ["空气脏的让人窒息", "空气很差"]
            return temp1 + "，" + temp2[random.randint(0, len(temp2) - 1)] + "，出门一定要带口罩啊。"
        if 300 < aqi_num:
            temp2 = ["空气严重污染", "空气污染爆表啦"]
            return temp1 + "，" + temp2[random.randint(0, len(temp2) - 1)] + "，乖乖待在屋子里吧。"
        return temp1


def get_lifestyle():
    """
    查询现在天气api
    执行index相关回复，包括以下意图：

        GetDressingIndex, GetDressingIndex_Followup,

        GetExerciseIndex, GetExerciseIndex_Followup,

        GetLivingIndex, GetLivingIndex_Followup,

        GetWashingIndex, GetWashingIndex_Followup
    """
    # Step1 检查api查询结果是否为空
    if not weather_list:
        proResult["session"]["variables"]["status"] = {"key": "status", "value": "failure"}
        return default_answer

    # Step2 其他检查
    raw_data = {
        "cloud": api_weather["cloud"] if api_weather.__contains__("cloud") else "",
        "cond_code": api_weather["condCode"] if api_weather.__contains__("condCode") else "",
        "cond_code_img": api_weather["condCodeImg"] if api_weather.__contains__("condCodeImg") else "",
        "cond_txt": api_weather["condTxt"] if api_weather.__contains__("condTxt") else "",
        "fl": api_weather["fl"] if api_weather.__contains__("fl") else "",
        "hum:": api_weather["humidity"] if api_weather.__contains__("humidity") else "",
        "location": api_weather["location"] if api_weather.__contains__("location") else "",
        "pcpn": api_weather["pcpn"] if api_weather.__contains__("pcpn") else "",
        "pres": api_weather["pres"] if api_weather.__contains__("pres") else "",
        "pub_time": api_weather["pubTime"] if api_weather.__contains__("pubTime") else "",
        "source": api_weather["source"] if api_weather.__contains__("source") else "",
        "tmp": api_weather["temperature"] if api_weather.__contains__("temperature") else "",
        "vis": api_weather["vis"] if api_weather.__contains__("vis") else "",
        "wind_deg": api_weather["windDeg"] if api_weather.__contains__("windDeg") else "",
        "wind_dir": api_weather["windDirection"] if api_weather.__contains__("windDirection") else "",
        "wind_sc": api_weather["windScale"] if api_weather.__contains__("windScale") else "",
        "wind_spd": api_weather["windSpeed"] if api_weather.__contains__("windSpeed") else "",
        "lifestyle": api_weather["lifeStyle"] if api_weather.__contains__("lifeStyle") else ""
    }
    proResult["session"]["variables"]["raw_data"] = {"key": "raw_data",
                                                     "value": json.dumps(raw_data, ensure_ascii=False)}
    # Step3 获取天气列表中第一个天气所有信息
    index_type = ""
    if current_intent in ["GetDressingIndex", "GetDressingIndex_Followup"]:
        index_type = "drsg"
    elif current_intent in ["GetExerciseIndex", "GetExerciseIndex_Followup"]:
        index_type = "sport"
    elif current_intent in ["GetLivingIndex", "GetLivingIndex_Followup"]:
        index_type = "comf"
    elif current_intent in ["GetWashingIndex", "GetWashingIndex_Followup"]:
        index_type = "cw"
    index_value = ""
    for index_info in weather_list:
        if index_info["type"] == index_type:
            index_value = index_info["txt"]
            break
    location = api_weather["location"]
    date = "今天"
    if index_value:
        return location + date + index_value


def get_weather():
    """
    按日期查询天气api
    执行weather相关的回复，包括以下意图：

        GetWeather, GetWeather_Followup,

        GetWind, GetWind_Followup,

        GetUvIndex, GetUvIndex_Followup,

        GetThunder, GetThunder_Followup,

        GetTemperature, GetTemperature_Followup,

        GetSnow, GetSnow_Followup,

        GetRain, GetRain_Followup,

        GetHumidity, GetHumidity_Followup,

        GetHailstone, GetHailstone_Followup,

    """
    # Step1 检查api查询结果是否为空
    if not weather_list:
        proResult["session"]["variables"]["status"] = {"key": "status", "value": "failure"}
        return default_answer

    # Step2 检查范围是否超过city
    if proResult["quresult"].__contains__("slots") and proResult["quresult"].__contains__("request_params"):
        if proResult["quresult"]["slots"].__contains__(slot_country) \
                and proResult["quresult"]["request_params"].__contains__("Default") \
                and proResult["quresult"]["slots"][slot_country]["origin"] \
                in proResult["quresult"]["request_params"]["Default"]:
            if not proResult["quresult"]["slots"].__contains__(slot_city) \
                    or (proResult["quresult"]["slots"].__contains__(slot_city)
                        and proResult["quresult"]["slots"][slot_country]["origin"] not in
                        proResult["quresult"]["request_params"]["Default"]):
                proResult["session"]["variables"]["status"] = {"key": "status", "value": "failure"}
                return "这个范围太大了呢，请告诉我具体是哪个城市吧！"
        if proResult["quresult"]["slots"].__contains__(slot_province) \
                and proResult["quresult"]["request_params"].__contains__("Default") \
                and proResult["quresult"]["slots"][slot_province]["origin"] \
                in proResult["quresult"]["request_params"]["Default"]:
            if not proResult["quresult"]["slots"].__contains__(slot_city) \
                    or (proResult["quresult"]["slots"].__contains__(slot_city)
                        and proResult["quresult"]["slots"][slot_province]["origin"] not in
                        proResult["quresult"]["request_params"]["Default"]):
                proResult["session"]["variables"]["status"] = {"key": "status", "value": "failure"}
                return "这个范围太大了呢，请告诉我具体是哪个城市吧！"

    # Step3 获取天气列表中第一个天气所有信息
    date = get_date_str()
    location = api_weather["location"] if api_weather.__contains__("location") else (weather_list[0]["location"] if weather_list[0].__contains__("location") else "")
    cond_txt_d = weather_list[0]["condTxtD"]
    cond_txt_n = weather_list[0]["condTxtN"]
    tmp_min = weather_list[0]["temperatureMin"]
    tmp_max = weather_list[0]["temperatureMax"]
    wind_dir = weather_list[0]["windDirection"]
    wind_sc = weather_list[0]["windScale"] if weather_list[0].__contains__("windScale") else weather_list[0]["windSpeed"]
    uv_index = weather_list[0]["uvIntensity"]

    proResult["session"]["variables"]["min_temperature"] = {"key": "min_temperature", "value": tmp_min}
    # Step4 获取槽位继承的位置信息
    if proResult["quresult"].__contains__("slots"):
        if proResult["quresult"]["slots"].__contains__(slot_city):
            location = proResult["quresult"]["slots"][slot_city]["origin"]

    # Step5 组装端侧需要的raw_data
    raw_data = {
        "location": location,
        "pub_time": api_weather["pubtime"] if api_weather.__contains__("pubtime") else "",
        "source": api_weather["source"] if api_weather.__contains__("source") else "",
        "weather_data": []
    }
    for data in api_weather["weather"]:
        raw_data["weather_data"].append({
            "cond_code_d": data["condCodeD"] if data.__contains__("condCodeD") else "",
            "cond_code_n": data["condCodeN"] if data.__contains__("condCodeN") else "",
            "cond_code_img_d": data["condCodeImgD"] if data.__contains__("condCodeImgD") else "",
            "cond_code_img_n": data["condCodeImgN"] if data.__contains__("condCodeImgN") else "",
            "cond_txt_d": data["condTxtD"] if data.__contains__("condTxtD") else "",
            "cond_txt_n": data["condTxtN"] if data.__contains__("condTxtN") else "",
            "date": data["date"] if data.__contains__("date") else "",
            "hum": data["humidity"] if data.__contains__("humidity") else "",
            "pcpn": data["pcpn"] if data.__contains__("pcpn") else "",
            "pres": data["pres"] if data.__contains__("pres") else "",
            "tmp_max": data["temperatureMax"] if data.__contains__("temperatureMax") else "",
            "tmp_min": data["temperatureMin"] if data.__contains__("temperatureMin") else "",
            "uv_index": data["uvIntensity"] if data.__contains__("uvIntensity") else "",
            "vis": data["vis"] if data.__contains__("vis") else "",
            "wind_deg": data["windDegree"] if data.__contains__("windDegree") else "",
            "wind_dir": data["windDirection"] if data.__contains__("windDirection") else "",
            "wind_sc": data["windScale"] if data.__contains__("windScale") else "",
            "wind_spd": data["windSpeed"] if data.__contains__("windSpeed") else "",
            "pop": ""
        })
    proResult["session"]["variables"]["raw_data"] = {"key": "raw_data",
                                                     "value": json.dumps(raw_data, ensure_ascii=False)}

    # GetWeather和GetWeather_Followup的回答
    if current_intent in ["GetWeather", "GetWeather_Followup"]:
        days = len(weather_list)
        result = location
        if 1 < days <= 7:
            for weather in weather_list:
                result += convert_date(weather["date"]) + "，" + weather["condTxtD"]
                if weather["condTxtD"] != weather["condTxtN"]:
                    result += "转" + weather["condTxtN"]
                result += "，" + convert_temperature(weather["temperatureMin"]) + "至" + \
                          convert_temperature(weather["temperatureMax"]) + "，"

            result += "若想了解更多，也可具体询问我某一天的天气哦。"
            return result

        if days > 7:
            min_sum, max_sum = 0, 0
            cond_table = {"晴天": 0, "多云": 0, "阴天": 0, "降雨": 0, "降雪": 0}
            temp_table = {"hot": 0, "cold": 0}

            for weather in weather_list:
                min_sum += int(weather["temperatureMin"])
                max_sum += int(weather["temperatureMax"])

                if "晴" in weather["condTxtD"]:
                    cond_table["晴天"] += 1
                if "多云" in weather["condTxtD"]:
                    cond_table["多云"] += 1
                if "阴" in weather["condTxtD"]:
                    cond_table["阴天"] += 1
                if "雨" in weather["condTxtD"]:
                    cond_table["降雨"] += 1
                if "雪" in weather["condTxtD"]:
                    cond_table["降雪"] += 1

                if int(weather["temperatureMin"]) >= 27:
                    temp_table["hot"] += 1
                if int(weather["temperatureMax"]) <= 5:
                    temp_table["cold"] += 1

            result += "未来一周， "
            min_avg = int(min_sum / days + 0.5)  # 四舍五入向下取整
            max_avg = int(max_sum / days + 0.5)  # 四舍五入向下取整
            tmp_min_str = convert_temperature(str(min_avg)) + "，"
            tmp_max_str = convert_temperature(str(max_avg)) + "，"

            for cond, num in cond_table.items():
                if num >= 4:
                    return result + "以" + cond + "为主，" + "平均最低温" + tmp_min_str + "平均最高温" + tmp_max_str + "若想了解更多，也可具体询问我某一天的天气哦。"

            if temp_table["hot"] >= 4:
                return result + "以热的冒烟模式为主，" + "平均最低温" + tmp_min_str + "平均最高温" + tmp_max_str + "若想了解更多，也可具体询问我某一天的天气哦。"
            if temp_table["cold"] >= 4:
                return result + "以冷的发抖模式为主，" + "平均最低温" + tmp_min_str + "平均最高温" + tmp_max_str + "若想了解更多，也可具体询问我某一天的天气哦。"

            if max_avg - min_avg > 10:
                return result + "温差较大，" + "平均最低温" + tmp_min_str + "平均最高温" + tmp_max_str + "若想了解更多，也可具体询问我某一天的天气哦。"

            return result + "平均最低温" + tmp_min_str + "平均最高温" + tmp_max_str + "若想了解更多，也可具体询问我某一天的天气哦。"

        temp1 = location + "，" + date + "天气" + cond_txt_d
        if cond_txt_d != cond_txt_n:
            temp1 += "转" + cond_txt_n
        temp1 += "，" + convert_temperature(tmp_min) + "至" + convert_temperature(tmp_max) + "，"

        if "雨" in cond_txt_d + cond_txt_n:
            temp2 = ["出门记得带把伞哦。", "这两天就别洗车咯。", "穿双防水的鞋吧。"]
            return temp1 + temp2[random.randint(0, len(temp2) - 1)]

        if "雪" in cond_txt_d + cond_txt_n:
            temp2 = ["出门记得带双手套。", "出门记得穿双防滑的鞋。", "叫上朋友来家吃火锅吧。"]
            return temp1 + temp2[random.randint(0, len(temp2) - 1)]

        if int(wind_sc.split("-")[1]) >= 7:
            temp2 = ["外面风呼呼的，请尽量减少外出。", "外面风超大，你可小心别被吹跑了。"]
            return temp1 + temp2[random.randint(0, len(temp2) - 1)]

        tmp_min_num = int(tmp_min)
        tmp_max_num = int(tmp_max)

        if tmp_min_num < 0:
            temp2 = ["别在室外呆太久哦，小心冻成冰棍。", "出门的话建议您随身带片暖宝宝。"]
            return temp1 + temp2[random.randint(0, len(temp2) - 1)]

        if 0 <= tmp_min_num < 8:
            temp2 = ["天气寒冷，请注意保暖。", "若不穿秋裤，后果请自负。"]
            return temp1 + temp2[random.randint(0, len(temp2) - 1)]
        if 8 <= tmp_max_num < 15:
            wind_sc_num = int(wind_sc.split("-")[1])
            if 1 <= wind_sc_num <= 4:
                temp2 = ["天气变化多端，注意别感冒啦。", "很适合来一杯香甜的热拿铁呢。"]
                return temp1 + temp2[random.randint(0, len(temp2) - 1)]

            if wind_sc_num >= 5:
                temp2 = ["穿件酷酷的风衣出门吧。", "外面妖风阵阵，记得添加衣物哦。"]
                return temp1 + temp2[random.randint(0, len(temp2) - 1)]

        if 15 <= tmp_max_num < 23:
            temp2 = ["很适合出门夜跑呢。", "温度适宜，适合外出游玩。"]
            return temp1 + temp2[random.randint(0, len(temp2) - 1)]

        if 23 <= tmp_max_num < 30:
            temp2 = ["约上朋友出去野个餐吧。", "切记不要贪凉，感冒了我会心疼的。"]
            return temp1 + temp2[random.randint(0, len(temp2) - 1)]

        if tmp_max_num >= 30 and int(uv_index) > 5:
            temp2 = ["紫外线强烈注意防晒哦。", "紫外线强烈戴顶帽子出门吧。"]
            return temp1 + temp2[random.randint(0, len(temp2) - 1)]

        if tmp_max_num >= 30 and int(uv_index) <= 5:
            temp2 = ["天热记得多多补充水分哦。", "天气闷热穿件透气的衬衣吧。"]
            return temp1 + temp2[random.randint(0, len(temp2) - 1)]

        return temp1

    # GetWind和GetWind_Followup的回答
    if current_intent in ["GetWind", "GetWind_Followup"]:
        if len(weather_list) > 1:
            temp = location
            for weather in weather_list:
                temp += convert_date(weather["date"]) + "，白天" + weather["condTxtD"] + "，夜晚" + weather["condTxtN"] \
                        + "，" + weather["windDirection"] + "，风力" + weather["windScale"] + "级。"
            return temp

        temp = "差点把我都给吹跑了。"

        if "1-2" in wind_sc:
            temp = "风很柔和，就像妈妈的怀抱一样。"
        if "3-4" in wind_sc:
            temp = "风有点大呢，把我的发型都给吹乱了。"
        if "4-5" in wind_sc:
            temp = "风呼呼的，把小树苗吹的摇摇晃晃的。"

        wind_sc_str = "风力" + wind_sc.split("-")[0] + "至" + wind_sc.split("-")[1] + "级"

        return location + "，" + date + "，" + wind_dir + "，" + wind_sc_str + "，" + temp

    # GetUvIndex和GetUvIndex_Followup的回答
    if current_intent in ["GetUvIndex", "GetUvIndex_Followup"]:
        if len(weather_list) > 1:
            temp = location
            for weather in weather_list:
                temp += convert_date(weather["date"]) + "，白天" + weather["condTxtD"] + "，夜晚" + weather["condTxtN"] \
                        + "，紫外线强度" + weather["uvIntensity"] + "。"
            return temp

        uv_index_int = int(uv_index)

        temp = ""
        if 0 <= uv_index_int <= 2:
            temp = "极弱，估计是太阳公公休假去了吧。"
        if 3 <= uv_index_int <= 4:
            temp = "较弱，阳光都被乌云遮住啦。"
        if 5 <= uv_index_int <= 6:
            temp = "较强，出门前记得涂点防晒霜哦。"
        if 7 <= uv_index_int <= 9:
            temp = "蛮强的，请做好充足的防晒措施，避免阳光直晒。"
        if 10 <= uv_index_int:
            temp = "超级强，请尽可能地待在阴凉处，晒伤了我会心疼的。"
        return location + "，" + date + "紫外线指数为" + uv_index + "，" + temp

    # GetThunder和GetThunder_Followup的回答
    if current_intent in ["GetThunder", "GetThunder_Followup"]:
        if len(weather_list) > 1:
            temp = location
            for weather in weather_list:
                temp += convert_date(weather["date"]) + "，白天" + weather["condTxtD"] + "，夜晚" + weather["condTxtN"]
            return temp
        if "雷" not in cond_txt_d + cond_txt_n:
            return location + date + "，白天" + cond_txt_d + "，夜晚" + cond_txt_n + "，放心吧，没有雷。"
        return location + date + "，白天" + cond_txt_d + "，夜晚" + cond_txt_n

    # GetTemperature和GetTemperature_Followup的回答
    if current_intent in ["GetTemperature", "GetTemperature_Followup"]:
        if len(weather_list) > 1:
            temp = location
            for weather in weather_list:
                temp += convert_date(weather["date"]) + "，白天" + weather["condTxtD"] + "，夜晚" + weather["condTxtN"] \
                        + "，最高气温" + weather["temperatureMax"] + "摄氏度" + "，最低气温" + weather[
                            "temperatureMin"] + "摄氏度。"
            return temp
        temp1 = location + date
        temp2 = convert_temperature(tmp_min) + "至" + convert_temperature(tmp_max)
        tmp_min_int = int(tmp_min)
        tmp_max_int = int(tmp_max)
        if tmp_min_int < 0:
            temp3 = ["把我都给冻傻了。", "你可别在室外呆太久哦。"]
            return temp1 + "，冷的跟冰窟窿一样，" + temp2 + "，" + temp3[random.randint(0, len(temp3) - 1)]
        if 0 <= tmp_min_int < 8:
            temp3 = ["记得穿秋裤哦。", "请多喝热水，注意保暖。"]
            return temp1 + "，天气寒冷，" + temp2 + "，" + temp3[random.randint(0, len(temp3) - 1)]
        if 8 <= tmp_max_int < 15:
            temp3 = ["带条围巾出门吧。", "很适合在被窝里睡懒觉。"]
            return temp1 + "，冷飕飕的，" + temp2 + "，" + temp3[random.randint(0, len(temp3) - 1)]
        if 15 <= tmp_max_int < 23:
            temp3 = ["约上朋友出去野餐吧。", "超级适合出门夜跑呢。"]
            return temp1 + "，温度适宜，" + temp2 + "，" + temp3[random.randint(0, len(temp3) - 1)]
        if 23 <= tmp_max_int < 30:
            temp3 = ["穿件透气的衬衣是不错的选择。", "切记不要贪凉，感冒了我会心疼的。"]
            return temp1 + "，有一丢丢热，" + temp2 + "，" + temp3[random.randint(0, len(temp3) - 1)]
        if 30 <= tmp_max_int:
            temp3 = ["请及时补充水分哦。", "注意防晒哦，晒伤了我会心疼的。"]
            return temp1 + "，热得跟火炉一样，" + temp2 + "，" + temp3[random.randint(0, len(temp3) - 1)]

    # GetSnow和GetSnow_Followup的回答
    if current_intent in ["GetSnow", "GetSnow_Followup"]:
        if len(weather_list) > 1:
            temp = location
            for weather in weather_list:
                temp += convert_date(weather["date"]) + "，白天" + weather["condTxtD"] + "，夜晚" + weather["condTxtN"]
                if "雪" not in weather["condTxtD"] + weather["condTxtN"]:
                    temp += "，放心吧，没有雪。"
                else:
                    temp += "记得戴手套哦。"
            return temp

        temp1 = location + date
        if "雪" not in cond_txt_d + cond_txt_n:
            return temp1 + "不下雪呢，" + convert_temperature(tmp_min) + "至" + convert_temperature(
                tmp_max) + "，我也盼着下雪呢。"

        if "雪" in cond_txt_d + cond_txt_n:
            temp3 = ["叫上朋友出去打雪仗吧。", "记得穿双防滑的鞋哦。", "记得戴手套哦。", "叫上朋友来家里吃火锅吧。"]
            return temp1 + "，" + convert_temperature(tmp_min) + "至" + convert_temperature(tmp_max) + temp3[
                random.randint(0, len(temp3) - 1)]
        return temp1 + "，" + convert_temperature(tmp_min) + "至" + convert_temperature(tmp_max)

    # GetRain和GetRain_Followup的回答
    if current_intent in ["GetRain", "GetRain_Followup"]:
        if len(weather_list) > 1:
            temp = location
            for weather in weather_list:
                temp += convert_date(weather["date"]) + "，白天" + weather["condTxtD"] + "，夜晚" + weather["condTxtN"]
                if "雨" not in weather["condTxtD"] + weather["condTxtN"]:
                    temp += "，放心吧，没有雨。"
                else:
                    temp += "出门记得带把伞哦。"
            return temp

        temp1 = location + date
        if cond_txt_d == cond_txt_n:
            temp2 = cond_txt_d
        else:
            temp2 = cond_txt_d + "转" + cond_txt_n

        if "雨" not in cond_txt_d + cond_txt_n:
            temp3 = ["放心出门玩吧。", "别宅在家里了，出门走走吧。"]
            return temp1 + "没有雨，" + convert_temperature(tmp_min) + "至" + convert_temperature(tmp_max) + "，" + temp3[
                random.randint(0, len(temp3) - 1)]

        if "雨" in cond_txt_d + cond_txt_n:
            temp3 = ["出门记得带把伞哦。", "这两天就别洗车咯。", "穿双防水的鞋吧。", "我都快发霉了。"]
            return temp1 + temp2 + convert_temperature(tmp_min) + "至" + convert_temperature(tmp_max) + "，" + temp3[
                random.randint(0, len(temp3) - 1)]
        return temp1 + temp2 + convert_temperature(tmp_min) + "至" + convert_temperature(tmp_max)

    # GetHumidity和GetHumidity_Followup的回答
    if current_intent in ["GetHumidity", "GetHumidity_Followup"]:
        temp = location
        for weather in weather_list:
            temp += convert_date(weather["date"]) + "，白天" + weather["condTxtD"] + "，夜晚" + weather[
                "condTxtN"] + "，湿度" + \
                    weather["humidity"] + "。"
        return temp

    # GetHailstone和GetHailstone_Followup的回答
    if current_intent in ["GetHailstone", "GetHailstone_Followup"]:
        temp = location
        for weather in weather_list:
            temp += convert_date(weather["date"]) + "，白天" + weather["condTxtD"] + "，夜晚" + weather["condTxtN"]
            if "雹" not in weather["condTxtD"] + weather["condTxtN"]:
                temp += "，放心吧，没有冰雹。"
        return temp


def run():
    if current_intent in ["WeatherForProvince"]:
        proResult["session"]["variables"]["status"] = {"key": "status", "value": "failure"}
        return "抱歉，只能根据城市查询天气。"
    if current_intent in ["GetPollution", "GetPollution_Followup"]:
        return get_pollution()
    if current_intent in ["GetWeather", "GetWeather_Followup",
                          "GetWind", "GetWind_Followup",
                          "GetUvIndex", "GetUvIndex_Followup",
                          "GetThunder", "GetThunder_Followup",
                          "GetTemperature", "GetTemperature_Followup",
                          "GetSnow", "GetSnow_Followup",
                          "GetRain", "GetRain_Followup",
                          "GetHumidity", "GetHumidity_Followup",
                          "GetHailstone", "GetHailstone_Followup"]:
        return get_weather()
    if current_intent in ["GetDressingIndex", "GetDressingIndex_Followup",
                          "GetExerciseIndex", "GetExerciseIndex_Followup",
                          "GetLivingIndex", "GetLivingIndex_Followup",
                          "GetWashingIndex", "GetWashingIndex_Followup"]:
        return get_lifestyle()
    proResult["session"]["variables"]["status"] = {"key": "status", "value": "failure"}
    return "天气很好~"


proResult["session"]["variables"]["status"] = {"key": "status", "value": "success"}
proResult["session"]["variables"]["answer"] = {"key": "answer", "value": run()}
