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

        """sv 接口需要auth info  在调用sv接口时，需给headers重新赋值 self.HEADERS  在调用mmue接口时不需要此操作"""
        self.HEADERS["authinfo"] = json.dumps(auth_info, ensure_ascii=False)

    def user_add_new(self, username, password, tenant_code):
        """
        注册 MMUE 用户
        :param username: 用户名
        :param password: 密码
        :param tenant_code: 租户名称
        :return: 用户 id
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

    def get_tenant_list(self):  # unusable 不可用
        """获取 租户列表"""
        url = "/mmue/api/tenant"
        return self.mmue_request(method="POST", path=url)

    def get_scene_list(self):
        """获取 客户场景列表"""
        url = "/sv-api/v2/ux/scenetpl/list?keyword="
        return self.mmue_request(method="GET", path=url, headers=self.HEADERS)

    def get_robot_char_list(self):
        """获取 场景人设列表"""
        url = "/mmue/api/robotchar/search"
        payload = {"char_name": ""}
        return self.mmue_request(method="POST", path=url + f"?token={self.HEADERS['Authorization']}", json=payload)

    def get_skill_type_list(self):
        """获取 技能类型列表"""
        url = "/sv-api/v2/ux/skilltpl/list?keyword="
        return self.mmue_request(method="GET", path=url, headers=self.HEADERS)

    def get_dm_template_list(self):
        """获取 DM流程模板列表"""
        url = "/sv-api/v2/ux/dmtemplate/list?page=1&pagesize=100000&keyword="
        return self.mmue_request(method="GET", path=url, headers=self.HEADERS)

    def agent_add_new(self, tenant_code, agent_name, scenetplid, scenecharid, skilltplid,
                      language, timezone, longitude, latitude, dm_name):
        """
        角色创建
        :param tenant_code: 租户名称
        :param agent_name: 角色名称
        :param scenetplid: 客户场景      id     get_scene_list()
        :param skilltplid: 技能类型      id     get_skill_type_list()
        :param scenecharid: 场景人设     id     get_robot_char_list()
        :param language: 语言     zh-CN
        :param timezone: 时区     UTC+8
        :param longitude: 经度
        :param latitude: 纬度
        :param dm_name: DM流程                 get_dm_template_list()
        :return: agent_id: 角色id
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
                       "scenetplid": int(scenetplid),  # 客户场景
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
        """获取 角色信息"""
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
        """获取 admin 和 user 的权限列表"""
        url = "/mmue/api/permission/list"
        payload = {"system": "mmo", "component": "/app/client#/roles"}
        return self.mmue_request(method="POST", path=url + f"?token={self.HEADERS['Authorization']}", json=payload)

    def get_faq_cate(self):
        """获取 知识库配置列表"""
        url = "/main/fqacate/faqcate"
        return self.mmue_request(method="GET", path=url + f"?token={self.HEADERS['Authorization']}")

    def list_graphs(self):
        """获取 知识图谱库列表"""
        url = "/graph/kg/v1/graph/list"
        payload = {"spaceName": ""}
        return self.mmue_request(method="POST", path=url, json=payload)

    def get_entity_qa_cate(self):
        """获取 实体问答列表"""
        url = "/main/entityqacate/entityqacatetreelist"
        return self.mmue_request(method="GET", path=url + f"?token={self.HEADERS['Authorization']}")

    def agent_update(self, payload):
        """更新 角色信息
        payload = {"tenantcode": "cloudminds", "agentname": "lisi", "dflanguage": "zh-CN", "language": "zh-CN",
                   "latitude": "4", "longitude": "3", "dmName": "standard", "timezone": "UTC+8", "scenetplid": 1,
                   "scenecharid": 32, "skilltplid": 1,
                   # 前面的数据和创建用户时payload是一样的

                   # 这个参数好像也是查agent的时候查出来的
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
        """获取机器人人设标签列表"""
        url = "/mmue/api/robotcharvar/list"
        return self.mmue_request(method="POST", path=url)

    def save_custom_robot_labels(self, payload):
        """保存机器人人设标签
                payload = {"robotCharvarList": [
            {"var_label": "机器人名称", "var_name": "robotname", "var_desc": "必填，且唯一", "var_type": "string",
             "var_value": "李四"},
            {"var_label": "性格", "var_name": "character", "var_desc": "与人设有关", "var_type": "string",
             "var_value": ""},
            {"var_label": "性别", "var_name": "gender", "var_desc": "与人设有关", "var_type": "string",
             "var_value": ""},
            {"var_label": "绰号", "var_name": "robot.nickname", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "姓", "var_name": "robot.lastname", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "英文名", "var_name": "robot.ename", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "生日", "var_name": "birthday", "var_desc": "默认达闼成立日期，也可植入客户信息（创始日期）",
             "var_type": "date", "var_value": ""},
            {"var_label": "年龄", "var_name": "age", "var_desc": "与生日有关", "var_type": "string", "var_value": ""},
            {"var_label": "生肖", "var_name": "zodiac", "var_desc": "与生日有关", "var_type": "string",
             "var_value": ""},
            {"var_label": "星座", "var_name": "robot.constellation", "var_desc": "与生日有关", "var_type": "string",
             "var_value": ""},
            {"var_label": "血型", "var_name": "blood.type", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "国籍", "var_name": "motherland", "var_desc": "可能与语种有关", "var_type": "string",
             "var_value": ""},
            {"var_label": "民族", "var_name": "nationality", "var_desc": "可能与国籍有关", "var_type": "string",
             "var_value": ""},
            {"var_label": "语种", "var_name": "native.language", "var_desc": "可能与国籍有关", "var_type": "string",
             "var_value": ""},
            {"var_label": "家乡", "var_name": "hometown", "var_desc": "可能与方言有关", "var_type": "string",
             "var_value": ""},
            {"var_label": "方言", "var_name": "native.dialect", "var_desc": "可能与家乡有关", "var_type": "string",
             "var_value": ""},
            {"var_label": "所在地", "var_name": "current.location", "var_desc": "与SV经纬度有关，层级至少写到城市",
             "var_type": "string", "var_value": ""},
            {"var_label": "居住地", "var_name": "current.address", "var_desc": "与SV经纬度有关，层级至少写到城市",
             "var_type": "string", "var_value": ""},
            {"var_label": "电话", "var_name": "phone", "var_desc": "大写汉字，有停顿（不然TTS容易误读为数字而非号码）",
             "var_type": "string", "var_value": ""},
            {"var_label": "邮箱", "var_name": "email", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "微信", "var_name": "wechat", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "社交账号", "var_name": "social.media", "var_desc": "", "var_type": "string",
             "var_value": ""},
            {"var_label": "父亲", "var_name": "father", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "母亲", "var_name": "mother", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "家人", "var_name": "family", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "亲属", "var_name": "relative", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "老公", "var_name": "husband", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "老婆", "var_name": "Wife", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "男朋友", "var_name": "boyfriend", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "女朋友", "var_name": "girlfriend", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "朋友", "var_name": "friend", "var_desc": "可以写同一空间的其他机器人", "var_type": "string",
             "var_value": ""},
            {"var_label": "身高", "var_name": "robot.height", "var_desc": "可能与机型有关", "var_type": "string",
             "var_value": ""},
            {"var_label": "体重", "var_name": "robot.weight", "var_desc": "可能与机型有关", "var_type": "string",
             "var_value": ""},
            {"var_label": "肤色", "var_name": "skincolor", "var_desc": "可能与机型有关", "var_type": "string",
             "var_value": ""},
            {"var_label": "用途", "var_name": "use", "var_desc": "可能与机型有关", "var_type": "string",
             "var_value": ""},
            {"var_label": "智商", "var_name": "IQ", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "优点", "var_name": "advantage", "var_desc": "可能与人设或技能相关", "var_type": "string",
             "var_value": ""},
            {"var_label": "缺点", "var_name": "disadvantage", "var_desc": "可能与人设或技能相关", "var_type": "string",
             "var_value": ""},
            {"var_label": "座右铭", "var_name": "motto", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "秘密", "var_name": "secret", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "梦想", "var_name": "dream", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "灵魂", "var_name": "soul", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "兴趣", "var_name": "hobby", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "偶像", "var_name": "idol", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "喜欢的食物", "var_name": "fav.food", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "喜爱的颜色", "var_name": "fav.color", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "喜欢的游戏", "var_name": "fav.game", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "喜爱的运动", "var_name": "fav.sport", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "喜欢的作家", "var_name": "fav.writer", "var_desc": "", "var_type": "string",
             "var_value": ""},
            {"var_label": "喜欢的书籍", "var_name": "fav.book", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "喜欢的电影", "var_name": "fav.film", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "喜欢的歌手", "var_name": "fav.singer", "var_desc": "", "var_type": "string",
             "var_value": ""},
            {"var_label": "喜欢的音乐", "var_name": "fav.music", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "学校名", "var_name": "edu.school", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "学历", "var_name": "edu.degree", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "专业", "var_name": "edu.major", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "公司", "var_name": "employer", "var_desc": "与老板有关", "var_type": "string",
             "var_value": ""},
            {"var_label": "老板", "var_name": "boss", "var_desc": "与公司相关", "var_type": "string", "var_value": ""},
            {"var_label": "职业", "var_name": "job", "var_desc": "", "var_type": "string", "var_value": ""},
            {"var_label": "工作时间", "var_name": "worktime", "var_desc": "", "var_type": "time_range",
             "var_value": ""}], "vals": [{"var_name": "robotname", "var_value": "李四"}], "agent_id": "1635"}
        """
        url = "/mmue/api/robotcharagent/saveval"
        return self.mmue_request(method="POST", path=url, json=payload)

    def bind_agents_to_user(self, username, agents):
        """绑定用户与角色
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
    """自动注册MMUE步骤：
    1.超管登录MMUE
    2.创建角色 获取到agentID
    3.创建用户 获取到用户名
    4.绑定角色与用户组
    """
    mmue_platform_info = read_json_file("conf_env_list.json")
    user_list_info = read_json_file("conf_user_list.json")

    if mmue_platform_info and user_list_info:
        env_label = mmue_platform_info["env_label"]
        env_info = mmue_platform_info["mmue"][env_label]
        user_list = user_list_info["users"]
    else:
        return False

    """1.超管登录MMUE"""
    instance = UserManage(base_url=env_info["base_url"],
                          username=env_info["username"],
                          password=env_info["password"])

    logger.info("it will create users as follows:")
    logger.info(f"user_list={json.dumps(user_list)}")
    succeed_user = []
    failed_user = []
    for user in user_list:
        """2.创建角色 获取到agentID"""
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

        """2.1如果存在同名的角色时，给角色名加个随机数字后缀"""
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

        """3.创建用户 获取到用户名"""
        user_id = instance.user_add_new(username=user["username"],
                                        password=user["password"],
                                        tenant_code=env_info["tenant_code"])
        if not user_id:
            logger.error(f"user {user['username']} create mmue user failed reason: user_add_new exec failed!")
            break

        """4.绑定角色与用户组"""
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
