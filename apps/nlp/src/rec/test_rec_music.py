# -*- coding:utf-8 -*-
from test_rec import *
from utils.handler import Handlers


def rec_music_test():
    redis_info = {'host': '172.16.23.85', 'port': 31961}
    instance = Personas(redis_info)
    instance2 = MockAlgoInterface()

    # 指定用户id
    user_id = "233"
    # 随机构造音乐相关喜好
    system_skill_recent_info, system_skill_mine_info = mock_rec_music_history_randomly_full()

    for k, v in system_skill_mine_info["music"]["like"]["song"].items():
        system_skill_mine_info["music"]["like"]["song"][k] = 10

    system_skill_mine_info["music"]["like"]["song_type"] = {}
    system_skill_mine_info["music"]["like"]["singer"] = {}

    # 覆写用户喜好
    instance.set_history_attribute_info(user_id, "system_skill_recent_info",
                                        json.dumps(system_skill_recent_info, ensure_ascii=False))
    instance.set_history_attribute_info(user_id, "system_skill_mine_info",
                                        json.dumps(system_skill_mine_info, ensure_ascii=False))

    # 随机选择城市和对应经纬度
    instance2.position_info_map = mock_city_position_randomly()

    # 覆写用户上次访问城市和经纬度
    instance.set_history_attribute_info(user_id, "last_access_city", instance2.position_info_map["city"])
    instance.set_history_attribute_info(user_id, "last_access_time",
                                        system_skill_recent_info["music"][0]["access_time"])

    # 记录关键信息到result_data
    result_data = {}
    for key in instance.action_keys:
        result_data[key] = instance.get_history_attribute_info(user_id, key)
        print(key, result_data[key])

    # 记录多轮对话历史
    instance2.dialogue_info.append({
        "module": "music",
        "source": "system_service",
        "request": "唱首歌",
        "text_emotion": "none",
        "skill_info": {
            "domain": "music",
            "intent": "SongRandomly",
            "paraminfo": []
        },
        "timestamp": f"{int(time.time() * 1000)}"
    })

    # 构造推荐接口request payload
    instance2.user_id = user_id
    now_payload = instance2.get_payload()
    result_data["request payload"] = json.dumps(now_payload, ensure_ascii=False)
    print("request payload", result_data["request payload"])

    # 访问推荐接口进行测试
    now_answer = algo_interface("http://172.16.23.18:31250/multi_modal_recommend", now_payload)

    # 记录关键信息到result_data
    result_data["response cost"] = now_answer[0]
    print("response cost", result_data["response cost"])
    result_data["response json"] = json.dumps(now_answer[-1], ensure_ascii=False)
    print("response json", result_data["response json"])
    result_data["gender"] = now_payload["user_info"]["current_attribute_info"]["gender"]
    result_data["age"] = now_payload["user_info"]["current_attribute_info"]["age"]
    if not now_answer[-1].__contains__("status_code"):
        result_data["recommend_type"] = now_answer[-1]["recommend_type"]
        result_data["music_action"] = now_answer[-1]["answer_info"]["music"]["action_info"]
        result_data["default_recommend"] = now_answer[-1]["recommend_info"]["default_recommend"]
        result_data["geo_location_recommend"] = now_answer[-1]["recommend_info"]["geo_location_recommend"]
        result_data["music_recommend"] = now_answer[-1]["recommend_info"]["music_recommend"]
        result_data["qa_recommend"] = now_answer[-1]["recommend_info"]["qa_recommend"]
    return result_data


if __name__ == '__main__':
    if 1 == 2:
        rec_music_test()
    else:
        data = []
        for i in range(20):
            result_1 = rec_music_test()
            data.append(result_1)
        Handlers.write_list_map_as_excel(data, excel_writer=f'./{time.strftime("%Y-%m-%d-%H-%M-%S")}.xlsx',
                                         sheet_name="Sheet1", index=False)
