# -*- coding:utf-8 -*-
import json
import random
import re

"""
数据都存储到变量 now_poem_info = 
{"上一句": "", 
"下一句": "", 
"这一句": "", 
"享年": "", 
"卒年": "", 
"号": "", 
"字": "", 
"性别": "", 
"斋号": "", 
"权重": "", 
"民族": "", 
"生年": "", 
"社会身份": "", 
"简介": "", 
"序言": "", 
"情感": "", 
"正文": "君不见，黄河之水天上来，奔流到海不复回。君不见，高堂明镜悲白发，朝如青丝暮成雪。人生得意须尽欢，莫使金樽空对月。天生我材必有用，千金散尽还复来。烹羊宰牛且为乐，会须一饮三百杯。岑夫子，丹丘生，将进酒，杯莫停。与君歌一曲，请君为我倾耳听。古来圣贤皆寂寞，惟有饮者留其名。陈王昔时宴平乐，斗酒十千恣欢谑。主人何为言少钱，径须沽取对君酌。五花马，千金裘，呼儿将出换美酒，与尔同销万古愁。", 
"背景": "",
"英文译文": "", 
"译文": "你难道看不见那黄河之水从天上奔腾而来，波涛翻滚直奔东海，再也没有回来。你没见那年迈的父母，对着明镜感叹自己的白发。年轻时的满头青丝如今已是雪白一片。(喻意青春短暂）（所以）人生得意之时就应当纵情欢乐，不要让这金杯无酒空对明月。每个人的出生都一定有自己的价值和意义，黄金千两（就算）一挥而尽，它也还是能够再得来。我们烹羊宰牛姑且作乐，（今天）一次性痛快地饮三百杯也不为多！岑夫子和丹丘生啊！快喝酒吧！不要停下来。让我来为你们高歌一曲，请你们为我倾耳细听：整天吃山珍海味的豪华生活有何珍贵，只希望醉生梦死而不愿清醒。自古以来圣贤无不是冷落寂寞的，只有那会喝酒的人才能够留传美名。陈王曹植当年宴设平乐观的事迹你可知道，斗酒万千也豪饮，让宾主尽情欢乐。主人呀，你为何说我的钱不多？只管买酒来让我们一起痛饮。那些什么名贵的五花良马，昂贵的千金狐裘，把你的小儿喊出来，都让他拿去换美酒来吧。让我们一起来消除这无穷无尽的万古长愁！", 
"题目": "将进酒", 
"作者": "李白"}
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
    if proResult["session"]:
        if proResult["session"].__contains__("variables"):
            if proResult["session"]["variables"].__contains__(var_name):
                return proResult["session"]["variables"][var_name]["value"]
    return None


def get_next_phrases(poem_content=None, steps=5):
    """GetNextPhrases 从当前句向下查steps次，拼装answer时以句号结尾。
    :param poem_content:
    :param steps:
    :return: [p poet poem verse]
    """
    if poem_content and "||" in poem_content:
        """content可能有多段 这里默认SDK是已经排序给过来的 就去取最后一段"""
        poem_content = poem_content.split("||")[-1]
    query_condition = [
        {
            "limit": 100,
            "path_list": [
                {
                    "src_filter": [
                        {
                            "data_type": "string",
                            "filter_key": "name",
                            "vals": [
                                poem_content
                            ]
                        }
                    ],
                    "rel_concepts": [
                        "relation"
                    ],
                    "rel_filter": [
                        {
                            "data_type": "string",
                            "filter_key": "name",
                            "vals": [
                                "出处"
                            ]
                        }
                    ],
                    "rel_symbol": "r1",
                    "src_ot": "verse",
                    "src_symbol": "verse",
                    "target_filter": [],
                    "target_ot": "poem",
                    "target_symbol": "poem"
                },
                {
                    "direction": 0,
                    "optional": 1,
                    "rel_concepts": [
                        "relation"
                    ],
                    "rel_filter": [
                        {
                            "data_type": "string",
                            "filter_key": "name",
                            "vals": [
                                "作者"
                            ]
                        }
                    ],
                    "rel_symbol": "r3",
                    "src_ot": "poem",
                    "src_symbol": "poem",
                    "target_filter": [],
                    "target_ot": "poet",
                    "target_symbol": "poet"
                },
                {
                    "direction": 0,
                    "optional": 1,
                    "path_symbol": "p",
                    "rel_concepts": [
                        "relation"
                    ],
                    "rel_filter": [
                        {
                            "data_type": "string",
                            "filter_key": "name",
                            "vals": [
                                "下一句"
                            ]
                        }
                    ],
                    "rel_symbol": "r2",
                    "src_filter": [
                        {
                            "data_type": "string",
                            "filter_key": "name",
                            "vals": [
                                poem_content
                            ]
                        }
                    ],
                    "src_ot": "verse",
                    "src_symbol": "verse",
                    "steps": steps,
                    "target_filter": [],
                    "target_ot": "",
                    "target_symbol": "v4"
                }
            ],
            "recv_symbols": [
                "p",
                "poem",
                "poet",
                "verse"
            ]
        }
    ]
    return query_condition


def return_get_next_phrases(break_point=True):
    """GetNextPhrases 查询到n步后 组装回复的诗句 以句号终止
    :param break_point: true只返回后面一句 false返回后面所有句
    :return: [下一句 poet poem]
    """
    proResult["session"]["variables"]["success"] = {"key": "success", "value": "false"}
    now_poem_info = {"历史意图": "get_next_phrases"}
    api_kg = json.loads(proResult["session"]["variables"]["api_kg"]["value"])

    """接口报错 可能没查到 就表示没有下一句"""
    if api_kg.__contains__("msg"):
        return now_poem_info

    """这里先默认取最后一个 不知道后面会不会有问题"""
    data = api_kg["datas"][-1]

    if data["row"].__contains__("poem"):
        if data["row"]["poem"].__contains__("node"):
            poem_name = data["row"]["poem"]["node"]["vertexs"][0]["name"]
            poem_info = data["row"]["poem"]["node"]["vertexs"][0]["prop_map"]
            now_poem_info = dict(poem_info, **now_poem_info)
            now_poem_info["题目"] = poem_name

    if data["row"].__contains__("poet"):
        if data["row"]["poet"].__contains__("node"):
            poet_name = data["row"]["poet"]["node"]["vertexs"][0]["name"]
            poet_info = data["row"]["poet"]["node"]["vertexs"][0]["prop_map"]
            now_poem_info = dict(poet_info, **now_poem_info)
            now_poem_info["作者"] = poet_name

    if data["row"]["p"].__contains__("path"):
        steps = data["row"]["p"]["path"]["steps"]

        next_phrases = ""
        for step in steps:
            text = step["dst"]["vertexs"][0]["name"]
            next_phrases += text
            if break_point and "。" in text:
                break

        now_poem_info["下一句"] = next_phrases
        now_poem_info["这一句"] = data["row"]["p"]["path"]["src"]["vertexs"][0]["name"]

        """只有查到了下一句内容 才success=true 其他场景都算没找到下一句"""
        proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
        proResult["session"]["variables"]["now_poem_info"] = {"key": "now_poem_info",
                                                              "value": json.dumps(now_poem_info,
                                                                                  ensure_ascii=False)}
        return now_poem_info

    if data["row"].__contains__("verse"):
        if data["row"]["verse"].__contains__("node"):
            now_poem_info["这一句"] = data["row"]["verse"]["node"]["vertexs"][0]["name"]
            proResult["session"]["variables"]["now_poem_info"] = {"key": "now_poem_info",
                                                                  "value": json.dumps(now_poem_info,
                                                                                      ensure_ascii=False)}
    return now_poem_info


def get_next_phrases_again(poem_content, steps=100):
    """GetNextPhrasesAgain 再一次获取下一句，直接输出剩余全文
    :param poem_content:
    :param steps:
    :return:
    """
    return get_next_phrases(poem_content, steps)


def return_get_next_phrases_again(break_point=False):
    """GetNextPhrasesAgain 返回剩余全部内容"""
    return return_get_next_phrases(break_point=break_point)


def get_one_poetry_new(poem_author=None, poem_type=None, poem_anthology=None,
                       poem_category=None, poem_dynasty=None, poem_emotion=None,
                       poem_faction=None, poem_genre=None, poem_theme=None,
                       poem_expression=None, poem_titleGroup=None, poem_reference=None,
                       poem_TAG=None, poem_place=None, poem_person=None):
    """GetOnePoetry
        :param poem_author: 作者[poet]: 李白、杜甫
        :param poem_type:
        :param poem_anthology: 诗文集[anthology]: 宋词精选、诗经、楚辞
        :param poem_category: 文类[category]: 诗、文、词、曲
        :param poem_dynasty: 朝代[dynasty]: 唐、宋、元、魏晋
        :param poem_emotion: 情感[poem/情感]: 忧国忧民、慷慨悲壮、哀怨凄婉、怡然自得、闲时
        :param poem_faction: 流派[faction]: 婉约派、豪放派
        :param poem_genre: 体裁[genre]: 骚体、杂言、长篇、新乐府
        :param poem_theme: 题材[theme]: 流放、抒情、关塞、写景怀古
        :param poem_expression: 表现手法[theme/表现手法]:
        :param poem_titleGroup: 词牌[tune]: 海棠春、武林春、踏莎行
        :param poem_reference: 典故[reference]:
        :param poem_TAG: 意向[yixiang]: 秋思、写鸟、农民
        :param poem_place: 地名[place]:
        :param poem_person: 人名[person]:

        :return: [poem]

        此方法 是本体与本体随机双向关系查询 排列组合成num种场景 第num+1场景用作兜底
        """
    num = 1
    query_conditions = []
    for i in range(num):
        query_conditions.append({
            "path_list": [],
            "recv_symbols": [
                "poem"
            ],
            "limit": 20
        })

    def random_direction(d):
        key = random.sample(d.keys(), 1)[0]
        value = d[key]
        return key, value

    if poem_author:
        a = {"代表作品": 0, "作者": 2}
        for i in range(num - 1):
            k, v = random_direction(a)
            query_conditions[i]["path_list"].append({
                "src_symbol": "poet",
                "src_ot": "poet",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_author
                        ]
                    }
                ],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [],
                "rel_symbol": "poet_rl",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            k
                        ]
                    }
                ],
                "direction": v
            })
        query_conditions[-1]["path_list"].append({
            "src_symbol": "poet",
            "src_ot": "poet",
            "src_filter": [
                {
                    "filter_key": "name",
                    "data_type": "string",
                    "vals": [
                        poem_author
                    ]
                }
            ],
            "target_symbol": "poem",
            "target_ot": "poem",
            "target_filter": [],
            "rel_symbol": "poet_rl",
            "rel_concepts": [
                "relation"
            ],
            "steps": 0,
            "rel_filter": [
                {
                    "filter_key": "name",
                    "data_type": "string",
                    "vals": [
                        "作者"
                    ]
                }
            ],
            "direction": 2
        })
    if poem_dynasty:
        for i in range(num):
            query_conditions[i]["path_list"].append({
                "src_symbol": "dynasty",
                "src_ot": "dynasty",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_dynasty
                        ]
                    }
                ],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [],
                "rel_symbol": "dynasty_rl",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            "所属朝代"
                        ]
                    }
                ],
                "direction": 2
            })
    if poem_genre:
        a = {"代表作品": 0, "体裁": 2}
        for i in range(num - 1):
            k, v = random_direction(a)
            query_conditions[i]["path_list"].append({
                "src_symbol": "genre",
                "src_ot": "genre",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_genre
                        ]
                    }
                ],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [],
                "rel_symbol": "genre_rl",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            k
                        ]
                    }
                ],
                "direction": v
            })
        query_conditions[-1]["path_list"].append({
            "src_symbol": "genre",
            "src_ot": "genre",
            "src_filter": [
                {
                    "filter_key": "name",
                    "data_type": "string",
                    "vals": [
                        poem_genre
                    ]
                }
            ],
            "target_symbol": "poem",
            "target_ot": "poem",
            "target_filter": [],
            "rel_symbol": "genre_rl",
            "rel_concepts": [
                "relation"
            ],
            "steps": 0,
            "rel_filter": [
                {
                    "filter_key": "name",
                    "data_type": "string",
                    "vals": [
                        "体裁"
                    ]
                }
            ],
            "direction": 2
        })
    if poem_TAG:
        for i in range(num):
            query_conditions[i]["path_list"].append({
                "src_symbol": "yixiang",
                "src_ot": "yixiang",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_TAG
                        ]
                    }
                ],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [],
                "rel_symbol": "yixiang_rl",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            "意象"
                        ]
                    }
                ],
                "direction": 2
            })
    if poem_expression:
        a = {"代表作品": 0, "题材": 2}
        for i in range(num - 1):
            k, v = random_direction(a)
            query_conditions[i]["path_list"].append({
                "src_symbol": "theme",
                "src_ot": "theme",
                "src_filter": [
                    {
                        "filter_key": "表现手法",
                        "data_type": "string",
                        "vals": [
                            poem_expression
                        ]
                    }
                ],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [],
                "rel_symbol": "theme_rl2",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            k
                        ]
                    }
                ],
                "direction": v
            })
        query_conditions[-1]["path_list"].append({
            "src_symbol": "theme",
            "src_ot": "theme",
            "src_filter": [
                {
                    "filter_key": "表现手法",
                    "data_type": "string",
                    "vals": [
                        poem_expression
                    ]
                }
            ],
            "target_symbol": "poem",
            "target_ot": "poem",
            "target_filter": [],
            "rel_symbol": "theme_rl2",
            "rel_concepts": [
                "relation"
            ],
            "steps": 0,
            "rel_filter": [
                {
                    "filter_key": "name",
                    "data_type": "string",
                    "vals": [
                        "题材"
                    ]
                }
            ],
            "direction": 2
        })
    if poem_emotion:
        for i in range(num):
            query_conditions[i]["path_list"].append({
                "src_symbol": "poem",
                "src_ot": "poem",
                "src_filter": [
                    {
                        "filter_key": "情感",
                        "data_type": "string",
                        "vals": [
                            poem_emotion
                        ]
                    }
                ]
            })
    if poem_anthology:
        a = {"代表作品": 0, "出处": 2}
        for i in range(num - 1):
            k, v = random_direction(a)
            query_conditions[i]["path_list"].append({
                "src_symbol": "anthology",
                "src_ot": "anthology",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_anthology
                        ]
                    }
                ],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [],
                "rel_symbol": "anthology_rl",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            k
                        ]
                    }
                ],
                "direction": v
            })
        query_conditions[-1]["path_list"].append({
            "src_symbol": "anthology",
            "src_ot": "anthology",
            "src_filter": [
                {
                    "filter_key": "name",
                    "data_type": "string",
                    "vals": [
                        poem_anthology
                    ]
                }
            ],
            "target_symbol": "poem",
            "target_ot": "poem",
            "target_filter": [],
            "rel_symbol": "anthology_rl",
            "rel_concepts": [
                "relation"
            ],
            "steps": 0,
            "rel_filter": [
                {
                    "filter_key": "name",
                    "data_type": "string",
                    "vals": [
                        "代表作品"
                    ]
                }
            ],
            "direction": 0
        })
    if poem_faction:
        for i in range(num):
            query_conditions[i]["path_list"].append({
                "src_symbol": "faction",
                "src_ot": "faction",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_faction
                        ]
                    }
                ],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [],
                "rel_symbol": "faction_rl",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            "代表作品"
                        ]
                    }
                ],
                "direction": 0
            })
    if poem_theme:
        a = {"代表作品": 0, "题材": 2}
        for i in range(num - 1):
            k, v = random_direction(a)
            query_conditions[i]["path_list"].append({
                "src_symbol": "theme",
                "src_ot": "theme",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_theme
                        ]
                    }
                ],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [],
                "rel_symbol": "theme_rl",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            k
                        ]
                    }
                ],
                "direction": v
            })
        query_conditions[-1]["path_list"].append({
            "src_symbol": "theme",
            "src_ot": "theme",
            "src_filter": [
                {
                    "filter_key": "name",
                    "data_type": "string",
                    "vals": [
                        poem_theme
                    ]
                }
            ],
            "target_symbol": "poem",
            "target_ot": "poem",
            "target_filter": [],
            "rel_symbol": "theme_rl",
            "rel_concepts": [
                "relation"
            ],
            "steps": 0,
            "rel_filter": [
                {
                    "filter_key": "name",
                    "data_type": "string",
                    "vals": [
                        "题材"
                    ]
                }
            ],
            "direction": 2
        })
    if poem_titleGroup:
        a = {"代表作品": 0, "多个？？？": 2}
        for i in range(num - 1):
            k, v = random_direction(a)
            query_conditions[i]["path_list"].append({
                "src_symbol": "tune",
                "src_ot": "tune",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_titleGroup
                        ]
                    }
                ],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [],
                "rel_symbol": "tune_rl",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [],
                "direction": v
            })
        query_conditions[-1]["path_list"].append({
            "src_symbol": "tune",
            "src_ot": "tune",
            "src_filter": [
                {
                    "filter_key": "name",
                    "data_type": "string",
                    "vals": [
                        poem_titleGroup
                    ]
                }
            ],
            "target_symbol": "poem",
            "target_ot": "poem",
            "target_filter": [],
            "rel_symbol": "tune_rl",
            "rel_concepts": [
                "relation"
            ],
            "steps": 0,
            "rel_filter": [],
            "direction": 2
        })
    if poem_reference:
        a = {"出处": 0, "用典": 2}
        for i in range(num - 1):
            k, v = random_direction(a)
            query_conditions[i]["path_list"].append({
                "src_symbol": "reference",
                "src_ot": "reference",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_reference
                        ]
                    }
                ],
                "target_symbol": "verse",
                "target_ot": "verse",
                "target_filter": [],
                "rel_symbol": "reference_rl",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            k
                        ]
                    }
                ],
                "direction": v
            })
            query_conditions[i]["path_list"].append({
                "src_symbol": "verse",
                "src_ot": "verse",
                "src_filter": [],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [],
                "rel_symbol": "verse_rl",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            "出处"
                        ]
                    }
                ],
                "direction": 0
            })

        # 典故与verse有关联 与poem无直接关系 所以是两跳查询
        query_conditions[-1]["path_list"].append({
            "src_symbol": "reference",
            "src_ot": "reference",
            "src_filter": [
                {
                    "filter_key": "name",
                    "data_type": "string",
                    "vals": [
                        poem_reference
                    ]
                }
            ],
            "target_symbol": "verse",
            "target_ot": "verse",
            "target_filter": [],
            "rel_symbol": "reference_rl",
            "rel_concepts": [
                "relation"
            ],
            "steps": 0,
            "rel_filter": [
                {
                    "filter_key": "name",
                    "data_type": "string",
                    "vals": [
                        "用典"
                    ]
                }
            ],
            "direction": 2
        })
        query_conditions[-1]["path_list"].append({
            "src_symbol": "verse",
            "src_ot": "verse",
            "src_filter": [],
            "target_symbol": "poem",
            "target_ot": "poem",
            "target_filter": [],
            "rel_symbol": "verse_rl",
            "rel_concepts": [
                "relation"
            ],
            "steps": 0,
            "rel_filter": [
                {
                    "filter_key": "name",
                    "data_type": "string",
                    "vals": [
                        "出处"
                    ]
                }
            ],
            "direction": 0
        })
    if poem_person:
        for i in range(num):
            query_conditions[i]["path_list"].append({
                "src_symbol": "person",
                "src_ot": "person",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_person
                        ]
                    }
                ],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [],
                "rel_symbol": "person_rl",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            "提及人名"
                        ]
                    }
                ],
                "direction": 2
            })
    if poem_place:
        for i in range(num):
            query_conditions[i]["path_list"].append({
                "src_symbol": "place",
                "src_ot": "place",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_place
                        ]
                    }
                ],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [],
                "rel_symbol": "place_rl",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            "提及地名"
                        ]
                    }
                ],
                "direction": 2
            })
    if poem_category:
        for i in range(num):
            query_conditions[i]["path_list"].append({
                "src_symbol": "category",
                "src_ot": "category",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_category
                        ]
                    }
                ],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [],
                "rel_symbol": "category_rl",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [],
                "optional": 1,
                "direction": 2
            })

    # 首位不能optional=1 强制执行optional=0
    if len(query_conditions[0]["path_list"]) > 0:
        if query_conditions[0]["path_list"][0].__contains__("optional"):
            query_conditions[0]["path_list"][0]["optional"] = 0

    # 没有槽位的场景
    if query_conditions == [{"path_list": [], "recv_symbols": ["poem"], "limit": 20}]:
        query_conditions = [{"limit": 20, "path_list": [{"src_symbol": "poem", "src_ot": "poem", "src_filter": []}],
                             "recv_symbols": ["poem"]}]

    return query_conditions


def get_one_poetry(poem_author=None, poem_type=None, poem_anthology=None,
                   poem_category=None, poem_dynasty=None, poem_emotion=None,
                   poem_faction=None, poem_genre=None, poem_theme=None,
                   poem_expression=None, poem_titleGroup=None, poem_reference=None,
                   poem_TAG=None, poem_place=None, poem_person=None):
    """GetOnePoetry
    :param poem_author: 作者[poet]: 李白、杜甫
    :param poem_type:
    :param poem_anthology: 诗文集[anthology]: 宋词精选、诗经、楚辞
    :param poem_category: 文类[category]: 诗、文、词、曲
    :param poem_dynasty: 朝代[dynasty]: 唐、宋、元、魏晋
    :param poem_emotion: 情感[poem/情感]: 忧国忧民、慷慨悲壮、哀怨凄婉、怡然自得、闲时
    :param poem_faction: 流派[faction]: 婉约派、豪放派
    :param poem_genre: 体裁[genre]: 骚体、杂言、长篇、新乐府
    :param poem_theme: 题材[theme]: 流放、抒情、关塞、写景怀古
    :param poem_expression: 表现手法[theme/表现手法]:
    :param poem_titleGroup: 词牌[tune]: 海棠春、武林春、踏莎行
    :param poem_reference: 典故[reference]:
    :param poem_TAG: 意向[yixiang]: 秋思、写鸟、农民
    :param poem_place: 地名[place]:
    :param poem_person: 人名[person]:

    :return: [poem]

    目前都是 各本体与poem本体双向关系查询
    """
    if poem_author:
        query_condition = [
            {
                "path_list": [
                    {
                        "src_symbol": "poet",
                        "src_ot": "poet",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_author
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 2
                    }
                ],
                "recv_symbols": [
                    "poem",
                    "poet"
                ],
                "limit": 20
            },
            {
                "path_list": [
                    {
                        "src_symbol": "poet",
                        "src_ot": "poet",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_author
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem",
                    "poet"
                ],
                "limit": 20
            }
        ]
        return query_condition

    if poem_anthology:
        query_condition = [
            {
                "path_list": [
                    {
                        "src_symbol": "anthology",
                        "src_ot": "anthology",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_anthology
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 2
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            },
            {
                "path_list": [
                    {
                        "src_symbol": "anthology",
                        "src_ot": "anthology",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_anthology
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            }
        ]
        return query_condition

    if poem_dynasty:
        query_condition = [
            {
                "path_list": [
                    {
                        "src_symbol": "dynasty",
                        "src_ot": "dynasty",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_dynasty
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 2
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            },
            {
                "path_list": [
                    {
                        "src_symbol": "dynasty",
                        "src_ot": "dynasty",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_dynasty
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            }
        ]
        return query_condition

    if poem_faction:
        query_condition = [
            {
                "path_list": [
                    {
                        "src_symbol": "faction",
                        "src_ot": "faction",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_faction
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 2
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            },
            {
                "path_list": [
                    {
                        "src_symbol": "faction",
                        "src_ot": "faction",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_faction
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            }
        ]
        return query_condition

    if poem_genre:
        query_condition = [
            {
                "path_list": [
                    {
                        "src_symbol": "genre",
                        "src_ot": "genre",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_genre
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 2
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            },
            {
                "path_list": [
                    {
                        "src_symbol": "genre",
                        "src_ot": "genre",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_genre
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            }
        ]
        return query_condition

    if poem_theme:
        query_condition = [
            {
                "path_list": [
                    {
                        "src_symbol": "theme",
                        "src_ot": "theme",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_theme
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 2
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            },
            {
                "path_list": [
                    {
                        "src_symbol": "theme",
                        "src_ot": "theme",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_theme
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            }
        ]
        return query_condition

    if poem_expression:
        query_condition = [
            {
                "path_list": [
                    {
                        "src_symbol": "theme",
                        "src_ot": "theme",
                        "src_filter": [
                            {
                                "filter_key": "表现手法",
                                "data_type": "string",
                                "vals": [
                                    poem_expression
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 2
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            },
            {
                "path_list": [
                    {
                        "src_symbol": "theme",
                        "src_ot": "theme",
                        "src_filter": [
                            {
                                "filter_key": "表现手法",
                                "data_type": "string",
                                "vals": [
                                    poem_expression
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            }
        ]
        return query_condition

    if poem_titleGroup:
        query_condition = [
            {
                "path_list": [
                    {
                        "src_symbol": "tune",
                        "src_ot": "tune",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_titleGroup
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 2
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            },
            {
                "path_list": [
                    {
                        "src_symbol": "tune",
                        "src_ot": "tune",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_titleGroup
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            }
        ]
        return query_condition

    if poem_reference:
        # 典故与verse有关联 与poem无直接关系 所以是两跳查询
        query_condition = [
            {
                "path_list": [
                    {
                        "src_symbol": "reference",
                        "src_ot": "reference",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_reference
                                ]
                            }
                        ],
                        "target_symbol": "verse",
                        "target_ot": "verse",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 2
                    },
                    {
                        "src_symbol": "verse",
                        "src_ot": "verse",
                        "src_filter": [],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r2",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            },
            {
                "path_list": [
                    {
                        "src_symbol": "reference",
                        "src_ot": "reference",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_reference
                                ]
                            }
                        ],
                        "target_symbol": "verse",
                        "target_ot": "verse",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    },
                    {
                        "src_symbol": "verse",
                        "src_ot": "verse",
                        "src_filter": [],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r2",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            }
        ]
        return query_condition

    if poem_TAG:
        # 意向与verse有关联 与poem无直接关系 所以是两跳查询
        query_condition = [
            {
                "path_list": [
                    {
                        "src_symbol": "yixiang",
                        "src_ot": "yixiang",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_TAG
                                ]
                            }
                        ],
                        "target_symbol": "verse",
                        "target_ot": "verse",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 2
                    },
                    {
                        "src_symbol": "verse",
                        "src_ot": "verse",
                        "src_filter": [],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r2",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            },
            {
                "path_list": [
                    {
                        "src_symbol": "yixiang",
                        "src_ot": "yixiang",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_TAG
                                ]
                            }
                        ],
                        "target_symbol": "verse",
                        "target_ot": "verse",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    },
                    {
                        "src_symbol": "verse",
                        "src_ot": "verse",
                        "src_filter": [],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r2",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            }
        ]
        return query_condition

    if poem_person:
        # 人名与verse有关联 与poem无直接关系 所以是两跳查询
        query_condition = [
            {
                "path_list": [
                    {
                        "src_symbol": "person",
                        "src_ot": "person",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_person
                                ]
                            }
                        ],
                        "target_symbol": "verse",
                        "target_ot": "verse",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 2
                    },
                    {
                        "src_symbol": "verse",
                        "src_ot": "verse",
                        "src_filter": [],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r2",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            },
            {
                "path_list": [
                    {
                        "src_symbol": "person",
                        "src_ot": "person",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_person
                                ]
                            }
                        ],
                        "target_symbol": "verse",
                        "target_ot": "verse",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    },
                    {
                        "src_symbol": "verse",
                        "src_ot": "verse",
                        "src_filter": [],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r2",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            }
        ]
        return query_condition

    if poem_emotion:
        query_condition = [
            {
                "path_list": [
                    {
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [
                            {
                                "filter_key": "情感",
                                "data_type": "string",
                                "vals": [
                                    poem_emotion
                                ]
                            }
                        ],
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            }
        ]
        return query_condition

    if poem_category:
        query_condition = [
            {
                "path_list": [
                    {
                        "src_symbol": "category",
                        "src_ot": "category",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_category
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 2
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            },
            {
                "path_list": [
                    {
                        "src_symbol": "category",
                        "src_ot": "category",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_category
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            }
        ]
        return query_condition

    if poem_place:
        query_condition = [
            {
                "path_list": [
                    {
                        "src_symbol": "place",
                        "src_ot": "place",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_place
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 2
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            },
            {
                "path_list": [
                    {
                        "src_symbol": "place",
                        "src_ot": "place",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_place
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            }
        ]
        return query_condition

    # 现在没用type了 保留 后面的流程应该走不去了
    if poem_type:
        """by type 背一首七言诗 槽位type
        p_1 情感  --pass
        p0 genre
        p1 theme
        p2 faction
        p3 category
        p4 anthology
        p5 dynasty
        p6 place
        p7 随机诗 兜底专业户  --pass
        """
        query_condition = [
            {
                "limit": 20,
                "path_list": [
                    {
                        "target_filter": [
                            {
                                "data_type": "string",
                                "filter_key": "情感",
                                "vals": [
                                    poem_type
                                ]
                            }
                        ],
                        "target_ot": "poem",
                        "target_symbol": "poem"
                    }
                ],
                "recv_symbols": [
                    "poem"
                ]
            },
            {
                "path_list": [
                    {
                        "path_symbol": "",
                        "src_symbol": "poem",
                        "src_ot": "poem",
                        "src_filter": [],
                        "target_symbol": "genre",
                        "target_ot": "genre",
                        "target_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    "七言律诗"
                                ]
                            }
                        ],
                        "rel_symbol": "",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 10
            },
            {
                "path_list": [
                    {
                        "path_symbol": "p1",
                        "src_symbol": "theme",
                        "src_ot": "theme",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_type
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 2
                    }
                ],
                "recv_symbols": [
                    "poem",
                    "theme"
                ],
                "limit": 10
            },
            {
                "path_list": [
                    {
                        "path_symbol": "p2",
                        "src_symbol": "faction",
                        "src_ot": "faction",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_type
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r2",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem",
                    "poet"
                ],
                "limit": 10
            },
            {
                "path_list": [
                    {
                        "path_symbol": "p3",
                        "src_symbol": "category",
                        "src_ot": "category",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_type
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r3",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem",
                    "poet"
                ],
                "limit": 10
            },
            {
                "path_list": [
                    {
                        "path_symbol": "p4",
                        "src_symbol": "anthology",
                        "src_ot": "anthology",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_type
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r4",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem",
                    "poet"
                ],
                "limit": 10
            },
            {
                "path_list": [
                    {
                        "path_symbol": "p5",
                        "src_symbol": "dynasty",
                        "src_ot": "dynasty",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_type
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r5",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem",
                    "poet"
                ],
                "limit": 10
            },
            {
                "path_list": [
                    {
                        "path_symbol": "p6",
                        "src_symbol": "place",
                        "src_ot": "place",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_type
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r6",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "poem",
                    "poet"
                ],
                "limit": 10
            },
            {
                "path_list": [
                    {
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                    }
                ],
                "recv_symbols": [
                    "poem"
                ],
                "limit": 20
            }
        ]
        return query_condition

    # 没有槽位场景
    query_condition = [
        {
            "path_list": [
                {
                    "target_symbol": "poem",
                    "target_ot": "poem",
                    "target_filter": [],
                }
            ],
            "recv_symbols": [
                "poem"
            ],
            "limit": 20
        }
    ]
    return query_condition


def return_get_one_poetry():
    """从获取到的诗句列表中随机返回一首 返回信息包含poem和poet的相关属性"""
    proResult["session"]["variables"]["success"] = {"key": "success", "value": "false"}
    poem_list = []
    api_kg = json.loads(proResult["session"]["variables"]["api_kg"]["value"])
    """接口报错 可能没查到 就表示没有下一句"""
    if api_kg.__contains__("msg"):
        return poem_list

    """从返回信息中循环取到所有诗句及其相关信息 存储到poem_list"""
    for data in api_kg["datas"]:
        a_poem_info = {}
        if data["row"].__contains__("poem"):
            if data["row"]["poem"].__contains__("node"):
                a_poem_info["题目"] = data["row"]["poem"]["node"]["vertexs"][0]["name"]
                a_poem_info = dict(data["row"]["poem"]["node"]["vertexs"][0]["prop_map"], **a_poem_info)

        if data["row"].__contains__("poet"):
            if data["row"]["poet"].__contains__("node"):
                a_poem_info["作者"] = data["row"]["poet"]["node"]["vertexs"][0]["name"]
                a_poem_info = dict(data["row"]["poet"]["node"]["vertexs"][0]["prop_map"], **a_poem_info)

        if a_poem_info:
            poem_list.append(a_poem_info)

    if poem_list:
        proResult["session"]["variables"]["recommend"] = {"key": "recommend", "value": "false"}
        this_turn_poetry = poem_list[random.randint(0, len(poem_list) - 1)]
        proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
        proResult["session"]["variables"]["now_poem_list"] = {"key": "now_poem_list",
                                                              "value": json.dumps(poem_list, ensure_ascii=False)}
        proResult["session"]["variables"]["now_poem_info"] = {"key": "now_poem_info",
                                                              "value": json.dumps(this_turn_poetry, ensure_ascii=False)}
        if this_turn_poetry.__contains__("题目"):
            title = this_turn_poetry["题目"]
            condition = get_one_poetry_information(title)
            proResult["session"]["variables"]["author_condition"] = {"key": "author_condition",
                                                                     "value": json.dumps(condition,
                                                                                         ensure_ascii=False)}
        """先看下是不是问的词牌名 词牌名有多个 采用追问/推荐 方案"""
        tune = return_slot_value("titleGroup")
        if tune:
            proResult["session"]["variables"]["recommend"] = {"key": "recommend", "value": "true"}
        return this_turn_poetry
    return poem_list


def return_recommend_one_poetry():
    tune = return_slot_value("titleGroup")
    this_turn_poetry = json.loads(proResult["session"]["variables"]["now_poem_info"]["value"])
    now_poem_list = json.loads(proResult["session"]["variables"]["now_poem_list"]["value"])
    recommend_tts = f"你想听哪一首{tune}呢，我推荐{this_turn_poetry['作者']}的《{this_turn_poetry['题目']}》！" \
                    f"同意请对我说“背诵{this_turn_poetry['作者']}的《{this_turn_poetry['题目']}》”"
    if len(now_poem_list) > 1:
        proResult["session"]["variables"]["recommend_tts"] = {"key": "recommend_tts", "value": recommend_tts}
        proResult["session"]["variables"]["recommend"] = {"key": "recommend", "value": "true"}
        return True
    """发现诗库只找到一首诗 就不走推荐回复"""
    proResult["session"]["variables"]["recommend"] = {"key": "recommend", "value": "false"}
    return False


def get_one_poetry_information(title):
    query_condition = [{"path_list": [{"src_symbol": "poem", "src_ot": "poem", "src_filter": [
        {"filter_key": "name", "data_type": "string",
         "vals": [f"{title}"]}], "target_symbol": "poet",
                                       "target_ot": "poet", "target_filter": [], "rel_symbol": "r1",
                                       "rel_concepts": ["relation"], "steps": 0, "rel_filter": [], "direction": 0},
                                      {"src_symbol": "poet", "src_ot": "poet", "src_filter": [],
                                       "target_symbol": "dynasty", "target_ot": "dynasty", "target_filter": [],
                                       "rel_symbol": "r2", "rel_concepts": ["relation"], "steps": 0, "rel_filter": [],
                                       "direction": 0}], "recv_symbols": ["poem", "poet", "dynasty"], "limit": 20}, {
                           "path_list": [{"src_symbol": "poem", "src_ot": "poem", "src_filter": [
                               {"filter_key": "name", "data_type": "string",
                                "vals": [f"{title}"]}],
                                          "target_symbol": "poet", "target_ot": "poet", "target_filter": [],
                                          "rel_symbol": "r1", "rel_concepts": ["relation"], "steps": 0,
                                          "rel_filter": [], "direction": 0},
                                         {"src_symbol": "poem", "src_ot": "poem", "src_filter": [],
                                          "target_symbol": "dynasty", "target_ot": "dynasty", "target_filter": [],
                                          "rel_symbol": "r2", "rel_concepts": ["relation"], "steps": 0,
                                          "rel_filter": [], "direction": 0}],
                           "recv_symbols": ["poem", "poet", "dynasty"], "limit": 20}, {"path_list": [
        {"src_symbol": "poem", "src_ot": "poem", "src_filter": [{"filter_key": "name", "data_type": "string", "vals": [
            f"{title}"]}], "target_symbol": "poet",
         "target_ot": "poet", "target_filter": [], "rel_symbol": "r1", "rel_concepts": ["relation"], "steps": 0,
         "rel_filter": [], "direction": 0}], "recv_symbols": ["poem", "poet"], "limit": 20}, {"path_list": [
        {"src_symbol": "poem", "src_ot": "poem", "src_filter": [{"filter_key": "name", "data_type": "string", "vals": [
            f"{title}"]}], "target_symbol": "dynasty",
         "target_ot": "dynasty", "target_filter": [], "rel_symbol": "r1", "rel_concepts": ["relation"], "steps": 0,
         "rel_filter": [], "direction": 0}], "recv_symbols": ["poem", "dynasty"], "limit": 20}, {"path_list": [
        {"src_symbol": "poem", "src_ot": "poem", "src_filter": [{"filter_key": "name", "data_type": "string", "vals": [
            f"{title}"]}]}], "recv_symbols": ["poem"], "limit": 20}]
    return query_condition


def return_get_one_poetry_information():
    """通过查出来的诗标题 去查询其作者与朝代信息"""
    proResult["session"]["variables"]["success"] = {"key": "success", "value": "false"}
    now_poem_info = json.loads(proResult["session"]["variables"]["now_poem_info"]["value"])
    api_kg = json.loads(proResult["session"]["variables"]["api_kg"]["value"])

    if api_kg.__contains__("msg"):
        return now_poem_info

    for data in api_kg["datas"]:
        if data["row"].__contains__("poem"):
            if data["row"]["poem"].__contains__("node"):
                a_poem_info = {}
                for v in data["row"]["poem"]["node"]["vertexs"]:
                    a_poem_info["题目"] = v["name"]
                    a_poem_info = dict(v["prop_map"], **a_poem_info)

                if a_poem_info["正文"] != now_poem_info["正文"]:
                    # 如果发现现在这首诗的正文与之前存的那首诗不一致 则跳过后面步骤 直接进入下一次循环
                    continue

                if data["row"].__contains__("poet"):
                    if data["row"]["poet"].__contains__("node"):
                        for w in data["row"]["poet"]["node"]["vertexs"]:
                            a_poem_info["作者"] = w["name"]
                            a_poem_info = dict(w["prop_map"], **a_poem_info)

                if data["row"].__contains__("dynasty"):
                    if data["row"]["dynasty"].__contains__("node"):
                        for x in data["row"]["dynasty"]["node"]["vertexs"]:
                            a_poem_info["朝代"] = x["name"]
                            a_poem_info = dict(x["prop_map"], **a_poem_info)
                proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
                proResult["session"]["variables"]["now_poem_info"] = {"key": "now_poem_info",
                                                                      "value": json.dumps(a_poem_info,
                                                                                          ensure_ascii=False)}
                return a_poem_info
    return now_poem_info


def get_poetry_by_title(poem_title, poem_author=None):
    """GetPoetryByTitle 根据诗名查作者 answer取诗内容 作者留给后续多轮
    :param poem_title:
    :param poem_author:
    :return: [poet poem]
    """
    query_condition = [{
        "path_list": [
            {
                "path_symbol": "p",
                "src_symbol": "poem",
                "src_ot": "poem",
                "src_filter": [{
                    "filter_key": "name",
                    "data_type": "string",
                    "vals": [
                        poem_title
                    ]
                }],
                "target_symbol": "poet",
                "target_ot": "poet",
                "target_filter": [{
                    "filter_key": "name",
                    "data_type": "string",
                    "vals": [
                        poem_author
                    ]
                }],
                "rel_symbol": "r1",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [],
                "direction": 0
            }
        ],
        "recv_symbols": [
            "p",
            "poem",
            "poet"
        ],
        "limit": 10
    }]
    if not poem_author:
        query_condition[0]["path_list"][0]["target_filter"] = []
    return query_condition


def get_poetry_by_phrases(poem_content, poem_author=None, poem_type=None):
    """GetPoetryByPhrases 根据诗句查诗并同时查作者 answer取诗内容 作者留给后续多轮
    :param poem_type: 这里先不管type 后续出问题了再看看
    :param poem_author:
    :param poem_content:
    :return: [poet poem]
    """
    if poem_content and "||" in poem_content:
        # content可能有多段 这里默认SDK是已经排序给过来的 就去取最后一段
        poem_content = poem_content.split("||")[-1]
    query_condition = [{
        "path_list": [
            {
                "path_symbol": "p",
                "src_symbol": "verse",
                "src_ot": "verse",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_content
                        ]
                    }
                ],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [],
                "rel_symbol": "r1",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            "出处"
                        ]
                    }
                ],
                "direction": 0
            },
            {
                "path_symbol": "p1",
                "src_symbol": "poem",
                "src_ot": "poem",
                "src_filter": [],
                "target_symbol": "poet",
                "target_ot": "poet",
                "target_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_author
                        ]
                    }
                ],
                "rel_symbol": "r2",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            "作者"
                        ]
                    }
                ],
                "direction": 0
            }
        ],
        "recv_symbols": [
            "p",
            "p1",
            "poem",
            "poet",
            "verse"
        ],
        "limit": 10
    }]
    if not poem_author:
        query_condition[0]["path_list"][1]["target_filter"] = []
    return query_condition


def return_get_trans_by_phrases():
    """先判断本句诗是否有句号 再通过本句向下查询 找到含有句号的这段 输出其译文
    :return: [这一句 poet poem]
    """
    text_list = ["读诗不求甚解，跟随一字一句，体悟内心生发的感动，自会有自己的理解！",
                 "读诗百遍，其义自见，一定是我读的还不够多，译文下次再讲给你听吧"]
    now_text = text_list[random.randint(0, len(text_list) - 1)]
    proResult["session"]["variables"]["not_found_poetry_answer"] = {"key": "not_found_poetry_answer", "value": now_text}
    proResult["session"]["variables"]["success"] = {"key": "success", "value": "false"}
    now_poem_info = {}
    api_kg = json.loads(proResult["session"]["variables"]["api_kg"]["value"])
    """接口报错 可能没查到本句"""
    if api_kg.__contains__("msg"):
        return now_poem_info

    """先判断下本段有没有句号"""
    for data in api_kg["datas"]:
        if data["row"].__contains__("verse"):
            if data["row"]["verse"].__contains__("node"):

                name = data["row"]["verse"]["node"]["vertexs"][0]["name"]
                # TODO 这里原句需要向前补齐
                now_poem_info = {"这一句": name}
                if "。" in name:
                    now_poem_info = dict(data["row"]["verse"]["node"]["vertexs"][0]["prop_map"], **now_poem_info)
                    proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
                    proResult["session"]["variables"]["now_poem_info"] = {"key": "now_poem_info",
                                                                          "value": json.dumps(now_poem_info,
                                                                                              ensure_ascii=False)}
                    if len(now_poem_info["译文"]) < 10:
                        proResult["session"]["variables"]["success"] = {"key": "success", "value": "false"}
                    return now_poem_info

    """再判断后续段有没有句号"""
    for data in api_kg["datas"]:
        if data["row"].__contains__("p"):
            steps = data["row"]["p"]["path"]["steps"]
            poem_text = data["row"]["p"]["path"]["src"]["vertexs"][0]["name"]
            for step in steps:
                name = step["dst"]["vertexs"][0]["name"]
                # TODO 如果是中间句 也需要向前补齐
                poem_text += name
                if "。" in name:
                    now_poem_info = step["dst"]["vertexs"][0]["prop_map"]
                    now_poem_info = dict({"这一句": poem_text}, **now_poem_info)
                    proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
                    proResult["session"]["variables"]["now_poem_info"] = {"key": "now_poem_info",
                                                                          "value": json.dumps(now_poem_info,
                                                                                              ensure_ascii=False)}
                    if len(now_poem_info["译文"]) < 10:
                        proResult["session"]["variables"]["success"] = {"key": "success", "value": "false"}
                    return now_poem_info
    return now_poem_info


def get_trans_by_phrases(poem_content, poem_author=None, steps=5):
    """GetTransByPhrases 诗句的翻译都存放在本句最后一段 先查本段的本体 看看有没有句号 再找下一句 决定选取哪句下的译文
    :param poem_content:
    :param poem_author:
    :param steps:
    :return: [p verse]
    """
    if poem_content and "||" in poem_content:
        # content可能有多段 这里默认SDK是已经排序给过来的 就去取第一段
        poem_content = poem_content.split("||")[0]
    query_condition = [
        {
            "limit": 10,
            "path_list": [
                {
                    "src_filter": [
                        {
                            "data_type": "string",
                            "filter_key": "name",
                            "vals": [
                                poem_content
                            ]
                        }
                    ],
                    "src_ot": "verse",
                    "src_symbol": "verse"
                },
                {
                    "direction": 0,
                    "optional": 1,
                    "path_symbol": "p",
                    "rel_concepts": [
                        "relation"
                    ],
                    "rel_filter": [
                        {
                            "data_type": "string",
                            "filter_key": "name",
                            "vals": [
                                "下一句"
                            ]
                        }
                    ],
                    "rel_symbol": "r1",
                    "src_filter": [
                        {
                            "data_type": "string",
                            "filter_key": "name",
                            "vals": [
                                poem_content
                            ]
                        }
                    ],
                    "src_ot": "verse",
                    "src_symbol": "verse",
                    "steps": steps,
                    "target_filter": [],
                    "target_ot": "",
                    "target_symbol": "v2"
                }
            ],
            "recv_symbols": [
                "p",
                "verse"
            ]
        }
    ]
    return query_condition


def get_core_phrases(poem_title, poem_content, steps=5):
    """GetCorePhrases 根据诗名查名句 再查2步下一句 answer取句号为止
    :param steps:
    :param poem_title:
    :param poem_content:
    :return: [p]
    """
    if poem_title:
        query_condition = [
            {
                "path_list": [
                    {
                        "path_symbol": "",
                        "src_symbol": "poem",
                        "src_ot": "poem",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_title
                                ]
                            }
                        ],
                        "target_symbol": "verse1",
                        "target_ot": "verse",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    "名句"
                                ]
                            }
                        ],
                        "direction": 0
                    },
                    {
                        "path_symbol": "p",
                        "src_symbol": "verse1",
                        "src_ot": "verse",
                        "src_filter": [],
                        "target_symbol": "verse2",
                        "target_ot": "",
                        "target_filter": [],
                        "rel_symbol": "r2",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": steps,
                        "rel_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    "下一句"
                                ]
                            }
                        ],
                        "direction": 0
                    },
                    {
                        "direction": 0,
                        "optional": 1,
                        "rel_concepts": [
                            "relation"
                        ],
                        "rel_filter": [
                            {
                                "data_type": "string",
                                "filter_key": "name",
                                "vals": [
                                    "作者"
                                ]
                            }
                        ],
                        "rel_symbol": "r3",
                        "src_ot": "poem",
                        "src_symbol": "poem",
                        "target_filter": [],
                        "target_ot": "poet",
                        "target_symbol": "poet"
                    }
                ],
                "recv_symbols": [
                    "p",
                    "poem",
                    "poet"
                ],
                "limit": 10
            }
        ]
        return query_condition

    elif poem_content:
        query_condition = [
            {
                "path_list": [
                    {
                        "path_symbol": "",
                        "src_symbol": "verse0",
                        "src_ot": "verse",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_content
                                ]
                            }
                        ],
                        "target_symbol": "poem",
                        "target_ot": "poem",
                        "target_filter": [],
                        "rel_symbol": "r0",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    "出处"
                                ]
                            }
                        ],
                        "direction": 0
                    },
                    {
                        "path_symbol": "",
                        "src_symbol": "poem",
                        "src_ot": "poem",
                        "src_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    poem_title
                                ]
                            }
                        ],
                        "target_symbol": "verse1",
                        "target_ot": "verse",
                        "target_filter": [],
                        "rel_symbol": "r1",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": 0,
                        "rel_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    "名句"
                                ]
                            }
                        ],
                        "direction": 0
                    },
                    {
                        "path_symbol": "p",
                        "src_symbol": "verse1",
                        "src_ot": "verse",
                        "src_filter": [],
                        "target_symbol": "verse2",
                        "target_ot": "",
                        "target_filter": [],
                        "rel_symbol": "r2",
                        "rel_concepts": [
                            "relation"
                        ],
                        "steps": steps,
                        "rel_filter": [
                            {
                                "filter_key": "name",
                                "data_type": "string",
                                "vals": [
                                    "下一句"
                                ]
                            }
                        ],
                        "direction": 0
                    }
                ],
                "recv_symbols": [
                    "p",
                    "poem"
                ],
                "limit": 10
            }
        ]
        return query_condition


def return_get_core_phrases():
    """
    :return: [这一句]
    """
    proResult["session"]["variables"]["success"] = {"key": "success", "value": "false"}
    now_poem_info = {}
    api_kg = json.loads(proResult["session"]["variables"]["api_kg"]["value"])
    """接口报错 可能没查到本句"""
    if api_kg.__contains__("msg"):
        return now_poem_info

    for data in api_kg["datas"]:
        if data["row"].__contains__("poem"):
            if data["row"]["poem"].__contains__("node"):
                now_poem_info["题目"] = data["row"]["poem"]["node"]["vertexs"][0]["name"]
                now_poem_info = dict(data["row"]["poem"]["node"]["vertexs"][0]["prop_map"], **now_poem_info)

        if data["row"].__contains__("poet"):
            if data["row"]["poet"].__contains__("node"):
                for w in data["row"]["poet"]["node"]["vertexs"]:
                    now_poem_info["作者"] = w["name"]
                    now_poem_info = dict(w["prop_map"], **now_poem_info)

        if data["row"].__contains__("p"):
            steps = data["row"]["p"]["path"]["steps"]
            poem_text = data["row"]["p"]["path"]["src"]["vertexs"][0]["name"]
            for step in steps:
                name = step["dst"]["vertexs"][0]["name"]
                poem_text += name
                if "。" in name:
                    now_poem_info = dict(step["dst"]["vertexs"][0]["prop_map"], **now_poem_info)
                    proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
                    now_poem_info = dict({"这一句": poem_text}, **now_poem_info)
                    proResult["session"]["variables"]["now_poem_info"] = {"key": "now_poem_info",
                                                                          "value": json.dumps(now_poem_info,
                                                                                              ensure_ascii=False)}
                    return now_poem_info
    return now_poem_info


def get_master_piece(poem_author, poem_type=None):
    """GetMasterpiece 直接查poet到poem路径
    :param poem_type:
    :param poem_author:
    :return: [poet poem]
    """
    query_condition = [{
        "path_list": [
            {
                "path_symbol": "p",
                "src_symbol": "poet",
                "src_ot": "poet",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_author
                        ]
                    }
                ],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [],
                "rel_symbol": "r1",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [],
                "direction": 0
            }
        ],
        "recv_symbols": [
            "p",
            "poem",
            "poet"
        ],
        "limit": 10
    }]

    return query_condition


def return_get_master_piece():
    """返回篇名，热门原则，作品颇丰的诗人，不用全部返回，需要抽取3~4首名篇即可(在数据里有hot标记)"""
    proResult["session"]["variables"]["success"] = {"key": "success", "value": "false"}
    now_poem_info = {}
    api_kg = json.loads(proResult["session"]["variables"]["api_kg"]["value"])
    """接口报错处理"""
    if api_kg.__contains__("msg"):
        return now_poem_info

    poem_titles = []
    for data in api_kg["datas"]:
        if data["row"].__contains__("poem"):
            if data["row"]["poem"].__contains__("node"):
                one_poem = data["row"]["poem"]["node"]["vertexs"][0]["name"]
                poem_titles.append(one_poem)
                poem_info = data["row"]["poem"]["node"]["vertexs"][0]["prop_map"]
                now_poem_info = dict(poem_info, **now_poem_info)
        if data["row"].__contains__("poet"):
            if data["row"]["poet"].__contains__("node"):
                poet_info = data["row"]["poet"]["node"]["vertexs"][0]["prop_map"]
                now_poem_info = dict(poet_info, **now_poem_info)
                now_poem_info["作者"] = data["row"]["poet"]["node"]["vertexs"][0]["name"]

    if now_poem_info and poem_titles:
        for i in range(len(poem_titles)):
            poem_titles[i] = f"《{poem_titles[i]}》"
        now_poem_info = dict({"代表作品": "".join(poem_titles)}, **now_poem_info)
        proResult["session"]["variables"]["now_poem_info"] = {"key": "now_poem_info",
                                                              "value": json.dumps(now_poem_info,
                                                                                  ensure_ascii=False)}
        proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
        return now_poem_info
    return now_poem_info


def get_translates(poem_title=None, poem_author=None, poem_content=None):
    """GetTranslates 直接从poem到poet
    :param poem_title:
    :param poem_author:
    :param poem_content: 好像没有这个槽位 get_trans_by_phrases 已经实现功能
    :return: [poet poem]
    """
    query_condition = [{
        "path_list": [
            {
                "path_symbol": "p",
                "src_symbol": "poet",
                "src_ot": "poet",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_author
                        ]
                    }
                ],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_title
                        ]
                    }
                ],
                "rel_symbol": "r1",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [],
                "direction": 2
            }
        ],
        "recv_symbols": [
            "p",
            "poem",
            "poet"
        ],
        "limit": 10
    }]
    if not poem_author:
        query_condition[0]["path_list"][0]["src_filter"] = []

    if not poem_title:
        query_condition[0]["path_list"][0]["target_filter"] = []

    return query_condition


def return_get_translates():
    """从poem中抽取译文"""
    text_list = ["读诗不求甚解，跟随一字一句，体悟内心生发的感动，自会有自己的理解！",
                 "读诗百遍，其义自见，一定是我读的还不够多，译文下次再讲给你听吧"]
    now_text = text_list[random.randint(0, len(text_list) - 1)]
    proResult["session"]["variables"]["not_found_poetry_answer"] = {"key": "not_found_poetry_answer", "value": now_text}
    proResult["session"]["variables"]["success"] = {"key": "success", "value": "false"}
    now_poem_info = {}
    api_kg = json.loads(proResult["session"]["variables"]["api_kg"]["value"])
    """接口报错 可能没查到本句"""
    if api_kg.__contains__("msg"):
        return now_poem_info
    for data in api_kg["datas"]:
        if data["row"].__contains__("poet"):
            poet_info = data["row"]["poet"]["node"]["vertexs"][0]["prop_map"]
            now_poem_info = dict(poet_info, **now_poem_info)
            now_poem_info["作者"] = data["row"]["poet"]["node"]["vertexs"][0]["name"]
        if data["row"].__contains__("poem"):
            poem_info = data["row"]["poem"]["node"]["vertexs"][0]["prop_map"]
            now_poem_info = dict(poem_info, **now_poem_info)
            proResult["session"]["variables"]["now_poem_info"] = {"key": "now_poem_info",
                                                                  "value": json.dumps(now_poem_info,
                                                                                      ensure_ascii=False)}
            proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
            if len(now_poem_info["译文"]) < 10:
                proResult["session"]["variables"]["success"] = {"key": "success", "value": "false"}
            return now_poem_info
    return now_poem_info


def get_author_names(poem_title=None, poem_content=None):
    """GetAuthorNames 多轮/单轮 获取作者信息
    :param poem_title:
    :param poem_content:
    :return: [poet poem]
    """
    if poem_content and "||" in poem_content:
        # content可能有多段 这里默认SDK是已经排序给过来的 就去取最后一段
        poem_content = poem_content.split("||")[-1]
    query_condition = [{
        "path_list": [
            {
                "path_symbol": "p",
                "src_symbol": "verse",
                "src_ot": "verse",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_content
                        ]
                    }
                ],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [],
                "rel_symbol": "r1",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            "出处"
                        ]
                    }
                ],
                "direction": 0
            },
            {
                "path_symbol": "p1",
                "src_symbol": "poem",
                "src_ot": "poem",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_title
                        ]
                    }
                ],
                "target_symbol": "poet",
                "target_ot": "poet",
                "target_filter": [],
                "rel_symbol": "r2",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            "作者"
                        ]
                    }
                ],
                "direction": 0
            }
        ],
        "recv_symbols": [
            "p",
            "p1",
            "poem",
            "poet",
            "verse"
        ],
        "limit": 10
    }]
    if not poem_title:
        query_condition[0]["path_list"][1]["src_filter"] = []
    if not poem_content:
        query_condition[0]["path_list"].remove(query_condition[0]["path_list"][0])
        query_condition[0]["recv_symbols"].remove("p")
        query_condition[0]["recv_symbols"].remove("verse")
    return query_condition


def return_get_author_names():
    return return_get_authors()


def check_author_name():
    """多轮get_author_names的连线条件 先看下用户本轮是否有新输入槽位 如果没有则去判断上一轮信息"""
    content = return_slot_value("content")
    title = return_slot_value("title")
    if content or title:
        proResult["success"] = False
        return False
    if proResult["session"]["variables"].__contains__("now_poem_info"):
        now_poem_info = json.loads(proResult["session"]["variables"]["now_poem_info"]["value"])
        if now_poem_info.__contains__("作者"):
            poet = now_poem_info["作者"]
            if poet:
                proResult["success"] = True
                return True
    proResult["success"] = False
    return False


def get_authors(poem_author, poem_title=None):
    """GetAuthors 介绍作者相关
    :param poem_title: 好像没有用到这个 不过还是从poem到poet去查
    :param poem_author:
    :return: [poet poem]
    """
    query_condition = [{
        "path_list": [
            {
                "path_symbol": "p",
                "src_symbol": "poet",
                "src_ot": "poet",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_author
                        ]
                    }
                ],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_title
                        ]
                    }
                ],
                "rel_symbol": "r1",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [],
                "direction": 2
            }
        ],
        "recv_symbols": [
            "p",
            "poem",
            "poet"
        ],
        "limit": 10
    }]
    if not poem_author:
        query_condition[0]["path_list"][0]["src_filter"] = []
    if not poem_title:
        query_condition[0]["path_list"][0]["target_filter"] = []
    return query_condition


def return_get_authors():
    """介绍作者相关"""
    proResult["session"]["variables"]["success"] = {"key": "success", "value": "false"}
    now_poem_info = {}
    api_kg = json.loads(proResult["session"]["variables"]["api_kg"]["value"])
    """接口报错 可能没查到本句"""
    if api_kg.__contains__("msg"):
        return now_poem_info
    for data in api_kg["datas"]:
        if data["row"].__contains__("poem"):
            if data["row"]["poem"].__contains__("node"):
                poem_info = data["row"]["poem"]["node"]["vertexs"][0]["prop_map"]
                now_poem_info = dict(poem_info, **now_poem_info)

        if data["row"].__contains__("poet"):
            if data["row"]["poet"].__contains__("node"):
                poet_info = data["row"]["poet"]["node"]["vertexs"][0]["prop_map"]
                now_poem_info["作者"] = data["row"]["poet"]["node"]["vertexs"][0]["name"]
                now_poem_info = dict(poet_info, **now_poem_info)

                """这里先检查简介是否为空 如果为空 则遍历输出poet的属性值"""
                if now_poem_info["简介"] != "":
                    proResult["session"]["variables"]["now_poem_info"] = {"key": "now_poem_info",
                                                                          "value": json.dumps(now_poem_info,
                                                                                              ensure_ascii=False)}
                    proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
                    return now_poem_info
                else:
                    now_poem_info["简介"] += data["row"]["poet"]["node"]["vertexs"][0]["name"]
                    for x, y in data["row"]["poet"]["node"]["vertexs"][0]["prop_map"].items():
                        if y != "":
                            now_poem_info["简介"] += f"，{x}:{y}"
                    proResult["session"]["variables"]["now_poem_info"] = {"key": "now_poem_info",
                                                                          "value": json.dumps(now_poem_info,
                                                                                              ensure_ascii=False)}
                    proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
                    return now_poem_info
    return now_poem_info


def check_title():
    """多轮get_authors的连线条件 先看下用户本轮是否有新输入槽位 如果没有则去判断上一轮信息"""
    content = return_slot_value("content")
    if content:
        proResult["success"] = False
        return False
    if proResult["session"]["variables"].__contains__("now_poem_info"):
        now_poem_info = json.loads(proResult["session"]["variables"]["now_poem_info"]["value"])
        if now_poem_info.__contains__("题目"):
            poet = now_poem_info["题目"]
            if poet:
                proResult["success"] = True
                return True
    proResult["success"] = False
    return False


def get_dynasty(poem_author):
    """GetDynasty 查询作者 所属朝代
    :param poem_author:
    :return: [poet dynasty]
    """
    query_condition = [{
        "path_list": [
            {
                "path_symbol": "p",
                "src_symbol": "poet",
                "src_ot": "poet",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_author
                        ]
                    }
                ],
                "target_symbol": "dynasty",
                "target_ot": "dynasty",
                "target_filter": [],
                "rel_symbol": "r1",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [],
                "direction": 0
            }
        ],
        "recv_symbols": [
            "p",
            "dynasty",
            "poet"
        ],
        "limit": 10
    }]
    return query_condition


def return_get_dynasty():
    """返回作者朝代"""
    proResult["session"]["variables"]["success"] = {"key": "success", "value": "false"}
    now_poem_info = {}
    api_kg = json.loads(proResult["session"]["variables"]["api_kg"]["value"])
    """接口报错 可能没查到"""
    if api_kg.__contains__("msg"):
        return now_poem_info
    for data in api_kg["datas"]:
        if data["row"].__contains__("poet"):
            if data["row"]["poet"].__contains__("node"):
                poet_info = data["row"]["poet"]["node"]["vertexs"][0]["prop_map"]
                now_poem_info = dict(poet_info, **now_poem_info)
                now_poem_info["作者"] = data["row"]["poet"]["node"]["vertexs"][0]["name"]

        if data["row"].__contains__("dynasty"):
            if data["row"]["dynasty"].__contains__("node"):
                dynasty_info = data["row"]["dynasty"]["node"]["vertexs"][0]["prop_map"]
                now_poem_info = dict(dynasty_info, **now_poem_info)
                now_poem_info["朝代"] = data["row"]["dynasty"]["node"]["vertexs"][0]["name"]
                proResult["session"]["variables"]["now_poem_info"] = {"key": "now_poem_info",
                                                                      "value": json.dumps(now_poem_info,
                                                                                          ensure_ascii=False)}
                proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
                return now_poem_info
    return now_poem_info


def get_last_phrases(poem_content, steps=5):
    """GetLastPhrases
    :param steps:
    :param poem_content:
    :return: [p]
    """
    if poem_content and "||" in poem_content:
        """content可能有多段 这里默认SDK是已经排序给过来的 就去取第一段"""
        poem_content = poem_content.split("||")[0]
    query_condition = [{
        "path_list": [
            {
                "path_symbol": "p",
                "src_symbol": "v1",
                "src_ot": "verse",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_content
                        ]
                    }
                ],
                "target_symbol": "v2",
                "target_ot": "",
                "target_filter": [],
                "rel_symbol": "r1",
                "rel_concepts": [
                    "relation"
                ],
                "steps": steps,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            "上一句"
                        ]
                    }
                ],
                "direction": 0
            }
        ],
        "recv_symbols": [
            "p"
        ],
        "limit": 10
    }]
    return query_condition


def return_get_last_phrases():
    """查询到2步后 组装回复的诗句 以句号终止"""
    proResult["session"]["variables"]["success"] = {"key": "success", "value": "false"}
    now_poem_info = {"历史意图": "get_last_phrases"}
    api_kg = json.loads(proResult["session"]["variables"]["api_kg"]["value"])

    """接口报错 可能没查到 就表示没有上一句"""
    if api_kg.__contains__("msg"):
        return now_poem_info

    """这里先默认取最后一个 不知道后面会不会有问题"""
    data = api_kg["datas"][-1]
    steps = data["row"]["p"]["path"]["steps"]

    # 先判断本句中是否含有句号
    query_content = data["row"]["p"]["path"]["src"]["vertexs"][0]["name"]
    now_poem_info["这一句"] = query_content
    max_c = 2  # 统计句号出现的次数，出现第二次就不要那一段了
    if "。" in query_content:
        max_c = 1  # 统计句号出现的次数，出现第一次就不要那一段了

    last_phrases = ""
    c = 0
    for step in steps:
        text = step["dst"]["vertexs"][0]["name"]
        if "。" in text:
            c += 1
        if c >= max_c:
            break
        else:
            last_phrases = text + last_phrases

    if "。" in query_content:
        last_phrases += query_content

    now_poem_info["上一句"] = last_phrases
    # TODO 如果是中间句该怎么办

    proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
    proResult["session"]["variables"]["now_poem_info"] = {"key": "now_poem_info",
                                                          "value": json.dumps(now_poem_info, ensure_ascii=False)}
    return now_poem_info


def get_one_more_poetry():
    """OneMorePoetry 换诗 随机抽诗即可 回复时需排除掉上一轮的诗
    :return:
    """
    return get_one_poetry()


def return_one_more_poetry():
    """OneMorePoetry多轮 排除掉上一轮的诗"""
    last_poem_info = None
    if proResult["session"]["variables"].__contains__("now_poem_info"):
        last_poem_info = json.loads(proResult["session"]["variables"]["now_poem_info"]["value"])
    new_turn_poetry = return_get_one_poetry()

    # 看下这个意图之前有没有上文 没有则当第一轮处理
    if not last_poem_info:
        return new_turn_poetry

    # 看下随机取诗是否取到与上一轮不相同的 相同则进一步处理
    if new_turn_poetry and last_poem_info["题目"] != new_turn_poetry["题目"]:
        return True

    # 如果取到的诗与上一轮相同了 就从诗列表中去遍历取不相同的 实在没有 也没办法了
    if proResult["session"]["variables"].__contains__("now_poem_list"):
        now_poem_list = json.loads(proResult["session"]["variables"]["now_poem_list"]["value"])
        for p in now_poem_list:
            if p["题目"] != last_poem_info["题目"]:
                proResult["session"]["variables"]["now_poem_info"] = {"key": "now_poem_info",
                                                                      "value": json.dumps(p, ensure_ascii=False)}
                if p.__contains__("题目"):
                    title = p["题目"]
                    condition = get_one_poetry_information(title)
                    proResult["session"]["variables"]["author_condition"] = {"key": "author_condition",
                                                                             "value": json.dumps(condition,
                                                                                                 ensure_ascii=False)}
                proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
                return True


def get_titles(poem_content):
    """GetTitles 通过verse查找poem
    :param poem_content:
    :return: [poet poem verse]
    """
    if poem_content and "||" in poem_content:
        # content可能有多段 这里默认SDK是已经排序给过来的 就去取最后一段
        poem_content = poem_content.split("||")[-1]
    query_condition = [{
        "path_list": [
            {
                "path_symbol": "p",
                "src_symbol": "verse",
                "src_ot": "verse",
                "src_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            poem_content
                        ]
                    }
                ],
                "target_symbol": "poem",
                "target_ot": "poem",
                "target_filter": [],
                "rel_symbol": "r1",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            "出处"
                        ]
                    }
                ],
                "direction": 0
            },
            {
                "path_symbol": "p1",
                "src_symbol": "poem",
                "src_ot": "poem",
                "src_filter": [],
                "target_symbol": "poet",
                "target_ot": "poet",
                "target_filter": [],
                "rel_symbol": "r2",
                "rel_concepts": [
                    "relation"
                ],
                "steps": 0,
                "rel_filter": [
                    {
                        "filter_key": "name",
                        "data_type": "string",
                        "vals": [
                            "作者"
                        ]
                    }
                ],
                "direction": 0
            }
        ],
        "recv_symbols": [
            "p",
            "p1",
            "poem",
            "poet",
            "verse"
        ],
        "limit": 10
    }]

    return query_condition


def return_get_titles():
    """"""
    proResult["session"]["variables"]["success"] = {"key": "success", "value": "false"}
    now_poem_info = {}
    api_kg = json.loads(proResult["session"]["variables"]["api_kg"]["value"])
    """接口报错 可能没查到本句"""
    if api_kg.__contains__("msg"):
        return now_poem_info

    for data in api_kg["datas"]:
        if data["row"].__contains__("poem"):
            if data["row"]["poem"].__contains__("node"):
                poem_info = data["row"]["poem"]["node"]["vertexs"][0]["prop_map"]
                now_poem_info["题目"] = data["row"]["poem"]["node"]["vertexs"][0]["name"]
                now_poem_info = dict(poem_info, **now_poem_info)

        if data["row"].__contains__("poet"):
            if data["row"]["poet"].__contains__("node"):
                poet_info = data["row"]["poet"]["node"]["vertexs"][0]["prop_map"]
                now_poem_info["作者"] = data["row"]["poet"]["node"]["vertexs"][0]["name"]
                now_poem_info = dict(poet_info, **now_poem_info)

        if data["row"].__contains__("verse"):
            if data["row"]["verse"].__contains__("node"):
                now_poem_info["这一句"] = data["row"]["verse"]["node"]["vertexs"][0]["name"]
                now_poem_info = dict(data["row"]["verse"]["node"]["vertexs"][0]["prop_map"], **now_poem_info)

                proResult["session"]["variables"]["success"] = {"key": "success", "value": "true"}
                proResult["session"]["variables"]["now_poem_info"] = {"key": "now_poem_info",
                                                                      "value": json.dumps(now_poem_info,
                                                                                          ensure_ascii=False)}
                return now_poem_info
    return now_poem_info


def modify_query_condition():
    current_intent = proResult["quresult"]["intent"]
    if current_intent == "GetNextPhrases":
        poem_content = return_slot_value("content")
        if not poem_content:
            now_poem_info_value = return_variable_value("now_poem_info")
            if now_poem_info_value:
                now_poem_info = json.loads(now_poem_info_value)
                if now_poem_info.__contains__("下一句"):
                    poem_content = re.findall("[一-龥]+", now_poem_info["下一句"])[-1]
                elif now_poem_info.__contains__("这一句"):
                    poem_content = re.findall("[一-龥]+", now_poem_info["这一句"])[-1]
        return get_next_phrases(poem_content=poem_content, steps=5)

    if current_intent == "GetNextPhrasesAgain":
        now_poem_info_value = return_variable_value("now_poem_info")
        if now_poem_info_value:
            this_reply = json.loads(now_poem_info_value)
            if this_reply.__contains__("下一句"):
                this_content = this_reply["下一句"]
                """上一轮的GetNextPhrases 返回的应该是一整句 所以这里取到一整句后 通过正则取到最后一段 将最后一段放到接口去查"""
                poem_content = re.findall("[一-龥]+", this_content)[-1]
                return get_next_phrases_again(poem_content=poem_content, steps=100)

    if current_intent == "GetOnePoetry":
        """这里针对此case做特殊处理 query:再来一首他的诗    从上一轮看看有没有作者"""
        author = None
        now_poem_info_value = return_variable_value("now_poem_info")
        if now_poem_info_value:
            now_poem_info = json.loads(now_poem_info_value)
            if now_poem_info.__contains__("作者"):
                author = now_poem_info["作者"]
        if not author:
            author = return_slot_value("authorname")
        """上面这种处理逻辑好像有问题 还是得从query中判断有没有他字"""
        return get_one_poetry_new(poem_author=return_slot_value("authorname"),
                                  poem_type=return_slot_value("type"),
                                  poem_anthology=return_slot_value("anthology"),
                                  poem_category=return_slot_value("category"),
                                  poem_dynasty=return_slot_value("dynasty"),
                                  poem_emotion=return_slot_value("emotion"),
                                  poem_faction=return_slot_value("faction"),
                                  poem_genre=return_slot_value("genre"),
                                  poem_theme=return_slot_value("theme"),
                                  poem_expression=return_slot_value("expression"),
                                  poem_titleGroup=return_slot_value("titleGroup"),
                                  poem_reference=return_slot_value("reference"),
                                  poem_TAG=return_slot_value("TAG"),
                                  poem_place=return_slot_value("place"),
                                  poem_person=return_slot_value("person"))

    if current_intent == "GetPoetryByTitle":
        return get_poetry_by_title(poem_title=return_slot_value("title"),
                                   poem_author=return_slot_value("authorname"))

    if current_intent == "GetPoetryByPhrases":
        return get_poetry_by_phrases(poem_content=return_slot_value("content"),
                                     poem_author=return_slot_value("authorname"))

    if current_intent == "GetTransByPhrases":
        content = return_slot_value("content")
        """先看下用户有没有输入content 如果没有则从上一轮会话中查看看content"""
        if not content:
            now_poem_info_value = return_variable_value("now_poem_info")
            if now_poem_info_value:
                now_poem_info = json.loads(now_poem_info_value)
                if now_poem_info.__contains__("历史意图") and now_poem_info["历史意图"] == "get_last_phrases":
                    content = re.findall("[一-龥]+", now_poem_info["上一句"])[0] if now_poem_info.__contains__("上一句") else content
                    now_poem_info["这一句"] = now_poem_info["上一句"]
                    del now_poem_info["上一句"]
                    del now_poem_info["历史意图"]
                    proResult["session"]["variables"]["now_poem_info"]["value"] = json.dumps(now_poem_info, ensure_ascii=False)
                elif now_poem_info.__contains__("历史意图") and now_poem_info["历史意图"] == "get_next_phrases":
                    content = re.findall("[一-龥]+", now_poem_info["下一句"])[0] if now_poem_info.__contains__("下一句") else content
                    now_poem_info["这一句"] = now_poem_info["下一句"]
                    del now_poem_info["下一句"]
                    del now_poem_info["历史意图"]
                    proResult["session"]["variables"]["now_poem_info"]["value"] = json.dumps(now_poem_info, ensure_ascii=False)

                elif now_poem_info.__contains__("这一句"):
                    content = now_poem_info["这一句"]

        return get_trans_by_phrases(poem_content=content,
                                    poem_author=return_slot_value("authorname"))

    if current_intent == "GetCorePhrases":
        poem_title = return_slot_value("title")
        poem_content = return_slot_value("content")
        if not poem_title and not poem_content:
            now_poem_info_value = return_variable_value("now_poem_info")
            if now_poem_info_value:
                now_poem_info = json.loads(now_poem_info_value)
                if now_poem_info.__contains__("题目"):
                    poem_title = now_poem_info["题目"]
        return get_core_phrases(poem_title=poem_title, poem_content=poem_content, steps=5)

    if current_intent == "GetMasterpiece":
        author = return_slot_value("authorname")
        if not author:
            now_poem_info_value = return_variable_value("now_poem_info")
            if now_poem_info_value:
                now_poem_info = json.loads(now_poem_info_value)
                if now_poem_info.__contains__("作者"):
                    author = now_poem_info["作者"]
        return get_master_piece(poem_author=author)

    if current_intent == "GetTranslates":
        title = return_slot_value("title")
        if not title:
            now_poem_info_value = return_variable_value("now_poem_info")
            if now_poem_info_value:
                now_poem_info = json.loads(now_poem_info_value)
                if now_poem_info.__contains__("题目"):
                    title = now_poem_info["题目"]
        return get_translates(poem_title=title,
                              poem_author=return_slot_value("authorname"))

    if current_intent == "GetAuthors":
        author = return_slot_value("authorname")
        if not author:
            now_poem_info_value = return_variable_value("now_poem_info")
            if now_poem_info_value:
                now_poem_info = json.loads(now_poem_info_value)
                if now_poem_info.__contains__("作者"):
                    author = now_poem_info["作者"]

        return get_authors(poem_title=return_slot_value("title"), poem_author=author)

    if current_intent == "GetDynasty":
        poem_author = return_slot_value("authorname")
        if not poem_author:
            now_poem_info_value = return_variable_value("now_poem_info")
            if now_poem_info_value:
                now_poem_info = json.loads(now_poem_info_value)
                if now_poem_info.__contains__("作者"):
                    poem_author = now_poem_info["作者"]  # 上文需要将poet存下来
        return get_dynasty(poem_author=poem_author)

    if current_intent == "GetLastPhrases":
        poem_content = return_slot_value("content")
        if not poem_content:
            now_poem_info_value = return_variable_value("now_poem_info")
            if now_poem_info_value:
                now_poem_info = json.loads(now_poem_info_value)
                if now_poem_info.__contains__("上一句"):
                    poem_content = re.findall("[一-龥]+", now_poem_info["上一句"])[0]
                elif now_poem_info.__contains__("这一句"):
                    poem_content = re.findall("[一-龥]+", now_poem_info["这一句"])[0]
        return get_last_phrases(poem_content=poem_content, steps=5)

    if current_intent == "GetTitles":
        return get_titles(poem_content=return_slot_value("content"))

    if current_intent == "OneMorePoetry":
        return get_one_more_poetry()

    if current_intent == "GetAuthorNames":
        content = return_slot_value("content")
        title = return_slot_value("title")
        """先看下用户有没有输入content和title 如果没有则从上一轮会话中查看看content和title"""
        if not content and not title:
            now_poem_info_value = return_variable_value("now_poem_info")
            if now_poem_info_value:
                now_poem_info = json.loads(now_poem_info_value)
                if now_poem_info.__contains__("这一句"):
                    content = now_poem_info["这一句"]
                elif now_poem_info.__contains__("题目"):
                    title = now_poem_info["题目"]

        if title:
            return get_author_names(poem_title=title)
        elif content:
            return get_author_names(poem_content=content)
        else:
            return get_author_names(poem_content=content, poem_title=title)


if not proResult["session"]:
    proResult["session"] = {"variables": {"query_condition": {"key": "query_condition", "value": ""}}}

if not proResult["session"]["variables"]:
    proResult["session"]["variables"] = {"query_condition": {"key": "query_condition", "value": ""}}

proResult["session"]["variables"]["query_condition"] = {"key": "query_condition",
                                                        "value": json.dumps(modify_query_condition(),
                                                                            ensure_ascii=False)}
