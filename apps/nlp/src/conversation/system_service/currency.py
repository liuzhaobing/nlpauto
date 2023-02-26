# -*- coding:utf-8 -*-
proResult = {"quresult": {"domain_id": 80, "domain": "currency", "intent": "GetCurrentcy", "slots": {
    "fcurrentcy": {"key": "fcurrentcy", "value": "USD", "origin": "美元", "type": "sys.entity.fcurrency"}}},
             "session": None}


def set_cny():
    if proResult["quresult"]["slots"].__contains__("fcurrentcy"):
        input_fcurrentcy = True
    else:
        input_fcurrentcy = False
    if proResult["quresult"]["slots"].__contains__("tcurrentcy"):
        input_tcurrentcy = True
    else:
        input_tcurrentcy = False

    proResult["session"]["variables"] = {"currency": {"key": "currency", "value": ""}}

    if input_fcurrentcy and not input_tcurrentcy:
        proResult["session"]["variables"]["input_tcurrentcy"]["value"] = {"key": "input_tcurrentcy", "value": "CNY"}
        proResult["session"]["variables"]["input_tcurrentcy_origin"] = {"key": "input_tcurrentcy_origin", "value": "元"}

        fcurrentcy_origin = proResult["quresult"]["slots"]["fcurrentcy"]["origin"]
        fcurrentcy_value = proResult["quresult"]["slots"]["fcurrentcy"]["value"]
        proResult["session"]["variables"]["input_fcurrentcy"]["value"] = {"key": "input_fcurrentcy",
                                                                          "value": fcurrentcy_value}
        proResult["session"]["variables"]["input_fcurrentcy_origin"] = {"key": "input_fcurrentcy_origin",
                                                                        "value": fcurrentcy_origin}

    if input_tcurrentcy and not input_fcurrentcy:
        proResult["session"]["variables"]["input_fcurrentcy"]["value"] = {"key": "input_fcurrentcy", "value": "CNY"}
        proResult["session"]["variables"]["input_fcurrentcy_origin"] = {"key": "input_fcurrentcy_origin", "value": "元"}

        tcurrentcy_origin = proResult["quresult"]["slots"]["tcurrentcy"]["origin"]
        tcurrentcy_value = proResult["quresult"]["slots"]["tcurrentcy"]["value"]
        proResult["session"]["variables"]["input_tcurrentcy"]["value"] = {"key": "input_tcurrentcy",
                                                                          "value": tcurrentcy_value}
        proResult["session"]["variables"]["input_tcurrentcy_origin"] = {"key": "input_tcurrentcy_origin",
                                                                        "value": tcurrentcy_origin}


set_cny()
