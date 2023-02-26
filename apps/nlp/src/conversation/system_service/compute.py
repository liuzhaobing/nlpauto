# -*- coding:utf-8 -*-


slot_compute = "compute"

if proResult["quresult"].__contains__("request_params"):
    if proResult["quresult"]["request_params"].__contains__("query"):
        query = proResult["quresult"]["request_params"]["query"]

if proResult["quresult"].__contains__("slots"):
    if proResult["quresult"]["slots"].__contains__(slot_compute):
        result = proResult["quresult"]["slots"][slot_compute]["value"]


def compute():
    if "分之" in query:
        return "告诉你个秘密，我的数学是体育老师教的"
    else:
        return "等于" + result


proResult["answers"] = [compute()]
