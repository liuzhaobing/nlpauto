# -*- coding:utf-8 -*-
import json
import random


def get_theme():
    """get a theme from theme list"""
    theme_list = json.loads(proResult["session"]["variables"]["theme_list"]["value"])
    if len(theme_list) > 0:
        now_theme = theme_list[random.randint(0, len(theme_list) - 1)]
        theme_list.remove(now_theme)
        proResult["session"]["variables"]["theme_list"]["value"] = json.dumps(theme_list, ensure_ascii=False)
        return now_theme
    else:
        return "None"


def get_one_poetry_from_pool():
    """get one poetry from themed-poetry-pool"""

    def return_the_longest_one_from_list(li):
        """return the longest one from list"""
        return max(li, key=len)

    poetries = json.loads(proResult["session"]["variables"]["poetries"]["value"])  # 未使用的poetry
    if proResult["session"]["variables"].__contains__("used_poetries"):
        used_poetries = json.loads(proResult["session"]["variables"]["used_poetries"]["value"])  # 已使用的poetry
    else:
        used_poetries = []

    if poetries:  # 如果资源池还有诗
        """解决诗句随机性问题"""
        now_poetry = poetries[random.randint(0, len(poetries) - 1)]
        poetries.remove(now_poetry)
        # now_poetry = poetries.pop()
        title = now_poetry["itemname"]  # 实例名
        content = now_poetry["syn"]  # 同义词

        if content:
            now_poetry_content = return_the_longest_one_from_list(content.split("&&"))  # 同义词切割成列表，从中选出最长的那个
        else:
            now_poetry_content = title

        proResult["session"]["variables"]["now_poetry_content"] = {"key": "now_poetry_content",
                                                                   "value": now_poetry_content}

        """store the unused poetries to pool"""
        proResult["session"]["variables"]["poetries"] = {"key": "poetries",
                                                         "value": json.dumps(poetries, ensure_ascii=False)}

        proResult["session"]["variables"]["now_poetry"] = {"key": "now_poetry",
                                                           "value": json.dumps(now_poetry, ensure_ascii=False)}

        used_poetries.append(now_poetry)
        proResult["session"]["variables"]["used_poetries"] = {"key": "used_poetries",
                                                              "value": json.dumps(used_poetries, ensure_ascii=False)}
        return True

    else:
        return False


def check_user_answer():
    """优先级：不是>不含>已用过 """
    if proResult["quresult"]["slots"].__contains__("content"):
        current_answer = proResult["quresult"]["slots"]["content"]["value"]
    else:
        return "not poetry"

    current_theme = proResult["session"]["variables"]["now_theme"]["value"]

    if current_theme not in current_answer and current_theme not in proResult["quresult"]["slots"]["content"]["origin"]:
        return "wrong poetry"

    used_poetries = json.loads(proResult["session"]["variables"]["used_poetries"]["value"])
    if current_answer in str(used_poetries):
        return "used poetry"

    poetries = json.loads(proResult["session"]["variables"]["poetries"]["value"])  # 未使用的poetry
    for poetry in poetries:
        # if current_answer in poetry["syn"]:
        if current_answer in poetry["itemname"]:  #
            """
            如果用syn会有问题，解决遍历时提前取错的问题 用itemname
            老去秋风吹我恶  老去秋风吹我恶&&老去秋风吹我恶，梦回寒月照人孤
            梦回寒月照人孤  梦回寒月照人孤&&老去秋风吹我恶，梦回寒月照人孤
            """
            poetries.remove(poetry)
            proResult["session"]["variables"]["poetries"] = {"key": "poetries",
                                                             "value": json.dumps(poetries, ensure_ascii=False)}
            used_poetries.append(poetry)
            proResult["session"]["variables"]["used_poetries"] = {"key": "used_poetries",
                                                                  "value": json.dumps(used_poetries,
                                                                                      ensure_ascii=False)}
            return "right poetry"
    return "not find poetry"


def duplicate_poetries():
    """按照最长的同义词进行去重"""
    poetries = json.loads(proResult["session"]["variables"]["poetries"]["value"])  # 未使用的poetry
    current_theme = proResult["session"]["variables"]["now_theme"]["value"]
    for poetry in poetries:
        if current_theme not in poetry["itemname"] or current_theme not in poetry["syn"]:
            poetries.remove(poetry)
    proResult["session"]["variables"]["poetries"]["value"] = json.dumps(poetries, ensure_ascii=False)
    return poetries


def check_wrong_times():
    """判断错误次数是否达到阈值"""
    wrong_count = proResult["session"]["variables"]["wrong_count"]["value"]
    max_wrong_count = proResult["session"]["variables"]["max_wrong_count"]["value"]
    if int(wrong_count) >= int(max_wrong_count):
        proResult["success"] = True
    else:
        proResult["success"] = False
    return int(wrong_count)

