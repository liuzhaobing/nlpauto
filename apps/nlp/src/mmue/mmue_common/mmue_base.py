# -*- coding:utf-8 -*-
import datetime
import json
import requests
import urllib3
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler(filename=f'mmue-{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.log',
                         mode="a", encoding="utf-8")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(module)s] [%(funcName)s]: %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)
urllib3.disable_warnings()


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
            logger.info(f"token={self.HEADERS['Authorization']}")
            self.login_data = response_data["data"]
            """enumerate in [user_name, user_id, user_power, tenant_name, tenant_id, tenant_logo, otype]"""
            logger.info("user login success!")
            return True
        else:
            logger.error("user login failed!")
            self.login_data = None
            return False

    def mmue_request(self, path, *args, **kwargs):
        response = self.__request(path=path, *args, **kwargs)
        logger.debug(f'{kwargs.get("method")} {response.status_code} => {path}')
        if response.status_code >= 400:
            try:
                logger.error(f'error message => {response.json()}')
            except:
                logger.error(f'error message => {response.content}')
        return response

    def talk(self, payload):
        """
        :param payload:  = {"text": "现在几点了",
                           "agent_id": 666,
                           "env": "87",
                           "tanant_code": "cloudminds",
                           "event_type": 0,
                           "robot_id": "5C1AEC03573747D",
                           "session_id": "liuzhaobing@cloudminds",
                           "event_info": {}}
        :return:
        """
        url = "/v1/sv/talk"
        self.HEADERS["authinfo"] = json.dumps({"userid": self.login_data["user_id"], "username": self.username,
                                               "lang": "zh-CN", "agentid": 1})
        return self.mmue_request(method="POST", path=url, json=payload, headers=self.HEADERS)
