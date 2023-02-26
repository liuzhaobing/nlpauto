# -*- coding:utf-8 -*-
import json
import random

"""数据统一存储到story_list 结构如下：
同时会从story_list随机抽出一个故事 存储到now_story_info
story_list = [
    {
        "标题": "妙话后蜀主题春联",
        "中文故事": "",
        "主角": "",
        "国别": "",
        "寓意": "",
        "时间": "",
        "权重": "",
        "空间": "",
        "类型": "",
        "英文故事": ""
    }
]
"""


def return_slot_value(slot_name):
    if proResult["quresult"].__contains__("slots"):
        if proResult["quresult"]["slots"].__contains__(slot_name):
            if proResult["quresult"]["slots"][slot_name].__contains__("value"):
                return proResult["quresult"]["slots"][slot_name]["value"]
            elif proResult["quresult"]["slots"][slot_name].__contains__("origin"):
                return proResult["quresult"]["slots"][slot_name]["origin"]
    return None


def return_variable_value(var_name):
    if proResult["session"].__contains__("variables"):
        if proResult["session"]["variables"].__contains__(var_name):
            return proResult["session"]["variables"][var_name]["value"]
    return None


def story(story_title=None, story_tag=None, story_authorname=None, story_collection=None, story_type=None,
          skip=0, limit=10):
    """Story
    :param skip: 跳过多少个
    :param limit: 查询后 显示数量
    :param story_title:
    :param story_tag: tag涉及多值
    :param story_authorname:
    :param story_collection:
    :param story_type:
    :return:
    """

    if story_tag and "||" in story_tag:
        """与SDK约定 story_tag 传多值 以||分割"""
        story_tag = story_tag.split("||")
    elif story_tag:
        story_tag = [story_tag]

    # by title and tag
    if story_tag and story_title:
        query_conditions = [
            {
                "skip": skip,
                "limit": limit,
                "path_list": [
                    {
                        "src_ot": "storyName",
                        "src_symbol": "storyName",
                        "src_filter": [
                            {
                                "data_type": "string",
                                "filter_key": "name",
                                "vals": [
                                    story_title
                                ]
                            }
                        ],
                        "target_filter": [
                            {
                                "data_type": "string",
                                "filter_key": "name",
                                "vals": story_tag
                            }
                        ],
                        "target_ot": "storyTAG",
                        "target_symbol": "storyTAG",
                        "rel_concepts": [
                            "relation"
                        ],
                        "rel_filter": [],
                        "rel_symbol": "r1",
                        "steps": 0,
                        "direction": 2
                    }
                ],
                "recv_symbols": [
                    "storyName"
                ]
            }
        ]

    # by title and authorname
    elif story_authorname and story_title:
        query_conditions = [
            {
                "skip": skip,
                "limit": limit,
                "path_list": [
                    {
                        "src_ot": "storyName",
                        "src_symbol": "storyName",
                        "src_filter": [
                            {
                                "data_type": "string",
                                "filter_key": "name",
                                "vals": [
                                    story_title
                                ]
                            }
                        ],
                        "target_filter": [
                            {
                                "data_type": "string",
                                "filter_key": "name",
                                "vals": [
                                    story_authorname
                                ]
                            }
                        ],
                        "target_ot": "storyCreator",
                        "target_symbol": "storyCreator",
                        "rel_concepts": [
                            "relation"
                        ],
                        "rel_filter": [],
                        "rel_symbol": "r1",
                        "steps": 0,
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "storyName"
                ]
            }
        ]

    # by title and collection
    elif story_collection and story_title:
        query_conditions = [
            {
                "skip": skip,
                "limit": limit,
                "path_list": [
                    {
                        "src_ot": "storyName",
                        "src_symbol": "storyName",
                        "src_filter": [
                            {
                                "data_type": "string",
                                "filter_key": "name",
                                "vals": [
                                    story_title
                                ]
                            }
                        ],
                        "target_filter": [
                            {
                                "data_type": "string",
                                "filter_key": "name",
                                "vals": [
                                    story_collection
                                ]
                            }
                        ],
                        "target_ot": "storyColl",
                        "target_symbol": "storyColl",
                        "rel_concepts": [
                            "relation"
                        ],
                        "rel_filter": [],
                        "rel_symbol": "r1",
                        "steps": 0,
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "storyName"
                ]
            }
        ]

    # by title
    elif story_title:
        query_conditions = [
            {
                "skip": skip,
                "limit": limit,
                "path_list": [
                    {
                        "src_filter": [
                            {
                                "data_type": "string",
                                "filter_key": "name",
                                "vals": [
                                    story_title
                                ]
                            }
                        ],
                        "src_ot": "storyName",
                        "src_symbol": "storyName"
                    }
                ],
                "recv_symbols": [
                    "storyName"
                ]
            }
        ]

    # by tag
    elif story_tag:
        query_conditions = [
            {
                "skip": skip,
                "limit": limit,
                "path_list": [
                    {
                        "src_ot": "storyName",
                        "src_symbol": "storyName",
                        "src_filter": [],
                        "target_filter": [
                            {
                                "data_type": "string",
                                "filter_key": "name",
                                "vals": story_tag
                            }
                        ],
                        "target_ot": "storyTAG",
                        "target_symbol": "storyTAG",
                        "rel_concepts": [
                            "relation"
                        ],
                        "rel_filter": [],
                        "rel_symbol": "r1",
                        "steps": 0,
                        "direction": 2
                    }
                ],
                "recv_symbols": [
                    "storyName"
                ]
            }
        ]

    # by authorname
    elif story_authorname:
        query_conditions = [
            {
                "skip": skip,
                "limit": limit,
                "path_list": [
                    {
                        "src_ot": "storyName",
                        "src_symbol": "storyName",
                        "src_filter": [],
                        "target_filter": [
                            {
                                "data_type": "string",
                                "filter_key": "name",
                                "vals": [
                                    story_authorname
                                ]
                            }
                        ],
                        "target_ot": "storyCreator",
                        "target_symbol": "storyCreator",
                        "rel_concepts": [
                            "relation"
                        ],
                        "rel_filter": [],
                        "rel_symbol": "r1",
                        "steps": 0,
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "storyName"
                ]
            }
        ]

    # by collection
    elif story_collection:
        query_conditions = [
            {
                "skip": skip,
                "limit": limit,
                "path_list": [
                    {
                        "src_ot": "storyName",
                        "src_symbol": "storyName",
                        "src_filter": [],
                        "target_filter": [
                            {
                                "data_type": "string",
                                "filter_key": "name",
                                "vals": [
                                    story_collection
                                ]
                            }
                        ],
                        "target_ot": "storyColl",
                        "target_symbol": "storyColl",
                        "rel_concepts": [
                            "relation"
                        ],
                        "rel_filter": [],
                        "rel_symbol": "r1",
                        "steps": 0,
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "storyName"
                ]
            }
        ]

    # 兜底 不带任何槽位
    else:
        query_conditions = [
            {
                "skip": skip,
                "limit": limit,
                "path_list": [
                    {
                        "src_filter": [],
                        "src_ot": "storyName",
                        "src_symbol": "storyName"
                    }
                ],
                "recv_symbols": [
                    "storyName"
                ]
            }
        ]

    if story_type:
        query_conditions[0]["path_list"][0]["src_filter"].append({
            "data_type": "string",
            "filter_key": "类型",
            "multi_attr": True,
            "vals": [
                story_type
            ]
        })
    return query_conditions


def return_story():
    """从获取到的故事列表中随机返回n个"""
    proResult["session"]["variables"]["success"] = {"key": "success", "value": "false"}
    story_list = []
    api_kg = json.loads(proResult["session"]["variables"]["api_kg"]["value"])
    """接口报错 可能没查到 就表示没有数据"""
    if api_kg.__contains__("msg"):
        return story_list

    """从返回信息中循环取到所有诗句及其相关信息 存储到poem_list"""
    for data in api_kg["datas"]:
        if data["row"].__contains__("storyName"):
            if data["row"]["storyName"].__contains__("node"):
                story_title = data["row"]["storyName"]["node"]["vertexs"][0]["name"]
                a_story_info = {"标题": story_title}
                for x in data["row"]["storyName"]["node"]["vertexs"]:
                    info = x["prop_map"]
                    a_story_info = dict(a_story_info, **info)
                """这里将多个类型抽出来 放一个到键[故事类型]中 提供给后续回复节点使用"""
                if a_story_info.__contains__("类型"):
                    tp = a_story_info["类型"]
                    if tp and "|" in tp:
                        tps = tp.split("|")
                        p = tps[random.randint(0, len(tps) - 1)]
                        a_story_info["故事类型"] = p
                        user_input_story_type = return_slot_value("story_tag")
                        if user_input_story_type and user_input_story_type in tps:
                            a_story_info["故事类型"] = user_input_story_type
                    else:
                        a_story_info["故事类型"] = tp
                else:
                    a_story_info["故事类型"] = ""
                story_list.append(a_story_info)

    if story_list:
        proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
        proResult["session"]["variables"]["story_list"] = {"key": "story_list",
                                                           "value": json.dumps(story_list, ensure_ascii=False)}

        """随机抽一个故事"""
        now_story_info = story_list[random.randint(0, len(story_list) - 1)]
        proResult["session"]["variables"]["now_story_info"] = {"key": "now_story_info",
                                                               "value": json.dumps(now_story_info, ensure_ascii=False)}
        return now_story_info
    return story_list


def check_if_one_available():
    """机器人推荐了几个故事后 用户输入 检查用户select的这个是否存在"""
    proResult["session"]["variables"]["success"] = {"key": "success", "value": "false"}

    now_story_info = {}
    if proResult["session"]["variables"].__contains__("story_list"):
        story_list = json.loads(proResult["session"]["variables"]["story_list"]["value"])
        index1 = return_slot_value("index1")
        index2 = return_slot_value("index2")
        story_title = return_slot_value("story_title")
        story_title1 = return_slot_value("story_title1")
        if index1:
            if int(index1) - 1 >= len(story_list):
                return now_story_info
            now_story_info = story_list[int(index1) - 1]
            proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
            proResult["session"]["variables"]["now_story_info"] = {"key": "now_story_info",
                                                                   "value": json.dumps(now_story_info,
                                                                                       ensure_ascii=False)}
            return now_story_info

        elif story_title:
            for s in story_list:
                if s["标题"] == story_title:
                    proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
                    proResult["session"]["variables"]["now_story_info"] = {"key": "now_story_info",
                                                                           "value": json.dumps(s,
                                                                                               ensure_ascii=False)}
                    return now_story_info
            """现在只判断用户输入在不在机器人推荐列表 如果不在就没找到 实际应该去图谱再查一次 后面再实现"""
            query_conditions = story(story_title=story_title)
            proResult["session"]["variables"]["query_conditions"] = {"key": "query_conditions",
                                                                     "value": json.dumps(query_conditions,
                                                                                         ensure_ascii=False)}
            proResult["session"]["variables"]["success"] = {"key": "success", "value": "again"}
            return now_story_info
    return now_story_info


def modify_query_conditions():
    now_round = 0
    limit = 20
    current_intent = proResult["quresult"]["intent"]
    if proResult["session"].__contains__("variables"):
        if proResult["session"]["variables"].__contains__("limit"):
            limit = int(proResult["session"]["variables"]["limit"]["value"])
        else:
            proResult["session"]["variables"]["limit"] = {"key": "limit", "value": str(limit)}

        if proResult["session"]["variables"].__contains__("now_round"):
            now_round = int(proResult["session"]["variables"]["now_round"]["value"])
        else:
            proResult["session"]["variables"]["now_round"] = {"key": "now_round", "value": str(now_round)}
    else:
        proResult["session"]["variables"] = {
            "now_round": {"key": "now_round", "value": str(now_round)},
            "limit": {"key": "limit", "value": str(limit)}
        }

    if current_intent == "Story":
        return story(story_title=return_slot_value("story_title"),
                     story_collection=return_slot_value("story_collection"),
                     story_authorname=return_slot_value("story_authorname"),
                     story_tag=return_slot_value("story_tag"),
                     story_type=return_slot_value("story_type"))

    if current_intent == "CanStory":
        return story(skip=now_round * limit, limit=limit)

    if current_intent == "StoryAnother":
        return story(skip=now_round * limit, limit=limit)


proResult["session"]["variables"]["query_conditions"] = {"key": "query_conditions",
                                                         "value": json.dumps(modify_query_conditions(),
                                                                             ensure_ascii=False)}
