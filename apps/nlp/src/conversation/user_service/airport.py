# -*- coding:utf-8 -*-
"""
机场值机相关多轮
"""
related_answer = [
    {
        "title": "青岛航空",
        "content": "您好，青岛航空在四层K岛和B1层W岛办理手续。"
    },
    {
        "title": "成都航空",
        "content": "您好，成都航空在四层K岛和B1层W岛办理手续，再见。"
    },
    {
        "title": "北部湾航空",
        "content": "您好，北部湾航空在四层K岛和B1层W岛办理手续。"
    },
    {
        "title": "天津航空",
        "content": "您好，天津航空在四层K岛和B1层W岛办理手续。"
    },
    {
        "title": "西藏航空",
        "content": "您好，西藏航空在四层K岛和B1层W岛办理手续。"
    },
    {
        "title": "北部湾航空",
        "content": "您好，北部湾航空在四层K岛和B1层W岛办理手续。"
    },
    {
        "title": "天津航空",
        "content": "您好，天津航空在四层K岛和B1层W岛办理手续。"
    },
    {
        "title": "西藏航空",
        "content": "您好，西藏航空在四层K岛和B1层W岛办理手续。"
    },
    {
        "title": "山东航空",
        "content": "您好，山东航空在四层K岛和B1层W岛办理手续。"
    },
    {
        "title": "昆明航空",
        "content": "您好，昆明航空在四层K岛和B1层W岛办理手续。"
    },
    {
        "title": "江西航空",
        "content": "您好，江西航空在四层K岛和B1层W岛办理手续。"
    },
    {
        "title": "重庆航空",
        "content": "您好，重庆航空在四层B岛和B1层U岛办理手续。"
    },
    {
        "title": "吉祥航空",
        "content": "您好，吉祥航空在四层K岛和B1层W岛办理手续。"
    },
    {
        "title": "首都航空",
        "content": "您好，首都航空在四层K岛和B1层W岛办理手续。"
    },
    {
        "title": "东海航空",
        "content": "您好，东海航空在四层K区和B1层W区办理值机手续。"
    },
    {
        "title": "厦门航空",
        "content": "您好，厦门航空在四层B岛和B1层U岛办理手续。"
    },
    {
        "title": "东方航空",
        "content": "您好，东方航空经济舱在四层H岛和B1层W岛办理手续。高端旅客请前往三层最东侧办理手续。"
    },
    {
        "title": "上海航空",
        "content": "您好，上海航空经济舱在四层H岛、B1层W岛，高舱值机区位于三层东侧东航专享值机区。"
    },
    {
        "title": "河北航空",
        "content": "您好，实际承运人是河北航空在四层K区和B1层W区办理值机手续。"
    },
    {
        "title": "山东航空",
        "content": "您好，山东航空在四层K岛和B1层W岛办理手续。"
    }
]


def get_answer():
    hangkong = proResult["session"]["variables"]["hangkong"]["value"]
    for h in related_answer:
        if h["title"] == hangkong:
            return h["content"]


proResult["session"]["variables"]["answer"] = {"key": "answer", "value": get_answer()}
