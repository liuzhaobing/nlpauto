#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import requests


class KnowledgeGraph:
    def __init__(self, base_url, login_user, login_passwd, agent_id, agent_name=None):
        self.base_url = base_url  # http://10.11.35.104:4000
        self.login_user = login_user  # "lisha"
        self.login_passwd = login_passwd  # "123456"
        self.agent_id = agent_id  # "1223"
        self.agent_name = agent_name
        self.headers = {}
        self.login()

    def kg_request(self, method, url, *args, **kwargs):
        return requests.request(method=method, url=self.base_url + url, headers=self.headers,
                                verify=False, timeout=10, *args, **kwargs)

    def login(self):
        url = "/main/powerdomain/login"
        payload = {"username": self.login_user, "pwd": self.login_passwd}
        res = self.kg_request(method="POST", url=url, json=payload)
        login_result = res.json()

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Authorization": login_result["data"]["token"],
            "Origin": self.base_url,
            "Referer": self.base_url + "/app/client"
        }
        return self.headers

    def chat(self, query):
        url1 = "/graph/kgqa/v1/chat"
        payload = {"question": query}
        """
        res = {"code": 0,
               "data": {"@type": "type.googleapis.com/kgqa.chat.KgqaResp", "entity_name": "周杰伦", "disambi": "周杰伦",
                        "answer": "周杰伦的母亲是叶惠美",
                        "attr": {"describ": "周杰伦（Jay Chou），1979年1月18日出生于台湾省新北市，中国台湾流行乐男歌手、音乐人、演员、导演、编剧、监制、商人。"}}}
        """
        return self.kg_request("POST", url=url1, json=payload).json()


if __name__ == '__main__':
    t = KnowledgeGraph("http://10.11.35.104:4000", "lisha", "123456", "1223")
    a = t.chat("周杰伦的母亲是谁")
    print(a)
