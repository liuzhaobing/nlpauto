# -*- coding:utf-8 -*-

import json
import time

from apps.nlp.src.mmue.mmue_common.mmue_base import Base
from utils.handler import Handlers


class KG(Base):
    def search_kg_entity(self, space_en="gushitupu_4211540538733424010", entity_name="白雪公主"):
        """查询指定关键字的实体列表"""
        self.HEADERS["authinfo"] = json.dumps({"userid": self.login_data["user_id"], "username": self.username,
                                               "lang": "zh-CN", "agentid": 1})
        payload = {"space": space_en, "name": entity_name, "disambi": "", "ot_id": "", "sorted_by": "name",
                   "page_no": 1, "page_size": 50}
        url = "/graph/kg/v1/entity/list"
        return self.mmue_request(method="POST", path=url, json=payload, headers=self.HEADERS)

    def inspect_entity_attr(self, space_en, entity_id):
        """查询指定实体的属性信息"""
        self.HEADERS["authinfo"] = json.dumps({"userid": self.login_data["user_id"], "username": self.username,
                                               "lang": "zh-CN", "agentid": 1})
        url = "/graph/kg/v1/ea/list"
        payload = {"space": space_en, "entity_id": entity_id, "status": 0,
                   "page_no": 1, "page_size": 50}
        return self.mmue_request(method="POST", path=url, json=payload, headers=self.HEADERS)

    def update_entity_attr(self, space_en, id, e_id, ot_attr_id, value):
        """更新指定实体的单个属性值"""
        self.HEADERS["authinfo"] = json.dumps({"userid": self.login_data["user_id"], "username": self.username,
                                               "lang": "zh-CN", "agentid": 1})
        url = "/graph/kg/v1/ea/upsert"
        payload = {"space": space_en, "id": id,
                   "e_id": e_id, "ot_attr_id": ot_attr_id, "value": value, "status": 1, "failure_cause": "",
                   "is_del": False, "ori_status": 1}
        return self.mmue_request(method="POST", path=url, json=payload, headers=self.HEADERS)

    def manual_update(self, entity_name):
        """由于某些值没写到图数据库 手动导一下 中文故事
        """
        space_en = "gushitupu_4211540538733424010"
        res = self.search_kg_entity(space_en, entity_name)
        try:
            "1587334569562079232"
            entity_id = res.json()["data"]["data"][0]["id"]
            res2 = self.inspect_entity_attr(space_en, entity_id)
            try:
                attrs = res2.json()["data"]["attrs"]
                for at in attrs:
                    if at["ot_attr_name"] == "中文故事":
                        id = at["id"]
                        ot_attr_id = at["ot_attr_id"]
                        e_id = at["e_id"]
                        value = at["value"]
                        res3 = self.update_entity_attr(space_en, id, e_id, ot_attr_id, value)
                        print(res3.json()["code"])
                        break
            except:
                pass
        except:
            return

    def search_sys_entity(self):
        url = "/sv-api/v2/ux/agents/1/entities/5438/entityitems?page=1&pagesize=228&entityid=5438&keyword="
        self.HEADERS["authinfo"] = json.dumps({"userid": self.login_data["user_id"], "username": self.username,
                                               "lang": "zh-CN", "agentid": 1})
        response_data = self.mmue_request(method="GET", path=url, headers=self.HEADERS).json()["data"]
        return response_data

    def check(self):
        results = []
        res = self.search_sys_entity()
        for item in res:
            time.sleep(0.5)
            title = item["itemname"]
            query = f"讲一个{title}的故事"
            try:
                result = self.talk(payload={"text": query,
                                            "agent_id": 666,
                                            "env": "87",
                                            "tanant_code": "cloudminds",
                                            "event_type": 0,
                                            "robot_id": "5C1AEC03573747D",
                                            "session_id": "liuzhaobing@cloudminds",
                                            "event_info": {}})
                answer_text = result.json()["data"]["data"]["tts"][0]["text"]
                if len(answer_text) <= 30:
                    is_pass = False
                    self.manual_update(title)
                else:
                    is_pass = True

                results.append({
                    "title": title,
                    "query": query,
                    "answer_text": answer_text,
                    "is_pass": is_pass
                })
                print(f"title -> {title}\n")
                print(f"answer -> {answer_text}\n")
            except:
                continue
        Handlers.write_list_map_as_excel(results, excel_writer="story.xlsx", sheet_name="Sheet1", index=False)


if __name__ == '__main__':
    instance = KG(base_url="https://mmue-dit87.harix.iamidata.com", username="liuzhaobing", password="123456")
    instance.check()