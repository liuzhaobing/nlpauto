# -*- coding:utf-8 -*-
import copy
import datetime
import json
import requests
from apps.nlp.src.mmue.mmue_common.mmue_base import Base, logger
from utils.handler import Handlers


class SystemService(Base):
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

    def get_domains(self, agent_id=1, search_type="domain", keyword=""):
        url = f"/sv-api/v2/ux/agents/{agent_id}/domains?page=1&pagesize=1000&keyword={keyword}&type={search_type}"
        self.HEADERS["authinfo"] = json.dumps({"userid": self.login_data["user_id"], "username": self.username,
                                               "lang": "zh-CN", "agentid": agent_id})
        return self.mmue_request(method="GET", path=url, headers=self.HEADERS)

    def get_domains_info(self, agent_id=1, search_type="domain", keyword=""):
        datas = self.get_domains(agent_id, search_type, keyword)
        domain_info = []
        if datas.status_code != 200:
            logger.error(f"error with http code {datas.status_code}")
            return domain_info, datas
        try:
            res = datas.json()["data"]
        except Exception as e:
            logger.error(f"json unmarshall failed with error {e}")
            res = []
        if not res:
            return domain_info, datas

        for data in res:
            domain_info.append({"domain_name": data["domainname"], "domain_id": data["id"], "status": data["status"]})
        return domain_info, datas

    def get_intents(self, agent_id=1, domain_id=56, keyword=""):
        url = f"/sv-api/v2/ux/agents/{agent_id}/domains/{domain_id}/intents?page=1&pagesize=1000&keyword={keyword}"
        self.HEADERS["authinfo"] = json.dumps({"userid": self.login_data["user_id"], "username": self.username,
                                               "lang": "zh-CN", "agentid": agent_id})
        return self.mmue_request(method="GET", path=url, headers=self.HEADERS)

    def get_intent_info_by_domain_id(self, agent_id=1, domain_id=56, keyword=""):
        datas = self.get_intents(agent_id, domain_id, keyword)
        intent_info = []
        if datas.status_code != 200:
            logger.error(f"error with http code {datas.status_code}")
            return intent_info, datas
        try:
            res = datas.json()["data"]
        except Exception as e:
            logger.error(f"json unmarshall failed with error {e}")
            res = []
        if not res:
            return intent_info, datas

        for data in res:
            intent_info.append({"intent_name": data["intentname"],
                                "intent_id": data["id"],
                                "input_context": data["inputcontext"]})
        return intent_info, datas

    def get_regexs(self, agent_id=1, domain_id=56, intent_id=8329):
        url = f"/sv-api/v2/ux/agents/{agent_id}/domains/{domain_id}/intents/{intent_id}"
        self.HEADERS["authinfo"] = json.dumps({"userid": self.login_data["user_id"], "username": self.username,
                                               "lang": "zh-CN", "agentid": agent_id})
        return self.mmue_request(method="GET", path=url, headers=self.HEADERS)

    def get_regex_info_by_intent_id(self, agent_id=1, domain_id=56, intent_id=8329):
        datas = self.get_regexs(agent_id, domain_id, intent_id)
        regex_info = []
        if datas.status_code != 200:
            logger.error(f"error with http code {datas.status_code}")
            return regex_info, datas
        try:
            res = datas.json()["examplelist"]
        except Exception as e:
            logger.error(f"json unmarshall failed with error {e}")
            res = []
        if not res:
            return regex_info, datas

        for data in res:
            label_list = []
            for d in data["labellist"]:
                label_list.append(d["text"])
            regex_info.append({"type": data["type"], "text": data["text"], "label_list": label_list})
        return regex_info, datas


class RegexFormat(SystemService):
    """检测步骤
    1.查询系统技能下所有intent的模板 分解成.json和.xlsx json存放槽位 xlsx存放模板及其他信息
    2.查询实体清单 填充槽位值到.json
    3.递归拆分xlsx模板 组合成测试用例 组合时自动替换槽位值
    4.测试用例放到算法接口测试 校验测试结果 写入xlsx
    """

    def format_slots_and_templates(self, domain_name="", inspect_intent_list=None):
        """打印agent=1 现有意图的所有模板 仅用作后续代码参考
        :return: slots_template 所有实体类型和槽位 {"@sys.entity.poetry-content": ""}
        :return: templates 所有模板regex 和与之关联的intent domain等必要信息 [{},{}]
        """
        logger.info("start to find templates from smart voice!")
        templates_xlsx = []
        slots_json = {}
        domain_list, _ = self.get_domains_info(keyword=domain_name)
        if not domain_list:
            return slots_json, templates_xlsx
        for domain in domain_list:
            if domain_name and domain["domain_name"] != domain_name:
                continue
            domain_id = domain["domain_id"]
            domain_name = domain["domain_name"]
            status = domain["status"]
            intent_list, _ = self.get_intent_info_by_domain_id(domain_id=domain_id)
            if not intent_list:
                return slots_json, templates_xlsx

            this_intent_list = []
            if inspect_intent_list:
                for i in inspect_intent_list:
                    for j in intent_list:
                        if i == j["intent_name"]:
                            this_intent_list.append(j)
            else:
                this_intent_list = intent_list

            for intent in this_intent_list:
                intent_id = intent["intent_id"]
                intent_name = intent["intent_name"]
                input_context = intent["input_context"]
                regex_list, _ = self.get_regex_info_by_intent_id(domain_id=domain_id, intent_id=intent_id)
                if not regex_list:
                    continue
                for regex in regex_list:
                    text = regex["text"]
                    regex_type = regex["type"]
                    label_list = regex["label_list"]
                    templates_xlsx.append({
                        "domain_status": status,
                        "domain_name": domain_name,
                        "domain_id": domain_id,
                        "intent_name": intent_name,
                        "intent_id": intent_id,
                        "input_context": input_context,
                        "regex_type": regex_type,
                        "regex_text": text,
                        "regex_labels": json.dumps(label_list, ensure_ascii=False)
                    })
                    for label in label_list:
                        if "@" in label:
                            slots_json[label] = ""

        logger.info("find templates from smart voice finished!")
        return slots_json, templates_xlsx

    def format_slots_value(self, url, slots_json):
        """通过实体查询接口 给所有的槽位填值
        :param url:
        :param slots_json:
        :return:
        """
        logger.info("start to find slots value from entity trie!")
        result = slots_json
        if not isinstance(result, dict):
            logger.error("slots_json is not a dict instance!")
            return False
        for key, value in result.items():
            entity_type = key.split(":")[0].split("@")[-1]
            res = search_entity(url=url, entity_type=entity_type)
            if res:
                result[key] = res[-1]["itemname"]
            else:
                if "@sys.date" in key:
                    result[key] = "今天"

                if "@sys.date-time" in key:
                    result[key] = "今天五点"

                if "@sys.time" in key:
                    result[key] = "五点"

                if "@sys.date-duration" in key:
                    result[key] = "最近"

                if "@sys.percent" in key:
                    result[key] = "1"

                if "@sys.number" in key:
                    result[key] = "1"

                if "@sys.year" in key:
                    result[key] = "2022"

                if "@sys.entity.city" in key:
                    result[key] = "成都"

                if "@sys.entity.orientation" in key:
                    result[key] = "下"

                if "@sys.entity.solarterms" in key:
                    result[key] = "清明"

                if "@sys.entity.season" in key:
                    result[key] = "春"

                if "@sys.entity.holiday" in key:
                    result[key] = "国庆"

                if "@sys.entity.weekday" in key:
                    result[key] = "星期一"

                if "dance_name" in key:
                    result[key] = "茉莉花"

        logger.info("find slots value from entity trie finished!")
        return result

    def format_test_cases(self, slots_json, templates_xlsx):
        logger.info("start to format test cases!")
        test_cases = []
        for item in templates_xlsx:
            template = item["regex_text"]
            if item["regex_type"] == "quote":
                item["query"] = template
                test_cases.append(item)
            else:
                for slot_key in json.loads(item["regex_labels"]):
                    if "@" in slot_key:
                        slot_value = slots_json[slot_key]
                        if slot_value:
                            template = template.replace(slot_key, slot_value)

                this_temp_cases_list = regex_text_handle(template)
                if this_temp_cases_list:
                    this_temp_cases_list = this_temp_cases_list[0]
                for case in this_temp_cases_list:
                    new_item = copy.deepcopy(item)
                    new_item["query"] = case
                    test_cases.append(new_item)
        logger.info(f"format test cases succeed with total {len(test_cases)}!")
        return test_cases


def search_entity(url, entity_type, keywords="", limit="15"):
    """查询实体实例接口
    :param url: http://172.16.23.30:30732
    :param entity_type: sys.entity.poetry-content-feihualing
    :param keywords:
    :param limit:
    :return:
    """
    payload = {
        "keywords": keywords,
        "types": entity_type,
        "limit": limit
    }
    path = "/v1/search_entity"
    res = requests.request(method="POST", url=url + path, json=payload)
    if res.status_code == 200:
        try:
            return res.json()["entities"][entity_type.split(".")[-1]]["entity"]
        except:
            logger.warning(f"search for entity_type={entity_type} failed with status code {res.status_code}!")
            return None
    logger.warning(f"search for entity_type={entity_type} failed with status code {res.status_code}!")
    return None


def nlu_debug_info(url, query, context=""):
    """SDK算法 意图识别接口
    :param url: http://172.16.23.18:30757
    :param query:
    :param context:
    :return:
    """
    payload = {
        "traceid": "123",
        "agentid": "1",
        "query": query,
        "context": context,
        "robot_name": ""
    }
    path = "/nlp-sdk/nlu/intent-recognize"
    response = requests.request(method="POST", url=url + path, json=payload)
    data = response.json()["data"]
    return {
        "query": query,
        "domainname": data["domainname"],
        "intentname": data["intentname"],
        "parameters": data["parameters"]
    }


def save_file(file_name, file_data):
    with open(file_name, "w") as f:
        f.writelines(file_data)
    logger.info(f"store local file succeed! filename={file_name}")


def regex_text_handle(s):
    """对regex_text进行切割 排列组合成用例列表 步骤：
    example：小达[今天|明天|后天|昨天][成都|上海|北京|深圳]天气怎么样

    1.将regex_text按照[]拆分成列表：[小达, 今天|明天|后天|昨天, 成都|上海|北京|深圳, 天气怎么样]
    2.将列表中含有|分隔线的拆分成列表：[小达, [今天, 明天, 后天, 昨天], [成都, 上海, 北京, 深圳], 天气怎么样]
    3.通过递归将用例排列组合：
    :return: 返回用例列表 list
    """

    def permutation(new_list):
        """递归 排列组合用例"""
        if len(new_list) <= 1:
            return new_list
        cc = []
        for aa in new_list[-2]:
            for bb in new_list[-1]:
                cc.append(aa + bb)
        new_list.pop()
        new_list[-1] = cc
        return permutation(new_list)

    if "[" in s:
        temp = [i for i in s.replace("[", "kk").replace("]", "kk").split("kk") if i != ""]
        ss = []
        for i in temp:
            if "$" not in i and "^" not in i and "#" not in i:
                if "|" in i:
                    ss.append(i.split("|"))
                else:
                    ss.append([str(i)])
        return permutation(ss)
    return [[s]]


class SDKTest(RegexFormat):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    def __init__(self, base_url, username, password):
        super().__init__(base_url, username, password)
        self.test_cases = []
        self.test_results = []
        self.domain = ""

    def get_all_data(self, entity_search_url, domain_name="", inspect_intent_list=None):
        self.domain = domain_name
        slots_json, temps_xlsx = self.format_slots_and_templates(domain_name=domain_name,
                                                                 inspect_intent_list=inspect_intent_list)
        new_slots_json = self.format_slots_value(url=entity_search_url, slots_json=slots_json)
        save_file(f"{self.now_time}_new_slots_json_{domain_name}.json", json.dumps(new_slots_json, ensure_ascii=False))
        self.test_cases = self.format_test_cases(new_slots_json, temps_xlsx)

    def test_all_cases_by_sdk_interface(self, sdk_url):
        for case in self.test_cases:
            if "@" not in case["query"]:
                input_context = case["input_context"]
                if "," in input_context:
                    input_context = input_context.split(",")[0]
                result = nlu_debug_info(sdk_url, query=case["query"], context=input_context)
                case["act_domain"] = result["domainname"]
                case["act_intent"] = result["intentname"]
                case["act_param"] = result["parameters"]
                if case["act_intent"] == case["intent_name"]:
                    case["is_pass"] = True
                else:
                    case["is_pass"] = False
                self.test_results.append(case)

    def save_test_results(self):
        excel_filename = f"{self.now_time}_new_test_results_{self.domain}.xlsx"
        Handlers.write_list_map_as_excel(self.test_results, excel_writer=excel_filename, sheet_name="Sheet1",
                                         index=False)
        logger.info(f"store local file succeed! filename={excel_filename}")


if __name__ == '__main__':
    instance = SDKTest(base_url="https://mmue-dit87.harix.iamidata.com", username="liuzhaobing", password="123456")
    instance.get_all_data(entity_search_url="http://172.16.23.30:30732",
                          domain_name="system",
                          inspect_intent_list=['decreaseVolume',
                                               'mute',
                                               'DecreaseSpeechRate',
                                               'getVolume',
                                               'IncreaseSpeechRate',
                                               'increaseVolume',
                                               'NormalSpeechRate',
                                               'unmute',
                                               'StartPushing',
                                               ])
    instance.test_all_cases_by_sdk_interface(sdk_url="http://172.16.23.15:30375")
    instance.save_test_results()
