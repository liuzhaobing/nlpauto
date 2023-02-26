# -*- coding:utf-8 -*-
from test_rec import *
from utils.handler import Handlers
import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        redis_info = {'host': '172.16.23.85', 'port': 31961}
        self.instance = Personas(redis_info)
        self.instance2 = MockAlgoInterface()

    def tearDown(self) -> None:
        pass

    def music(self, l_empty, l_singer=None, l_song=None, l_song_type=None):
        # 指定用户id
        user_id = "233"
        # 随机构造音乐相关喜好
        system_skill_recent_info, system_skill_mine_info = mock_rec_music_history_randomly_full()

        if l_song:
            for k, v in system_skill_mine_info["music"]["like"]["song"].items():
                system_skill_mine_info["music"]["like"]["song"][k] = l_song
        if l_song_type:
            for k, v in system_skill_mine_info["music"]["like"]["song_type"].items():
                system_skill_mine_info["music"]["like"]["song_type"][k] = l_song_type
        if l_singer:
            for k, v in system_skill_mine_info["music"]["like"]["singer"].items():
                system_skill_mine_info["music"]["like"]["singer"][k] = l_singer
        for item in l_empty:
            system_skill_mine_info["music"]["like"][item] = {}
        # 覆写用户喜好
        self.instance.set_history_attribute_info(user_id, "system_skill_recent_info",
                                                 json.dumps(system_skill_recent_info, ensure_ascii=False))
        self.instance.set_history_attribute_info(user_id, "system_skill_mine_info",
                                                 json.dumps(system_skill_mine_info, ensure_ascii=False))

        # 随机选择城市和对应经纬度
        self.instance2.position_info_map = mock_city_position_randomly()

        # 覆写用户上次访问城市和经纬度
        self.instance.set_history_attribute_info(user_id, "last_access_city", self.instance2.position_info_map["city"])
        self.instance.set_history_attribute_info(user_id, "last_access_time",
                                                 system_skill_recent_info["music"][0]["access_time"])

        # 记录关键信息到result_data
        result_data = {}
        for key in self.instance.action_keys:
            result_data[key] = self.instance.get_history_attribute_info(user_id, key)
            print(key, result_data[key])

        # 记录多轮对话历史
        self.instance2.dialogue_info.append({
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
        self.instance2.user_id = user_id
        now_payload = self.instance2.get_payload()
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

    def test_music_same_singer(self):
        results = []
        empty = ["song", "song_type"]
        l_singer = random.randint(1, 100)
        for i in range(100):
            result = self.music(l_empty=empty, l_singer=l_singer)
            results.append(result)
        file_name = f'./音乐推荐-每个歌手都听了{l_singer}次{time.strftime("%Y-%m-%d-%H-%M-%S")}.xlsx'
        Handlers.write_list_map_as_excel(results,
                                         excel_writer=file_name,
                                         sheet_name="Sheet1",
                                         index=False)

    def test_music_same_song(self):
        results = []
        empty = ["singer", "song_type"]
        l_song = random.randint(1, 100)
        for i in range(100):
            result = self.music(l_empty=empty, l_song=l_song)
            results.append(result)
        file_name = f'./音乐推荐-每首歌曲都听了{l_song}次{time.strftime("%Y-%m-%d-%H-%M-%S")}.xlsx'
        Handlers.write_list_map_as_excel(results,
                                         excel_writer=file_name,
                                         sheet_name="Sheet1",
                                         index=False)

    def test_music_same_songType(self):
        results = []
        empty = ["singer", "song"]
        l_song_type = random.randint(1, 100)
        for i in range(100):
            result = self.music(l_empty=empty, l_song_type=l_song_type)
            results.append(result)
        file_name = f'./音乐推荐-每首歌曲都听了{l_song_type}次{time.strftime("%Y-%m-%d-%H-%M-%S")}.xlsx'
        Handlers.write_list_map_as_excel(results,
                                         excel_writer=file_name,
                                         sheet_name="Sheet1",
                                         index=False)

    def test_music_randomly_not_songType(self):
        results = []
        empty = ["song_type"]
        for i in range(100):
            result = self.music(l_empty=empty)
            results.append(result)
        file_name = f'./音乐推荐-随机听歌手和歌曲不含歌曲类型{time.strftime("%Y-%m-%d-%H-%M-%S")}.xlsx'
        Handlers.write_list_map_as_excel(results,
                                         excel_writer=file_name,
                                         sheet_name="Sheet1",
                                         index=False)

    def test_music_randomly_singer(self):
        results = []
        empty = ["song_type", "song"]
        for i in range(100):
            result = self.music(l_empty=empty)
            results.append(result)
        file_name = f'./音乐推荐-随机听歌手次数{time.strftime("%Y-%m-%d-%H-%M-%S")}.xlsx'
        Handlers.write_list_map_as_excel(results,
                                         excel_writer=file_name,
                                         sheet_name="Sheet1",
                                         index=False)

    def test_music_randomly_song(self):
        results = []
        empty = ["song_type", "singer"]
        for i in range(100):
            result = self.music(l_empty=empty)
            results.append(result)
        file_name = f'./音乐推荐-随机听歌曲次数{time.strftime("%Y-%m-%d-%H-%M-%S")}.xlsx'
        Handlers.write_list_map_as_excel(results,
                                         excel_writer=file_name,
                                         sheet_name="Sheet1",
                                         index=False)

    def test_music_randomly(self):
        results = []
        empty = []
        for i in range(100):
            result = self.music(l_empty=empty)
            results.append(result)
        file_name = f'./音乐推荐-完全随机{time.strftime("%Y-%m-%d-%H-%M-%S")}.xlsx'
        Handlers.write_list_map_as_excel(results,
                                         excel_writer=file_name,
                                         sheet_name="Sheet1",
                                         index=False)


if __name__ == '__main__':
    unittest.main()
