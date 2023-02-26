# -*- coding:utf-8 -*-
import datetime

proResult = {"quresult": {
    "domain_id": 3446,
    "domain": "ConversationWeather",
    "intent": "GetRain",
    "slots": {"date-duration": {"key": "date-duration", "value": "2022-08-08/2022-08-09", "origin": "最近",
                                "type": "sys.date-duration"}},
    "request_params": {"Default": "我要看最近的天气预报", "agentid": "1522", "devicetype": "ginger",
                       "envinfo": "{\"devicetype\":\"\",\"timezone\":\"UTC+8\"}",
                       "filter_query": "我要看最近的天气预报", "lang": "ZH", "position": "104.061;30.5444",
                       "query": "我要看最近的天气预报", "robotid": "5C1AEC03573747D",
                       "sessionid": "testAnno@@cloudminds", "tenantcode": "cloudminds",
                       "traceid": "d361e0c0-8b5e-4a20-8f7a-5430aac3d6f4", "version": "v3"}},
    "session": {
        "state": "cds8fg969h",
        "variables": {"input_city": {"key": "input_city", "value": ""},
                      "input_date": {"key": "input_date", "value": ""},
                      "input_duration": {"key": "input_duration", "value": "2022-09-06/2022-09-13"},
                      "input_position": {"key": "input_position", "value": ""}}},
    "extra": {
        "api_info": {"url": "http://sxct.region-dev-1.service.iamidata.com:31123/v1/weather/days",
                     "params": {"api": "", "city": "", "date": "", "datetime": "",
                                "duration": "2022-08-08/2022-08-09", "position": "", "time": ""},
                     "response": "{\"weather\":[{\"date\":\"2022-08-09\",\"humidity\":\"90\",\"temperatureMax\":\"27\",\"temperatureMin\":\"20\",\"windDirection\":\"西北风\",\"windSpeed\":\"1-2\",\"uvIntensity\":\"9\",\"condTxtD\":\"多云\",\"condTxtN\":\"晴\",\"location\":\"北京\"}]}",
                     # "response": "{\"weather\":[{\"date\":\"2022-08-08\",\"humidity\":\"94\",\"temperatureMax\":\"28\",\"temperatureMin\":\"22\",\"windDirection\":\"东北风\",\"windSpeed\":\"1-2\",\"uvIntensity\":\"2\",\"condTxtD\":\"多云\",\"condTxtN\":\"小雨\",\"location\":\"北京\"},{\"date\":\"2022-08-09\",\"humidity\":\"90\",\"temperatureMax\":\"27\",\"temperatureMin\":\"20\",\"windDirection\":\"西北风\",\"windSpeed\":\"1-2\",\"uvIntensity\":\"9\",\"condTxtD\":\"多云\",\"condTxtN\":\"晴\",\"location\":\"北京\"}]}",
                     "http_code": 200}}}


def check_str_contain_chinese(string):
    """判断字符串中是否含有中文字符"""
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def check_data_duration_string():
    """check invalidation of date and duration, service api support only recent a week weather info"""
    duration = proResult["session"]["variables"]["input_duration"]["value"]
    date = proResult["session"]["variables"]["input_date"]["value"]
    if check_str_contain_chinese(date) or check_str_contain_chinese(duration):
        return "请告诉我具体查询的日子吧"

    is_changed = False
    now = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')

    if len(duration) == 21:
        duration_li = duration.split("/")
        date_1 = datetime.datetime.strptime(duration_li[0], '%Y-%m-%d')
        date_2 = datetime.datetime.strptime(duration_li[1], '%Y-%m-%d')

        if date_1 >= date_2:
            is_changed = True
            return is_changed

        """
        service api support only recent a week weather info (total 6 days)
        but SDK returns recent a week string (total 7 days)
        """
        if duration_li[0] == now.strftime('%Y-%m-%d') and \
                duration_li[1] == (now + datetime.timedelta(days=7)).strftime('%Y-%m-%d'):
            duration_li[1] = (now + datetime.timedelta(days=6)).strftime('%Y-%m-%d')
            proResult["session"]["variables"]["input_duration"]["value"] = "/".join(duration_li)
            is_changed = False
            return is_changed

        if (date_2 - date_1).days >= 7 or (date_2 - now).days >= 7:
            is_changed = True
            return is_changed

        if (date_1 - now).days >= 6:
            is_changed = True
            return is_changed

        return is_changed

    if len(date) == 10:
        date_1 = datetime.datetime.strptime(date, '%Y-%m-%d')
        count_now_to_end = date_1 - now
        if count_now_to_end.days >= 7:
            is_changed = True
            return is_changed

    return is_changed


proResult["success"] = check_data_duration_string()
