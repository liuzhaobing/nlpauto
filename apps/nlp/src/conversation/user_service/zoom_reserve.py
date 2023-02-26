# -*- coding:utf-8 -*-
"""
来酷项目 预定会议室多轮
"""


def redefine_time():
    start_time_origin, start_time_after, signal = "", "", ""
    if proResult["session"]["slots"].__contains__("start_time"):
        signal = "session"
    elif proResult["quresult"]["slots"].__contains__("start_time"):
        signal = "quresult"

    if signal == "":
        return

    start_time_origin = proResult[signal]["slots"]["start_time"]["origin"]
    start_time_after = proResult[signal]["slots"]["start_time"]["value"]

    if "下" in start_time_origin or "晚" in start_time_origin or "中" in start_time_origin:
        hour = int(start_time_after[:2])
        if hour < 12:
            hour += 12
        if hour == 12:
            hour = "00"

        proResult[signal]["slots"]["start_time"]["value"] = str(hour) + start_time_after[2:]

    return


redefine_time()
