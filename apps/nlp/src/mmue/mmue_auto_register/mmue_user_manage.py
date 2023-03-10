# -*- coding:utf-8 -*-
import json
import random

import requests
import urllib3
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler(filename=f'mmue_user_manage.log', mode="a", encoding="utf-8")
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(module)s] [%(funcName)s]: %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)
urllib3.disable_warnings()


def read_json_file(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        logger.info(f"read json file {file_path} success!")
        return data
    except Exception as e:
        logger.error(f"read json file {file_path} failed! {e}")
        return None


class Base:
    HEADERS = None

    def __init__(self, base_url, username, password):
        self.base_url, self.username, self.__password = base_url, username, password
        self.HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                      "(KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
        self.login_data = None
        self.__login()

    def __request(self, path, headers=HEADERS, *args, **kwargs):
        return requests.request(url=self.base_url + path, headers=headers, verify=False, *args, **kwargs)

    def __login(self):
        response = self.__request(method="POST", path="/mmue/api/login",
                                  json={"username": self.username, "pwd": self.__password,
                                        "captchaid": "5555", "authcode": "5555"})
        if response.status_code == 200:
            response_data = response.json()["data"]
            self.HEADERS["Authorization"] = response_data["token"]
            self.login_data = response_data["data"]
            """enumerate in [user_name, user_id, user_power, tenant_name, tenant_id, tenant_logo, otype]"""
            logger.info(f"user {self.username} login success!")
            return True
        else:
            logger.error(f"user {self.username} login failed!")
            self.login_data = None
            return False

    def mmue_request(self, path, *args, **kwargs):
        response = self.__request(path=path, *args, **kwargs)
        logger.info(f'{kwargs.get("method")} {response.status_code} => {path}')
        if response.status_code >= 400:
            try:
                logger.error(f'error message => {response.json()}')
            except Exception as e:
                logger.error(f'error message => {response.content} {e}')
        return response


class UserManage(Base):
    def __init__(self, base_url, username, password):
        super().__init__(base_url, username, password)
        auth_info = {"username": self.username, "userid": self.login_data["user_id"], "lang": "zh-CN", "agentid": None}

        """sv ????????????auth info  ?????????sv??????????????????headers???????????? self.HEADERS  ?????????mmue???????????????????????????"""
        self.HEADERS["authinfo"] = json.dumps(auth_info, ensure_ascii=False)

    def user_add_new(self, username, password, tenant_code):
        """
        ?????? MMUE ??????
        :param username: ?????????
        :param password: ??????
        :param tenant_code: ????????????
        :return: ?????? id
        """
        url = "/mmue/api/sso/create/user"
        payload = {
            "username": username,
            "password": password,
            "tenantcode": tenant_code
        }
        response = self.mmue_request(method="POST", path=url, json=payload)
        if response.status_code != 200:
            logger.error(f"request to {url} failed with status code {response.status_code}")
            return None
        res = response.json()
        if res["status"]:
            user_id = response.json()["data"]
            logger.info(f"user {username} create succeed: user_id={user_id}")
            return user_id
        else:
            logger.warning(f"user {username} create failed reason: {res['msg']}")
            return None

    def get_tenant_list(self):  # unusable ?????????
        """?????? ????????????"""
        url = "/mmue/api/tenant"
        return self.mmue_request(method="POST", path=url)

    def get_scene_list(self):
        """?????? ??????????????????"""
        url = "/sv-api/v2/ux/scenetpl/list?keyword="
        return self.mmue_request(method="GET", path=url, headers=self.HEADERS)

    def get_robot_char_list(self):
        """?????? ??????????????????"""
        url = "/mmue/api/robotchar/search"
        payload = {"char_name": ""}
        return self.mmue_request(method="POST", path=url + f"?token={self.HEADERS['Authorization']}", json=payload)

    def get_skill_type_list(self):
        """?????? ??????????????????"""
        url = "/sv-api/v2/ux/skilltpl/list?keyword="
        return self.mmue_request(method="GET", path=url, headers=self.HEADERS)

    def get_dm_template_list(self):
        """?????? DM??????????????????"""
        url = "/sv-api/v2/ux/dmtemplate/list?page=1&pagesize=100000&keyword="
        return self.mmue_request(method="GET", path=url, headers=self.HEADERS)

    def agent_add_new(self, tenant_code, agent_name, scenetplid, scenecharid, skilltplid,
                      language, timezone, longitude, latitude, dm_name):
        """
        ????????????
        :param tenant_code: ????????????
        :param agent_name: ????????????
        :param scenetplid: ????????????      id     get_scene_list()
        :param skilltplid: ????????????      id     get_skill_type_list()
        :param scenecharid: ????????????     id     get_robot_char_list()
        :param language: ??????     zh-CN
        :param timezone: ??????     UTC+8
        :param longitude: ??????
        :param latitude: ??????
        :param dm_name: DM??????                 get_dm_template_list()
        :return: agent_id: ??????id
        """
        url = "/sv-api/v2/ux/agents/add"
        try:
            payload = {"tenantcode": tenant_code,
                       "agentname": agent_name,
                       "dflanguage": "zh-CN",
                       "language": language,
                       "latitude": str(latitude),
                       "longitude": str(longitude),
                       "dmName": dm_name,
                       "timezone": timezone,
                       "scenetplid": int(scenetplid),  # ????????????
                       "scenecharid": int(scenecharid),
                       "skilltplid": int(skilltplid)}
        except Exception as e:
            logger.error(f"input param error: {e}")
            return None
        response = self.mmue_request(method="POST", path=url, json=payload, headers=self.HEADERS)
        if response.status_code != 200:
            logger.error(f"request to {url} failed with status code {response.status_code}")
            return None
        res = response.json()
        if not res["status"]:
            logger.warning(f"agent {payload['agentname']} create failed reason: {res['msg']}")
            return None
        agent_id = res["id"]
        logger.info(f"agent {payload['agentname']} create succeed: agent_id={agent_id}")
        return agent_id

    def get_agent_info(self, agent_id):
        """?????? ????????????"""
        url = f"/sv-api/v2/ux/agents/{agent_id}"
        return self.mmue_request(method="GET", path=url, headers=self.HEADERS)

    def get_agent_id_by_name(self, agent_name):
        url = f"/sv-api/v2/ux/agents?tenantcode=&scenecharid=0&agentname={agent_name}&agentid=0&page=100&pagesize=1"
        response = self.mmue_request(method="GET", path=url, headers=self.HEADERS)
        if response.status_code != 200:
            return None
        res = response.json()
        for r in res["data"]:
            if r["agentname"] == agent_name:
                return r["id"]
        return None

    def list_permissions(self):
        """?????? admin ??? user ???????????????"""
        url = "/mmue/api/permission/list"
        payload = {"system": "mmo", "component": "/app/client#/roles"}
        return self.mmue_request(method="POST", path=url + f"?token={self.HEADERS['Authorization']}", json=payload)

    def get_faq_cate(self):
        """?????? ?????????????????????"""
        url = "/main/fqacate/faqcate"
        return self.mmue_request(method="GET", path=url + f"?token={self.HEADERS['Authorization']}")

    def list_graphs(self):
        """?????? ?????????????????????"""
        url = "/graph/kg/v1/graph/list"
        payload = {"spaceName": ""}
        return self.mmue_request(method="POST", path=url, json=payload)

    def get_entity_qa_cate(self):
        """?????? ??????????????????"""
        url = "/main/entityqacate/entityqacatetreelist"
        return self.mmue_request(method="GET", path=url + f"?token={self.HEADERS['Authorization']}")

    def agent_update(self, payload):
        """?????? ????????????
        payload = {"tenantcode": "cloudminds", "agentname": "lisi", "dflanguage": "zh-CN", "language": "zh-CN",
                   "latitude": "4", "longitude": "3", "dmName": "standard", "timezone": "UTC+8", "scenetplid": 1,
                   "scenecharid": 32, "skilltplid": 1,
                   # ?????????????????????????????????payload????????????

                   # ???????????????????????????agent?????????????????????
                   "eqaids": [10],

                   # get_faq_cate()
                   "fqaids": [188, 269, 258, 226, 210, 267, 190, 268, 189, 266],

                   # list_graphs()
                   "kgnames": ["common_kg", "db_12429135405209477533", "db_271003567416724429",
                               "zidingyitupu_479963348332101988", "shici_1549937929118056448",
                               "suibiandingyitupu_1551405104245309440",
                               "wangqiangdeceshizhishitupu_5177935683873814830", "db_7338609727454445713",
                               "db_9313390819905066577", "gushi_1555466196884180992", "db_10080664782208135874",
                               "shiciceshi_1557598135343026176", "gushici_1557614812554235904"], "agentid": 1635}
        """
        url = "/sv-api/v2/ux/agents/update"
        return self.mmue_request(method="PATCH", path=url, json=payload)

    def get_custom_robot_labels(self):
        """?????????????????????????????????"""
        url = "/mmue/api/robotcharvar/list"
        return self.mmue_request(method="POST", path=url)

    def save_custom_robot_labels(self, payload):
        """???????????????????????????
                payload = {"robotCharvarList": [
            {"var_label": "???????????????", "var_name": "robotname", "var_desc": "??????????????????", "var_type": "string",
             "var_value": "??????"},
            {"var_label": "??????", "var_name": "character", "var_desc": "???????????????", "var_type": "string",
             "var_value": ""},
            {"var_label": "??????", "var_name": "gender", "var_desc": "???????????????", "var_type": "string",
             "var_value": ""},
            {"var_label": "??????", "var_name": "robot.nickname", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "???", "var_name": "robot.lastname", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "?????????", "var_name": "robot.ename", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "birthday", "var_desc": "?????????????????????????????????????????????????????????????????????",
             "var_type": "date", "var_value": ""},
            {"var_label": "??????", "var_name": "age", "var_desc": "???????????????", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "zodiac", "var_desc": "???????????????", "var_type": "string",
             "var_value": ""},
            {"var_label": "??????", "var_name": "robot.constellation", "var_desc": "???????????????", "var_type": "string",
             "var_value": ""},
            {"var_label": "??????", "var_name": "blood.type", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "motherland", "var_desc": "?????????????????????", "var_type": "string",
             "var_value": ""},
            {"var_label": "??????", "var_name": "nationality", "var_desc": "?????????????????????", "var_type": "string",
             "var_value": ""},
            {"var_label": "??????", "var_name": "native.language", "var_desc": "?????????????????????", "var_type": "string",
             "var_value": ""},
            {"var_label": "??????", "var_name": "hometown", "var_desc": "?????????????????????", "var_type": "string",
             "var_value": ""},
            {"var_label": "??????", "var_name": "native.dialect", "var_desc": "?????????????????????", "var_type": "string",
             "var_value": ""},
            {"var_label": "?????????", "var_name": "current.location", "var_desc": "???SV??????????????????????????????????????????",
             "var_type": "string", "var_value": ""},
            {"var_label": "?????????", "var_name": "current.address", "var_desc": "???SV??????????????????????????????????????????",
             "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "phone", "var_desc": "?????????????????????????????????TTS????????????????????????????????????",
             "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "email", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "wechat", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "????????????", "var_name": "social.media", "var_desc": "", "var_type": "string",
             "var_value": ""},
            {"var_label": "??????", "var_name": "father", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "mother", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "family", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "relative", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "husband", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "Wife", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "?????????", "var_name": "boyfriend", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "?????????", "var_name": "girlfriend", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "friend", "var_desc": "???????????????????????????????????????", "var_type": "string",
             "var_value": ""},
            {"var_label": "??????", "var_name": "robot.height", "var_desc": "?????????????????????", "var_type": "string",
             "var_value": ""},
            {"var_label": "??????", "var_name": "robot.weight", "var_desc": "?????????????????????", "var_type": "string",
             "var_value": ""},
            {"var_label": "??????", "var_name": "skincolor", "var_desc": "?????????????????????", "var_type": "string",
             "var_value": ""},
            {"var_label": "??????", "var_name": "use", "var_desc": "?????????????????????", "var_type": "string",
             "var_value": ""},
            {"var_label": "??????", "var_name": "IQ", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "advantage", "var_desc": "??????????????????????????????", "var_type": "string",
             "var_value": ""},
            {"var_label": "??????", "var_name": "disadvantage", "var_desc": "??????????????????????????????", "var_type": "string",
             "var_value": ""},
            {"var_label": "?????????", "var_name": "motto", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "secret", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "dream", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "soul", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "hobby", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "idol", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "???????????????", "var_name": "fav.food", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "???????????????", "var_name": "fav.color", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "???????????????", "var_name": "fav.game", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "???????????????", "var_name": "fav.sport", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "???????????????", "var_name": "fav.writer", "var_desc": "", "var_type": "string",
             "var_value": ""},
            {"var_label": "???????????????", "var_name": "fav.book", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "???????????????", "var_name": "fav.film", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "???????????????", "var_name": "fav.singer", "var_desc": "", "var_type": "string",
             "var_value": ""},
            {"var_label": "???????????????", "var_name": "fav.music", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "?????????", "var_name": "edu.school", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "edu.degree", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "edu.major", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "employer", "var_desc": "???????????????", "var_type": "string",
             "var_value": ""},
            {"var_label": "??????", "var_name": "boss", "var_desc": "???????????????", "var_type": "string", "var_value": ""},
            {"var_label": "??????", "var_name": "job", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "????????????", "var_name": "worktime", "var_desc": "", "var_type": "time_range",
             "var_value": ""}], "vals": [{"var_name": "robotname", "var_value": "??????"}], "agent_id": "1635"}
        """
        url = "/mmue/api/robotcharagent/saveval"
        return self.mmue_request(method="POST", path=url, json=payload)

    def bind_agents_to_user(self, username, agents):
        """?????????????????????
        payload = {
                  "user_name": "wangerxiao",
                  "agent_ids": ["1638", "1639"]
                 }
        """
        url = "/mmue/api/agent/bind"
        payload = {"user_name": username, "agent_ids": agents}
        response = self.mmue_request(method="POST", path=url + f"?token={self.HEADERS['Authorization']}", json=payload)
        try:
            res = response.json()
            if not res["status"]:
                logger.error(f"bind agents to user failed reason: {res['msg']}")
                return False
            return True

        except Exception as e:
            logger.error(f"bind agents to user failed reason: {e}")
            return False


def auto_add_user_by_config():
    """????????????MMUE?????????
    1.????????????MMUE
    2.???????????? ?????????agentID
    3.???????????? ??????????????????
    4.????????????????????????
    """
    mmue_platform_info = read_json_file("conf_env_list.json")
    user_list_info = read_json_file("conf_user_list.json")

    if mmue_platform_info and user_list_info:
        env_label = mmue_platform_info["env_label"]
        env_info = mmue_platform_info["mmue"][env_label]
        user_list = user_list_info["users"]
    else:
        return False

    """1.????????????MMUE"""
    instance = UserManage(base_url=env_info["base_url"],
                          username=env_info["username"],
                          password=env_info["password"])

    logger.info("it will create users as follows:")
    logger.info(f"user_list={json.dumps(user_list)}")
    succeed_user = []
    failed_user = []
    for user in user_list:
        """2.???????????? ?????????agentID"""
        agent_id = instance.agent_add_new(agent_name=user["username"],
                                          tenant_code=env_info["tenant_code"],
                                          scenetplid=env_info["scenetplid"],
                                          scenecharid=env_info["scenecharid"],
                                          skilltplid=env_info["skilltplid"],
                                          language=env_info["language"],
                                          timezone=env_info["timezone"],
                                          longitude=env_info["longitude"],
                                          latitude=env_info["latitude"],
                                          dm_name=env_info["dm_name"])

        """2.1?????????????????????????????????????????????????????????????????????"""
        if not agent_id:
            new_name = user["username"] + str(random.randint(1, 1000))
            logger.error(f"user {user['username']} try to create agent "
                         f"agent_name={user['username']} failed reason: agent_add_new exec failed!")
            logger.info(f"user {user['username']} retry to create new agent: agent_name={new_name}")
            agent_id = instance.agent_add_new(agent_name=new_name,
                                              tenant_code=env_info["tenant_code"],
                                              scenetplid=env_info["scenetplid"],
                                              scenecharid=env_info["scenecharid"],
                                              skilltplid=env_info["skilltplid"],
                                              language=env_info["language"],
                                              timezone=env_info["timezone"],
                                              longitude=env_info["longitude"],
                                              latitude=env_info["latitude"],
                                              dm_name=env_info["dm_name"])

        if not agent_id:
            logger.error(f"user {user['username']} try to create agent failed reason: agent_add_new exec failed!")
            break

        """3.???????????? ??????????????????"""
        user_id = instance.user_add_new(username=user["username"],
                                        password=user["password"],
                                        tenant_code=env_info["tenant_code"])
        if not user_id:
            logger.error(f"user {user['username']} create mmue user failed reason: user_add_new exec failed!")
            break

        """4.????????????????????????"""
        logger.info(f"start bind role and user: user_name={user['username']}, user_id={user_id}, agent_id={agent_id}")

        result = instance.bind_agents_to_user(user['username'], [f"{agent_id}"])
        if not result:
            logger.error(f"user {user['username']} create failed reason: bind_agents_to_user exec failed!")
            break
        logger.info(f"bind role and user succeed: user_name={user['username']}, user_id={user_id}, agent_id={agent_id}")
        logger.info(f"this user create finished: user_name={user['username']}, user_id={user_id}, agent_id={agent_id}")
        succeed_user.append(user)

    logger.info(f"all user create finished!")
    logger.info(f"succeed user_list={json.dumps(succeed_user)}")
    logger.warning(f"failed user_list={json.dumps([item for item in user_list if item not in succeed_user])}")


if __name__ == '__main__':
    auto_add_user_by_config()
