# -*- coding:utf-8 -*-
import datetime
import json
import random
import time
import uuid

import redis
import requests


class RedisOperation:
    """
    {'host': '172.16.23.85', 'port': 31961}
    """

    def __init__(self, connect_info):
        self.r = redis.StrictRedis(host=connect_info['host'], port=connect_info['port'], db=0)

    def GET(self, name):
        result = self.r.get(name)
        if not result:
            return None
        return result.decode()

    def SET(self, name, value):
        result = self.r.set(name, value)
        if not result:
            return None
        return result

    def DEL(self, name):
        result = self.r.delete(name)
        if not result:
            return None
        return result

    def HGET(self, name, key):
        result = self.r.hget(name, key)
        if not result:
            return None
        return result.decode()

    def HSET(self, name, key, value):
        result = self.r.hset(name, key, value)
        if not result:
            return None
        return result


class Personas(RedisOperation):
    def __init__(self, connect_info):
        super().__init__(connect_info)
        self.action_keys = ["last_access_time",
                            "last_access_city",
                            "total_access_num",
                            "total_access_duration",
                            "avg_dialog_duration",
                            "query_no_answer",
                            "dressing",
                            "jacket_type",
                            "trousers_type",
                            "shoes",
                            "hair",
                            "glasses",
                            "hat",
                            "mask",
                            "smoke",
                            "trunk",
                            "knapsack",
                            "handbag",
                            "satchel",
                            "emotion",
                            "text_emotion",
                            "gesture",
                            "action",
                            "system_skill_statistics_info",
                            "system_skill_recent_info",
                            "system_skill_mine_info"]

    def get_history_attribute_info(self, user_id, search_key):
        """
        :param user_id:
        :param search_key: [
            "last_access_time",
            "last_access_city",
            "total_access_num",
            "total_access_duration",
            "avg_dialog_duration",
            "query_no_answer",
            "dressing",
            "jacket_type",
            "trousers_type",
            "shoes",
            "hair",
            "glasses",
            "hat",
            "mask",
            "smoke",
            "trunk",
            "knapsack",
            "handbag",
            "satchel",
            "emotion",
            "text_emotion",
            "gesture",
            "action",
            "system_skill_statistics_info",
            "system_skill_recent_info",
            "system_skill_mine_info"
        ]
        :return:
        """
        return self.HGET(name=f"action_{user_id}", key=search_key)

    def set_history_attribute_info(self, user_id, search_key, value):
        return self.HSET(name=f"action_{user_id}", key=search_key, value=value)

    def get_holiday(self, date_str):
        """
        :param date_str: 2022_10_01
        :return: ??????|??????
        """
        return self.GET(name=f"holiday_{date_str}")

    def set_holiday(self, date_str, value):
        """
        :param date_str: 2022_10_01
        :param value: ??????|??????
        :return: True
        """
        return self.SET(f"holiday_{date_str}", value)

    def get_address(self, position_str):
        """
        :param position_str: 104.0610;30.5444
        :return: {"country":"??????","province":"?????????","city":"?????????","area":"?????????","township":"????????????","street":"?????????",
        "number":"52???","formatted_address":"???????????????????????????????????????????????????????????????????????????"}
        """
        return self.GET(name=f"address_{position_str}")

    def set_address(self, position_str, value):
        """
        :param position_str: 104.0610;30.5444
        :param value: {"country":"??????","province":"?????????","city":"?????????","area":"?????????","township":"????????????","street":"?????????",
        "number":"52???","formatted_address":"???????????????????????????????????????????????????????????????????????????"}
        :return: True
        """
        return self.SET(f"address_{position_str}", value)

    def get_weather(self, position_str):
        """
        :param position_str: 104.08;30.65
        :return: {"weather_overall":"??????","temperature":"0???-10???","temp_value":6,"air_quality":"???","air_index":74,
        "ultraviolet":"???????????????","ultraviolet_index":4,"wind_power":"??????","wind_speed":1}
        """
        return self.GET(name=f"weather_{position_str}")

    def set_weather(self, position_str, value):
        """
        :param position_str: 104.08;30.65
        :param value: {"weather_overall":"??????","temperature":"0???-10???","temp_value":6,"air_quality":"???","air_index":74,
        "ultraviolet":"???????????????","ultraviolet_index":4,"wind_power":"??????","wind_speed":1}
        :return: True
        """
        return self.SET(f"weather_{position_str}", value)

    def get_robot_detail(self, tenant_code, roc_user, agent_id, char_id):
        """
        :param tenant_code: ??????
        :param roc_user:
        :param agent_id:??????
        :param char_id:????????????
        :return:
        """
        return self.GET(name=f"robot_char_{tenant_code};{roc_user};{agent_id};{char_id}")

    def set_robot_detail(self, tenant_code, roc_user, agent_id, char_id, value):
        """
        :param tenant_code: ??????
        :param roc_user:
        :param agent_id:??????
        :param char_id:????????????
        :param value:
        :return:
        """
        return self.SET(f"robot_char_{tenant_code};{roc_user};{agent_id};{char_id}", value)


def algo_interface(algo_url, payload):
    """
    :param algo_url: http://172.16.23.18:31250/multi_modal_recommend
    :param payload:{
        "traceid": "b95a7bf7-6cd7-44ea-b0e0-5e43bed9076a",
        "agentid": 1163,
        "sessionid": "admin@cloudminds",
        "user_id": "233",
        "user_info": {
            "current_attribute_info": {
                "id": "233",
                "type": 0,
                "gender": 1,
                "age": 20,
                "name": "test_music"
            }
        },
        "environment_info": {
            "time_interval": "2023-01-16 16:22:52",
            "week": "??????"
        },
        "robot_info": {
            "lng": "104.0800",
            "lat": "30.6500"
        },
        "dialogue_info": [
            {
                "module": "",
                "source": "system_service",
                "request": "?????????",
                "response": "?????????????????????????????????",
                "skill_info": {
                    "domain": "music",
                    "intent": "ask",
                    "paraminfo": [
                        {
                            "name": "song_type",
                            "value": "??????",
                            "entitytype": "sys.rec",
                            "beforevalue": "??????"
                        }
                    ]
                },
                "timestamp": "1673857363482",
                "recommend_info": {
                    "greeting": {},
                    "music": {
                        "action_info": {
                            "slot": {
                                "song_type": "??????",
                                "ask_text": "????????????????????????????????????",
                                "ask_turn": 1
                            },
                            "current_slot": {},
                            "domain": "music",
                            "intent": "ask"
                        }
                    }
                }
            },
            {
                "module": "",
                "source": "system_service",
                "request": "??????",
                "response": "?????????????????????????????????????????????",
                "skill_info": {
                    "domain": "music",
                    "intent": "ask",
                    "paraminfo": [
                        {
                            "name": "singer",
                            "value": "??????????????????",
                            "entitytype": "sys.rec",
                            "beforevalue": "??????????????????"
                        },
                        {
                            "name": "song_type",
                            "value": "??????",
                            "entitytype": "sys.rec",
                            "beforevalue": "??????"
                        }
                    ]
                },
                "timestamp": "1673857369430",
                "recommend_info": {
                    "music": {
                        "action_info": {
                            "current_slot": {
                                "song_type": {
                                    "emotion": "??????"
                                }
                            },
                            "domain": "music",
                            "intent": "ask",
                            "slot": {
                                "ask_text": "????????????????????????????????????????????????",
                                "ask_turn": 2,
                                "singer": "??????????????????"
                            }
                        }
                    },
                    "greeting": {}
                }
            },
            {
                "module": "music",
                "source": "system_service",
                "request": "??????",
                "text_emotion": "none",
                "skill_info": {
                    "domain": "music",
                    "intent": "PlayMusic",
                    "paraminfo": [
                        {
                            "name": "singer",
                            "value": "??????????????????",
                            "entitytype": "sys.rec",
                            "beforevalue": "??????????????????"
                        }
                    ]
                },
                "timestamp": "1673857372468"
            }
        ]
    }
    """
    """:return: {
            "agentid": 1163,
            "answer_info": {
                "greeting": {},
                "music": {
                    "action_info": {
                        "current_slot": {
                            "singer": "??????????????????",
                            "song_type": {
                                "emotion": "??????"
                            }
                        },
                        "domain": "music",
                        "intent": "PlayMusic",
                        "slot": {
                            "NCM_songid": "5266829",
                            "rec_info": {
                                "current_singer": 1100,
                                "current_song_type": 1000,
                                "hot_rand_songs": 0.2
                            },
                            "singer": "??????????????????",
                            "song": "????????????"
                        }
                    }
                }
            },
            "recommend_info": {
                "default_recommend": [
                    "??????????????????",
                    "?????????????????????????????????",
                    "?????????????????????????????????",
                    "?????????????????????"
                ],
                "geo_location_recommend": [
                    "???????????????????????????",
                    "???????????????????????????"
                ],
                "music_recommend": [],
                "qa_recommend": []
            },
            "recommend_type": "music",
            "sessionid": "admin@cloudminds",
            "traceid": "b95a7bf7-6cd7-44ea-b0e0-5e43bed9076a"
        }
    """
    start = time.time()
    response = requests.request(method="POST", url=algo_url, json=payload, verify=False)
    edg_cost = (time.time() - start) * 1000
    if response.status_code == 200:
        return edg_cost, response.json()
    return edg_cost, {"status_code": response.status_code}


def get_year_interface(url, payload):
    """
    :param url: http://172.16.23.30:30732/v1/get_year
    :param payload: {"year": "2023"}
    :return:
    """
    response = requests.request(method="POST", url=url, json=payload)
    if response.status_code == 200:
        try:
            result = response.json()
            return result
        except:
            return None
    return None


def init_holidays(holiday=True, solar_term=False, lunar_festival=False, us_festival=False):
    """???????????????????????????????????????
    :param holiday:
    :param solar_term:
    :param lunar_festival:
    :param us_festival:
    :return:
    """
    redis_holidays = {}
    res = get_year_interface("http://172.16.23.30:30732/v1/get_year", {"tag": "??????"})
    if holiday:
        for holidays in res["holidayList"]:
            year = holidays["startDate"]["year"]
            month = holidays["startDate"]["month"]
            day = holidays["startDate"]["day"]
            if month < 10:
                month = f"0{month}"
            if day < 10:
                day = f"0{day}"
            key = f'{year}-{month}-{day}'
            value = holidays["name"]
            if not redis_holidays.__contains__(key):
                redis_holidays[key] = value
            elif value not in redis_holidays[key]:
                redis_holidays[key] = redis_holidays[key] + "|" + value
    if solar_term:
        for solar_terms in res["solarFestivals"]:
            try:
                value = solar_terms["solarTerm"]
            except:
                value = solar_terms["typeDesc"]
            key = solar_terms["date"]["dateStr"]
            if not redis_holidays.__contains__(key):
                redis_holidays[key] = value
            elif value not in redis_holidays[key]:
                redis_holidays[key] = redis_holidays[key] + "|" + value
    if lunar_festival:
        for lunar_festivals in res["lunarFestivals"]:
            value = lunar_festivals["typeDesc"]
            key = lunar_festivals["date"]["dateStr"]
            if not redis_holidays.__contains__(key):
                redis_holidays[key] = value
            elif value not in redis_holidays[key]:
                redis_holidays[key] = redis_holidays[key] + "|" + value
    if us_festival:
        for us_festivals in res["usFestivals"]:
            value = us_festivals["typeDesc"]
            key = us_festivals["date"]["dateStr"]
            if not redis_holidays.__contains__(key):
                redis_holidays[key] = value
            elif value not in redis_holidays[key]:
                redis_holidays[key] = redis_holidays[key] + "|" + value
    return redis_holidays


def mock_holiday_randomly(holiday=True, solar_term=False, lunar_festival=False, us_festival=False):
    """?????????????????????
    :return: holiday_date, holiday_name
    """
    all_holidays = init_holidays(holiday, solar_term, lunar_festival, us_festival)
    holiday_date = random.choice(list(all_holidays.keys()))
    holiday_name = all_holidays[holiday_date]
    return holiday_date, holiday_name


def mock_city_position_randomly():
    """??????????????????????????????????????????
    :return: {"city": "??????", "longitude": 116.41667, "latitude": 39.91667}
    """
    main_city = [{"city": "??????", "longitude": 116.41667, "latitude": 39.91667},
                 {"city": "??????", "longitude": 121.43333, "latitude": 34.5},
                 {"city": "??????", "longitude": 117.2, "latitude": 39.13333},
                 {"city": "??????", "longitude": 114.1, "latitude": 22.2},
                 {"city": "??????", "longitude": 113.23333, "latitude": 23.16667},
                 {"city": "??????", "longitude": 113.51667, "latitude": 22.3},
                 {"city": "??????", "longitude": 114.06667, "latitude": 22.61667},
                 {"city": "??????", "longitude": 120.2, "latitude": 30.26667},
                 {"city": "??????", "longitude": 106.45, "latitude": 29.56667},
                 {"city": "??????", "longitude": 120.33333, "latitude": 36.06667},
                 {"city": "??????", "longitude": 118.1, "latitude": 24.46667},
                 {"city": "??????", "longitude": 119.3, "latitude": 26.08333},
                 {"city": "??????", "longitude": 103.73333, "latitude": 36.03333},
                 {"city": "??????", "longitude": 106.71667, "latitude": 26.56667},
                 {"city": "??????", "longitude": 113.0, "latitude": 28.21667},
                 {"city": "??????", "longitude": 118.78333, "latitude": 32.05},
                 {"city": "??????", "longitude": 115.9, "latitude": 28.68333},
                 {"city": "??????", "longitude": 123.38333, "latitude": 41.8},
                 {"city": "??????", "longitude": 112.53333, "latitude": 37.86667},
                 {"city": "??????", "longitude": 104.06667, "latitude": 30.66667},
                 {"city": "??????", "longitude": 91.0, "latitude": 29.6},
                 {"city": "????????????", "longitude": 87.68333, "latitude": 43.76667},
                 {"city": "??????", "longitude": 102.73333, "latitude": 25.05},
                 {"city": "??????", "longitude": 108.95, "latitude": 34.26667},
                 {"city": "??????", "longitude": 101.75, "latitude": 36.56667},
                 {"city": "??????", "longitude": 106.26667, "latitude": 38.46667},
                 {"city": "?????????", "longitude": 122.08333, "latitude": 46.06667},
                 {"city": "?????????", "longitude": 126.63333, "latitude": 45.75},
                 {"city": "??????", "longitude": 125.35, "latitude": 43.88333},
                 {"city": "??????", "longitude": 114.31667, "latitude": 30.51667},
                 {"city": "??????", "longitude": 113.65, "latitude": 34.76667},
                 {"city": "?????????", "longitude": 114.48333, "latitude": 38.03333},
                 {"city": "??????", "longitude": 109.5, "latitude": 18.2},
                 {"city": "??????", "longitude": 110.35, "latitude": 20.01667},
                 {"city": "??????", "longitude": 113.5, "latitude": 22.2}]
    return main_city[random.randint(0, len(main_city) - 1)]


class MockAlgoInterface:
    def __init__(self):
        self.user_id = "1867"
        self.user_type = 0
        self.user_gender = random.randint(0, 1)
        self.user_age = random.randint(5, 60)
        self.user_name = "test_music"
        self.agent_id = 666
        self.session_id = None
        self.position_info_map = {"city": "??????", "longitude": 116.41667, "latitude": 39.91667}
        self.now_time = ""
        self.now_date = ""
        self.week = ""
        self.dialogue_info = []

    def get_payload(self):
        self.generate_week_by_time()
        payload = {
            "traceid": f"{uuid.uuid4()}@cloudminds-test.com",
            "agentid": self.agent_id,
            "sessionid": "",
            "user_id": self.user_id,
            "user_info": {"current_attribute_info": {
                "id": self.user_id,
                "type": self.user_type,
                "gender": self.user_gender,
                "age": self.user_age,
                "name": self.user_name,
            }},
            "environment_info": {"time_interval": self.now_time, "week": self.week},
            "robot_info": {"lng": "%.4f" % float(self.position_info_map["longitude"]),
                           "lat": "%.4f" % float(self.position_info_map["latitude"])},
            "dialogue_info": self.dialogue_info
        }
        if not self.session_id:
            payload["sessionid"] = f"{uuid.uuid4()}@cloudminds-test.com"
        return payload

    def generate_week_by_time(self):
        self.now_time = f"{time.strftime('%Y-%m-%d %H:%M:%S')}"
        self.now_date = self.now_time[0:10]
        week_list = ["??????", "??????", "??????", "??????", "??????", "??????", "??????"]
        self.week = week_list[datetime.date(int(self.now_time[0:4]), int(self.now_time[5:7]),
                                            int(self.now_time[8:10])).weekday()]


def mock_rec_music_history_randomly():
    """??????mock??????????????????"""

    def load_json(input_file):
        """????????????????????????json"""
        with open(input_file, "r") as r:
            obj = json.load(r)
            return obj

    """???????????????"""
    file = load_json("./music.json")
    music = file["music"]

    """?????????????????????"""
    access_singer_times = random.randint(1, len(music))

    """?????????????????????"""
    singers = random.sample(music.keys(), access_singer_times)

    """???????????????????????????????????????"""
    like_singer = {}
    like_song = {}
    like_song_type = {}
    last_singer = ""
    last_song = ""
    last_type = ""
    for singer in singers:
        last_singer = singer
        access_song_times = random.randint(1, len(music[singer]))
        now_singer_songs = random.sample(music[singer], access_song_times)
        last_song = now_singer_songs[-1]
        each_song_times = random.sample(range(1, 100), len(now_singer_songs))
        singer_times = 0
        for i in range(len(each_song_times)):
            singer_times += each_song_times[i]
            like_song[now_singer_songs[i]] = each_song_times[i]
            for k, v in file["music_type"].items():
                if now_singer_songs[i] in v:
                    last_type = k
                    if like_song_type.__contains__(k):
                        like_song_type[k] += each_song_times[i]
                    else:
                        like_song_type[k] = each_song_times[i]
                    break
        like_singer[singer] = singer_times

    system_skill_recent_info = {"music": [{"access_time": f"{time.strftime('%Y-%m-%d %H:%M:%S')}",
                                           "slots": {"singer": last_singer, "song": last_song,
                                                     "song_type": last_type}}]}
    system_skill_mine_info = {"music": {
        "like": {"singer": like_singer, "song": like_song, "song_type": like_song_type},
        "dislike": {}}}

    return system_skill_recent_info, system_skill_mine_info


def mock_rec_music_history_randomly_full():
    """??????mock??????????????????"""
    like_singer = {}
    like_song = {}
    like_song_type = {}
    last_singer = ""
    last_song = ""
    last_type = ""

    def load_json(input_file):
        """????????????????????????json"""
        with open(input_file, "r") as r:
            obj = json.load(r)
            return obj

    """???????????????"""
    file = load_json("./music.json")
    music = file["music"]
    all_types = []
    all_songs = []
    for x, y in file["music_type"].items():
        all_songs += y
        all_types.append(x)

    """?????????????????????"""
    singers = random.sample(music.keys(), random.randint(0, len(music)))
    if singers:
        singers_times = random.sample(range(1, 100), len(singers))
        for i in range(len(singers)):
            like_singer[singers[i]] = singers_times[i]
            last_singer = singers[i]

    """???????????????"""
    songs = random.sample(all_songs, random.randint(0, len(all_songs)))
    if songs:
        songs_times = random.sample(range(1, 100), len(songs))
        for i in range(len(songs)):
            like_song[songs[i]] = songs_times[i]
            last_song = songs[i]

    """???????????????"""
    types = random.sample(all_types, random.randint(0, len(all_types)))
    if types:
        for i in range(len(types)):
            like_song_type[types[i]] = random.randint(1, 10)
            last_type = types[i]

    if songs:
        last_song = songs[-1]
    system_skill_recent_info = {"music": [{"access_time": f"{time.strftime('%Y-%m-%d %H:%M:%S')}",
                                           "slots": {"singer": last_singer, "song": last_song,
                                                     "song_type": last_type}}]}
    system_skill_mine_info = {"music": {
        "like": {"singer": like_singer, "song": like_song, "song_type": like_song_type},
        "dislike": {}}}

    return system_skill_recent_info, system_skill_mine_info
