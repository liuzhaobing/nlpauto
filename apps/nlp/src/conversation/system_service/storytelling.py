# -*- coding:utf-8 -*-
import json

proResult = {"quresult": {"domain_id": 191, "domain": "storytelling", "intent": "GetByPerformer",
                          "slots": {
                              "performer": {"key": "performer", "value": "单田芳", "origin": "单田芳",
                                            "type": "sys.entity.storytelling_performer"}}},

             "session": {"state": "ineq70n2sr", "variables": {
                 "api_media": {"key": "api_media",
                               "value": "{\"medias\":[{\"id\":50,\"title\":\"薛家将\",\"type\":[\"audio\"],\"audioUrl\":\"https://dev-s3.harix.iamidata.com/crss-smartomp-fit/cms/zh-CN/20210903/173940/jpzXoFx5.mp3?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K\\u0026Expires=4743019496\\u0026Signature=lPRtLCfDo7CSSMwZ2F368H3KeEc%3D\",\"author\":\"单田芳\"}],\"total\":1}"},
                 "default_index": {"key": "default_index", "value": "0"},
                 "input_index": {"key": "input_index", "value": ""},
                 "input_performer": {"key": "input_performer", "value": "单田芳"},
                 "input_title": {"key": "input_title", "value": ""}, "now_index": {"key": "now_index", "value": "0"},
                 "now_title": {"key": "now_title", "value": ""}}, "slots": {
                 "performer": {"key": "performer", "value": "单田芳", "origin": "单田芳",
                               "type": "sys.entity.storytelling_performer", "deleted": False, "inherit": True}}},
             "extra": {
                 "api_info": {"url": "http://mmpp-api-server:8087/v1/cms/search_media",
                              "params": {"author": "单田芳", "category": "评书", "isRandom": "", "title": "",
                                         "type": "",
                                         "without": ""},
                              "response": "{\"medias\":[{\"id\":50,\"title\":\"薛家将\",\"type\":[\"audio\"],\"audioUrl\":\"https://dev-s3.harix.iamidata.com/crss-smartomp-fit/cms/zh-CN/20210903/173940/jpzXoFx5.mp3?AWSAccessKeyId=0A1E0R8T5JSEY9UDTQ9K\\u0026Expires=4743019496\\u0026Signature=lPRtLCfDo7CSSMwZ2F368H3KeEc%3D\",\"author\":\"单田芳\"}],\"total\":1}",
                              "http_code": 200}}}


def select_index():
    """"""
    if proResult["session"]["variables"].__contains__("input_index"):
        input_index = proResult["session"]["variables"]["input_index"]["value"]
    else:
        input_index = ""

    if proResult["session"]["variables"].__contains__("change_index"):
        change_index = proResult["session"]["variables"]["change_index"]["value"]
    else:
        change_index = ""

    if proResult["session"]["variables"].__contains__("now_index"):
        now_index = proResult["session"]["variables"]["now_index"]["value"]
    else:
        now_index = ""

    if input_index:
        """若新输入指定集数 则将now_index更新为指定集数 然后将输入集数更新为空"""
        proResult["session"]["variables"]["input_index"] = {"key": "input_index", "value": ""}
        return str(int(input_index) - 1)

    if change_index:
        """若选择上一集或下一集 将now_index增减 然后将上下集更新为空"""
        if not now_index:
            now_index = "0"
        now_index = str(int(now_index) + int(change_index))
        proResult["session"]["variables"]["change_index"] = {"key": "change_index", "value": ""}
        return now_index

    if now_index:
        """若既没有指定选集 也没有指定上下集 则返回当前集数"""
        return now_index

    """若没有当前集数 则默认第0集"""
    return "0"


def check_length():
    """看下即将播放的集数是否超出范围"""
    now_index = proResult["session"]["variables"]["now_index"]["value"]
    api_media = proResult["session"]["variables"]["api_media"]["value"]
    if len(api_media["medias"]) - 1 < int(now_index):
        return True
    return False


def get_media_by_now_index():
    """通过index 取到对应的媒体资源对象"""
    api_media = proResult["session"]["variables"]["api_media"]["value"]
    if len(api_media) < 10:
        """若找到的资源为空"""
        proResult["session"]["variables"]["now_audio"] = {"key": "now_audio", "value": ""}
        proResult["session"]["variables"]["now_answer"] = {"key": "now_answer",
                                                           "value": "不好意思，未找到您想要的资源"}
        return
    medias = json.loads(api_media)["medias"]
    now_index = proResult["session"]["variables"]["now_index"]["value"]
    if len(medias) <= int(now_index):
        """若找到的资源只有n集 不够now_index那么多集"""
        proResult["session"]["variables"]["now_audio"] = {"key": "now_audio", "value": ""}
        proResult["session"]["variables"]["now_answer"] = {"key": "now_answer",
                                                           "value": "不好意思，未找到您想要的资源"}
        return

    now_media = medias[int(now_index)]
    proResult["session"]["variables"]["now_media"] = {"key": "now_media",
                                                      "value": json.dumps(now_media, ensure_ascii=False)}
    now_title = now_media["title"]
    now_performer = now_media["author"]
    now_audio = now_media["audioUrl"]
    proResult["session"]["variables"]["now_title"] = {"key": "now_title", "value": now_title}
    proResult["session"]["variables"]["now_performer"] = {"key": "now_performer", "value": now_performer}
    proResult["session"]["variables"]["now_audio"] = {"key": "now_audio", "value": now_audio}
    proResult["session"]["variables"]["now_answer"] = {"key": "now_answer",
                                                       "value": f"为您播放{now_performer}的评书{now_title}"}


get_media_by_now_index()

proResult["session"]["variables"]["now_index"] = {"key": "now_index", "value": select_index()}
