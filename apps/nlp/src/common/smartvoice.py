#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import time
import jsonpath
import requests
import urllib.parse
import urllib3

from utils.handler import Handlers

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SmartVoice:
    def __init__(self, base_url, login_user, login_passwd, agent_id, agent_name=None):
        self.base_url = base_url  # "http://172.16.23.85:30950"
        self.login_user = login_user  # "admin@cloudminds"
        self.login_passwd = login_passwd  # "Smartvoice1506"
        self.agent_id = agent_id  # "1223"
        self.agent_name = agent_name
        self.sys_entities = None
        self.auth_info = None
        self.headers = {'Connection': 'keep-alive', 'Content-Type': 'application/json',
                        'Accept': 'application/json, text/plain, */*',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
        self.login()
        self.get_sv_agent_by_name(self.agent_name) if not self.agent_id else self.agent_id

    def sv_request(self, method, url, *args, **kwargs):
        return requests.request(method=method, url=self.base_url + url, headers=self.headers,
                                verify=False, timeout=10, *args, **kwargs)

    def get_login_headers(self):
        self.headers = {'Connection': 'keep-alive', 'Content-Type': 'application/json',
                        'Accept': 'application/json, text/plain, */*', 'authinfo': self.auth_info}
        return self.headers

    def login(self):
        url = '/v2/ux/user/login'
        payload = {"username": self.login_user, "password": self.login_passwd}
        res = self.sv_request(method="POST", url=url, json=payload)
        login_result = res.json()

        auth_info = {
            "userid": login_result['userid'],
            "authtoken": "{}".format(login_result['authtoken']),
            "sessionid": login_result['sessionid'],
            "agentid": login_result['agentid'],
            "manualsel": True,
            "userName": self.login_user,
            "role": login_result['role'],
            "isadmin": login_result['isadmin'],
            "masteruserid": login_result['masteruserid'],
            "lang": "zh-CN",
            "parentId": login_result['parentId']
        }
        self.auth_info = json.dumps(auth_info)
        return self.get_login_headers()

    def get_sv_agent_list(self):
        url = '/v2/ux/agents?keyword=&page=1&pagesize=10'
        res = self.sv_request(method="GET", url=url)
        return res

    def get_sv_agent_by_name(self, agent_name):
        dict_response = self.get_sv_agent_list().json()
        total_pages = dict_response['pagination']['pagecount']

        url = '/v2/ux/agents?keyword={}&page=1&pagesize={}'.format(agent_name, total_pages)
        res = self.sv_request(method="GET", url=url)
        agent_info = res.json()['data'][0]
        if agent_info:
            self.agent_id = agent_info['id']
            print('  - 接口提示：存在该 agent name 打印 agent id', self.agent_id)
            agent_token = jsonpath.jsonpath(agent_info,
                                            expr='$..data[?(@.agentname==\'{}\')].accesstoken'.format(agent_name))
            return agent_token[0]
        else:
            print('  - 接口提示：不存在该 agent name')
            return False

    def send_qa(self, question):
        url = "/v2/ux/agents/{}/smartqa/query?question={}&hariVersion=v3".format(self.agent_id,
                                                                                 urllib.parse.quote(question))
        start = time.time()
        res = self.sv_request(method="GET", url=url)
        edg_cost = (time.time() - start) * 1000  # 端测耗时
        logs = json.loads(res.json()['answer'])
        resp_cost = logs['hitlog']['cost']  # 响应耗时
        return logs, edg_cost, resp_cost

    def send_msg(self, question):
        return self.send_qa(question)[0]


class SvSystemModule(SmartVoice):
    def get_agent_system_service_list(self):
        url = '/v2/ux/agents/services?agentid={}&domaintype=0'.format(self.agent_id)
        return self.sv_request(method="GET", url=url)

    def get_agent_system_service_info(self, system_service_name):
        for service in self.get_agent_system_service_list().json():
            if service['name'] == system_service_name:
                print('  - 接口提示：存在系统服务', system_service_name)
                return service
        print('  - 接口提示：不存在系统服务', system_service_name)
        return False

    def get_agent_system_service_info_dict(self, system_service_name):
        service = self.get_agent_system_service_info(system_service_name)
        if service:
            service_dict = {'系统服务名称': service['name'],
                            '系统服务ID': service['id'],
                            '系统服务开启状态': service['enabled'],
                            '关闭后命中状态': service['closedrecg'],
                            '关闭后命中信息': service['closedhit']}
            print('  - 接口返回：', service_dict)
            return service_dict
        else:
            return False

    def get_agent_system_service_id(self, system_service_name):
        service = self.get_agent_system_service_info_dict(system_service_name)
        if service:
            return service['系统服务ID']
        else:
            return False

    def get_agent_system_service_status(self, system_service_name):
        service = self.get_agent_system_service_info_dict(system_service_name)
        if service:
            return service['系统服务开启状态']
        else:
            return False

    def operate_system_service_action(self, system_service_name, action_status):
        service_id = self.get_agent_system_service_id(system_service_name)
        if service_id:
            url1 = '/v2/ux/agents/{}/domains/{}/enable?domainid={}'.format(self.agent_id, service_id, service_id)
            url2 = '/v2/ux/agents/{}/domains/{}/disable'.format(self.agent_id, service_id)
            print('  - 接口提示：系统服务 {} 准备{}'.format(system_service_name, action_status))
            if action_status == '开启':
                self.sv_request(method="GET", url=url1)
            elif action_status == '关闭':
                self.sv_request(method="POST", url=url2)
            else:
                print('  - 代码提示：action_status输入错误 请输入[开启]/[关闭]')
                return False
            time.sleep(3)
            if self.get_agent_system_service_status(system_service_name):
                print('  - 接口提示：系统服务 {} 已开启'.format(system_service_name))
            else:
                print('  - 接口提示：系统服务 {} 已关闭'.format(system_service_name))
            return True
        else:
            return False

    def open_all_services(self, action='开启'):
        for name in [service["name"] for service in self.get_agent_system_service_list().json()]:
            self.operate_system_service_action(name, action)

    def operate_system_service_closedrecg(self, system_service_name, action_status):
        """
        修改指定agent的指定服务为[关闭后不命中]/[关闭后仍然命中]
        """
        service_info = self.get_agent_system_service_info(system_service_name)
        if service_info:
            if action_status == '开启':
                closedrecg_status = 1
                print('  - 接口提示：系统服务 {}  [关闭后命中状态] 准备开启'.format(system_service_name))
            elif action_status == '关闭':
                closedrecg_status = 0
                print('  - 接口提示：系统服务 {}  [关闭后命中状态] 准备关闭'.format(system_service_name))
            else:
                print('  - 代码提示：action 操作值写错')
                return False
            payload = {"domainname": service_info["name"], "domaininfo": service_info["info"],
                       "supportedLanguages": service_info["supportedLanguages"], "type": service_info["type"],
                       "status": service_info["status"], "url": service_info["url"],
                       "callservice": service_info["callservice"], "release": service_info["release"],
                       "operation": service_info["operation"], "thirdparty": service_info["thirdparty"],
                       "keyword": service_info["keyword"], "closedrecg": closedrecg_status,
                       "closedhit": service_info["closedhit"], "domainswitchhit": service_info["domainswitchhit"],
                       "id": service_info["id"]}
            # 修改此服务的配置信息
            url = "/v2/ux/agents/{}/domains".format(self.agent_id)
            self.sv_request(method="PATCH", url=url, json=payload)
            if self.get_agent_system_service_info_dict(system_service_name)['关闭后命中状态']:
                print('  - 接口提示：系统服务 {}  [关闭后命中状态] 已开启'.format(system_service_name))
            else:
                print('  - 接口提示：系统服务 {}  [关闭后命中状态] 已关闭'.format(system_service_name))
            return True
        else:
            return False

    def edit_dm_details(self, dm_name, dm_status):
        check_dm_url = "/v2/ux/agents/{}".format(self.agent_id)
        dm_url_r = self.sv_request(method="GET", url=check_dm_url)
        dm = dm_url_r.json()['dmName']

        dm_list_url = "/v2/ux/dmtemplate/listdetail/" + str(dm)
        dm_details = self.sv_request(method="GET", url=dm_list_url)
        data = dm_details.json()["data"]

        if dm_status == "关闭":
            dm_status = False
        else:
            dm_status = True
        for n in data:
            if dm_name == n['dmRoutineName']:
                n["isOpen"] = dm_status

        edit_dm_url = "/v2/ux/dmtemplate"
        payload = {"templateName": dm, "data": data}
        self.sv_request(method="PUT", url=edit_dm_url, json=payload)
        agent_dm_details = self.sv_request(method="PUT", url=dm_list_url, json=payload).json()['data']
        print("  - 接口提示：DM流程变更后当前状态:", agent_dm_details)
        flg = False
        for routine in agent_dm_details:
            if routine['dmRoutineName'] == dm_name:
                if routine['isOpen'] == dm_status:
                    flg = True
                    break
        return flg


class SmartVoiceEntityMange(SmartVoice):
    """实体管理"""

    def get_entity_list_all(self):
        """查询所有实体列表  返回response"""
        try:
            url1 = "/v2/ux/agents/{}/entities".format(self.agent_id)
            res = self.sv_request(method="GET", url=url1)
            if res.status_code == 200:
                print("查询所有实体列表  成功")
            else:
                print("查询所有实体列表  失败  原因：", res.json()["error"])
            return res
        except Exception as e:
            print("查询所有实体列表  失败  原因：", e)

    def get_entity_list_sys(self):
        """查询所有系统实体列表  返回list"""
        try:
            entities = self.get_entity_list_all().json()
            self.sys_entities = entities["system"]
            print("查询所有系统实体列表  成功")
            return self.sys_entities
        except Exception as e:
            print("查询所有系统实体列表  失败  原因：", e)

    def get_entity_list_cus(self):
        """查询所有用户实体列表  返回list"""
        try:
            entities = self.get_entity_list_all().json()
            sys_entities = entities["custom"]
            print("查询所有用户实体列表  成功")
            return sys_entities
        except Exception as e:
            print("查询所有用户实体列表  失败  原因：", e)

    def get_entity_id_by_name_sys(self, entity_name):
        """根据实体名查询实体id值  返回int类型"""
        try:
            entity_id = -1
            if not self.sys_entities:
                sys_entities_list = self.get_entity_list_sys()
            else:
                sys_entities_list = self.sys_entities
            for entity_info in sys_entities_list:
                if entity_info["entityname"] == entity_name:
                    entity_id = entity_info["id"]
                    print("根据实体名{}查询实体id值{}  成功".format(entity_name, entity_id))
                    return entity_id
            if entity_id == -1:
                print("根据实体名{}查询实体id值  失败  原因：".format(entity_name), "未找到对应的实体")
        except Exception as e:
            print("根据实体名查询实体id值  失败  原因：", e)

    def get_entity_id_by_name_cus(self, entity_name):
        """根据实体名查询实体id值  返回int类型"""
        try:
            entity_id = -1
            sys_entities_list = self.get_entity_list_cus()
            for entity_info in sys_entities_list:
                if entity_info["entityname"] == entity_name:
                    entity_id = entity_info["id"]
                    print("根据实体名{}查询实体id值{}  成功".format(entity_name, entity_id))
                    return entity_id
            if entity_id == -1:
                print("根据实体名{}查询实体id值  失败  原因：".format(entity_name), "未找到对应的实体")
        except Exception as e:
            print("根据实体名查询实体id值  失败  原因：", e)


class SmartVoiceSettingsMange(SmartVoice):
    """应用参数管理"""

    def get_additional_settings(self):
        """应用参数 查询"""
        url1 = "/v2/ux/agents/{}/agentsetting?page=1&pagesize=100&keyword=".format(self.agent_id)
        res = self.sv_request(method="GET", url=url1)
        return res

    def add_additional_setting(self, key, value):
        """应用参数 新增"""
        url1 = "/v2/ux/agents/{}/agentsetting".format(self.agent_id)
        payload = {"data": [{"key": key, "value": value, "comment": ""}]}
        res = self.sv_request(method="POST", url=url1, json=payload)
        return res

    def del_additional_setting(self, key):
        """应用参数 删除"""
        settings = self.get_additional_settings().json()["data"]
        for s in settings:
            if key == s["key"]:
                url1 = "/v2/ux/agents/{}/agentsetting/{}".format(self.agent_id, s["id"])
                res = self.sv_request(method="DELETE", url=url1)
                return res


class SmartVoiceCustomDomainMange(SmartVoice):
    """用户自定义服务管理"""

    def get_custom_domain_list(self):
        """查询所有服务列表  返回response"""
        try:
            url1 = "/v2/ux/agents/{}/domains?page=1&pagesize=100&keyword=&type=intent".format(self.agent_id)
            res = self.sv_request(method="GET", url=url1)
            if res.status_code == 200:
                print("查询所有服务列表  成功")
            else:
                print("查询所有服务列表  失败  原因：", res.json()["error"])
            return res
        except Exception as e:
            print("查询所有服务列表  失败  原因：", e)

    def get_custom_domain_id_by_name(self, domain_name):
        """根据服务名查询服务id值  返回int类型"""
        try:
            domain_id = -1
            domain_list = self.get_custom_domain_list().json()
            for domain_info in domain_list["data"]:
                if domain_info["domainname"] == domain_name:
                    domain_id = domain_info["id"]
                    print("根据服务名{}查询服务id值{}  成功".format(domain_name, domain_id))
                    return domain_id
            if domain_id == -1:
                print("根据服务名{}查询服务id值{}  失败  原因：".format(domain_name, domain_id), "未找到对应的服务")
        except Exception as e:
            print("根据服务名查询服务id值  失败  原因：", e)

    def del_custom_domain(self, domain_name):
        """删除自定义服务"""
        domain_id = self.get_custom_domain_id_by_name(domain_name)
        try:
            url1 = "/v2/ux/agents/{}/domains/{}".format(self.agent_id, domain_id)
            res = self.sv_request(method="DELETE", url=url1)
            if res.status_code == 200:
                print("删除自定义服务{}  成功".format(domain_name))
            else:
                print("删除自定义服务{}  失败  原因：".format(domain_name), res.json()["error"])
            return res
        except Exception as e:
            print("删除自定义服务{}  失败  原因：".format(domain_name), e)

    def create_custom_domain(self, domain_name):
        """创建自定义服务"""
        try:
            url1 = "/v2/ux/agents/{}/domains".format(self.agent_id)
            payload = {"domainname": domain_name,
                       "domaininfo": "",
                       "supportedLanguages": ["zh-CN", "en-US"],
                       "status": "",
                       "type": "",
                       "url": "",
                       "callservice": "",
                       "release": 1,
                       "operation": 0,
                       "thirdparty": 0,
                       "keyword": 0,
                       "closedrecg": 0,
                       "closedhit": "",
                       "domainswitchhit": ""}
            res = self.sv_request(method="POST", url=url1, json=payload)
            if res.status_code == 200:
                print("创建自定义服务{}  成功".format(domain_name))
            else:
                print("创建自定义服务{}  失败  原因：".format(domain_name), res.json()["error"])
            return res
        except Exception as e:
            print("创建自定义服务{}  失败  原因：".format(domain_name), e)


class SmartVoiceHWMange(SmartVoice):
    """热词管理"""

    def get_hw_list(self):
        """获取热词列表"""
        url1 = "/v2/ux/agents/{agent_id}/hotwords?category=0".format(agent_id=self.agent_id)
        res = self.sv_request(method="GET", url=url1)
        return res

    def del_hw(self, hw_id):
        """删除单个热词"""
        url1 = "/v2/ux/agents/{agent_id}/hotwords/{hw_id}".format(agent_id=self.agent_id, hw_id=hw_id)
        res = self.sv_request(method="DELETE", url=url1)
        return res

    def del_hws(self, hws):
        """批量删除热词 hws='8706,8704'  """
        url1 = "/v2/ux/agents/{agent_id}/hotwords/delete".format(agent_id=self.agent_id)
        payload = {"ids": hws}
        res = self.sv_request(method="POST", url=url1, json=payload)
        return res

    def add_hw(self, hw):
        """新增单个热词"""
        url1 = "/v2/ux/agents/{agent_id}/hotwords".format(agent_id=self.agent_id)
        payload = {"hotword": hw,
                   "category": "0",
                   "agentid": str(self.agent_id)}
        res = self.sv_request(method="POST", url=url1, json=payload)
        return res

    def activate_hw(self):
        """激活热词"""
        url1 = "/v2/ux/agents/{agent_id}/submithotwords".format(agent_id=self.agent_id)
        payload = {"username": self.login_user, "category": "0"}
        res = self.sv_request(method="POST", url=url1, json=payload)
        return res

    def auto_activate_hw(self):
        flag = True
        while flag:
            res = self.get_hw_list().json()
            for hw in res["data"]["data"]:
                if hw["canSubmit"]:
                    self.activate_hw()
                    flag = False

    def get_id_by_hw(self, hw):
        res = self.get_hw_list().json()
        for hw_info in res["data"]["data"]:
            if hw_info["hotword"] == hw:
                return hw_info["id"]
        return 0

    def del_hw_by_name(self, hw):
        return self.del_hw(self.get_id_by_hw(hw))

    def get_ids_by_hws(self, hws):
        """获取热词id"""
        ids = []
        res = self.get_hw_list().json()
        for hw in res["data"]["data"]:
            if hw["hotword"] in hws:
                ids.append(str(hw["id"]))
        return ids

    def del_hw_by_names(self, hws):
        ids = self.get_ids_by_hws(hws)
        return self.del_hws(",".join(ids))


class SmartVoiceCustomIntentMange(SmartVoiceEntityMange, SmartVoiceCustomDomainMange):
    """用户自定义意图管理"""

    def get_custom_intents_list(self, domain_name):
        """查询所有意图列表  返回response"""
        try:
            domain_id = self.get_custom_domain_id_by_name(domain_name)
            url1 = "/v2/ux/agents/{}/domains/{}/intents?page=1&pagesize=100&keyword=".format(self.agent_id, domain_id)
            res = self.sv_request(method="GET", url=url1)
            if res.status_code == 200:
                print("根据服务名{}查询所有意图列表  成功".format(domain_name))
            else:
                print("根据服务名{}查询所有意图列表  失败  原因：".format(domain_name), res.json()["error"])
            return res
        except Exception as e:
            print("根据服务名{}查询所有意图列表  失败  原因：".format(domain_name), e)

    def get_custom_intent_id_by_name(self, domain_name, intent_name):
        """根据意图名查询意图id  返回int"""
        try:
            intent_id = -1
            intents_list = self.get_custom_intents_list(domain_name).json()
            for intent in intents_list["data"]:
                if intent["intentname"] == intent_name:
                    intent_id = intent["id"]
                    print("根据意图名{}查询意图id{}  成功".format(intent_name, intent_id))
                    return intent_id
            if intent_id == -1:
                print("根据意图名{}查询意图id  失败  原因：", "未找到对应的意图")
        except Exception as e:
            print("根据意图名{}查询意图id  失败  原因：", e)

    def del_custom_intent(self, domain_name, intent_name):
        """删除指定服务下的意图"""
        domain_id = self.get_custom_domain_id_by_name(domain_name)
        intent_id = self.get_custom_intent_id_by_name(domain_name, intent_name)
        try:
            url1 = "/v2/ux/agents/{}/domains/{}/intents/{}".format(self.agent_id, domain_id, intent_id)
            res = self.sv_request(method="DELETE", url=url1)
            if res.status_code == 200:
                print("删除指定服务{}下的意图{}  成功".format(domain_name, intent_name))
            else:
                print("删除指定服务{}下的意图{}  失败  原因：".format(domain_name, intent_name), res.json()["error"])
            return res
        except Exception as e:
            print("删除指定服务下的意图  失败  原因：", e)

    def compose_string_for_text(self, string):
        """创建意图的payload 先对正则语句进行切割"""
        # TODO 此时      string = "唱一首@sys.entity.singer:Singer的@sys.entity.song:Name"
        string_list = string.split("@")  # 先用@切割成列表
        # TODO 此时 string_list = ['唱一首', 'sys.entity.singer:Singer的', 'sys.entity.song:Name']
        for one in string_list:
            # 遍历列表，如果列表元素中包含中文英文和标点符号，则进一步处理
            if Handlers.is_contain_chinese(one) and Handlers.is_contain_english(one) and Handlers.is_contain_character(
                    one):
                index = string_list.index(one)  # 获取到此元素的索引

                # 将该元素的中文与其他内容分开
                en, ch = "", ""
                for o in one:
                    if Handlers.is_contain_english(o) or Handlers.is_contain_character(o):
                        en += o
                    else:
                        ch += o

                # 根据该元素的第一个字符来确定插入顺序
                if Handlers.is_contain_chinese(one[0]):
                    string_list.insert(index, ch)
                    string_list.insert(index + 1, en)
                else:
                    string_list.insert(index, en)
                    string_list.insert(index + 1, ch)

                string_list.remove(one)
            else:
                pass
        # TODO 此时 string_list = ['唱一首', 'sys.entity.singer:Singer', '的', 'sys.entity.song:Name']
        return string_list

    def return_example_list(self, input_text):
        """拆解正则
        例如输入：唱一首@sys.entity.singer:Singer的@sys.entity.song:Name
        则输出其对应的：examplelist和paramlist
        """
        # meta = input_text.split("@")  # 这样切割好像有点问题
        meta = self.compose_string_for_text(input_text)  # 这样切割好像没有问题
        print(meta)
        labellist = []
        paramlist = []
        for core in meta:
            if "." not in core:
                labellist.append({"text": core})
            else:
                if ":" in core:
                    paramname = core.split(":")[1]
                    entityname = core.split(":")[0]
                    entityid = self.get_entity_id_by_name_sys(entityname)
                    labellist.append({"paramname": paramname,
                                      "entityname": entityname,
                                      "entityid": entityid,
                                      "text": "@" + core})

                    paramlist.append({"paramname": paramname,
                                      "anynum": "",
                                      "entityname": entityname,
                                      "entityid": str(entityid),
                                      "required": False,
                                      "extendable": False,
                                      "prompt": "",
                                      "isexistincorpus": True})

        examplelist = [{"type": "complex",
                        "text": input_text,
                        "labellist": labellist,
                        "textIsEmpty": False}]
        return examplelist, paramlist

    def compose_create_custom_intent_payload(self, intent_name, intent_texts,
                                             inputcontext="", outputcontext="", *args, **kwargs):
        """为创建意图  组装payload"""
        examplelist = []
        paramlist = []
        for intent_text in intent_texts:
            examplelist_1, paramlist_1 = self.return_example_list(intent_text)
            examplelist += examplelist_1
            paramlist += paramlist_1
        paramlist = Handlers.list_duplicate_removal(paramlist)
        examplelist = Handlers.list_duplicate_removal(examplelist)

        payload = {"intentname": intent_name,
                   "inputcontext": inputcontext,
                   "outputcontext": outputcontext,
                   "frontlist": [],
                   "afterlist": [],
                   "voicepad": "",
                   "prompt": "",
                   "luaenabled": False,
                   "reply": False,
                   "examplelist": examplelist,
                   "paramlist": paramlist
                   }
        return payload

    def create_custom_intent(self, domain_name, intent_payload):
        """
        在指定服务domain上 创建意图intent
        :param domain_name:
        :param intent_payload:
            payload = {"id": 0,
                       "agentid": self.agent_id,
                       "domainid": domain_id,
                       "intentname": intent_name,
                       "inputcontext": "",
                       "outputcontext": "",
                       "frontlist": [],
                       "afterlist": [],
                       "voicepad": "",
                       "prompt": "",
                       "luaenabled": False,
                       "reply": False,
                       "examplelist": [{"type": "complex",
                                        "text": "放一首@sys.entity.song:Name",
                                        "labellist": [{"text": "放一首"},
                                                      {"paramname": "Name",
                                                       "entityname": "sys.entity.song",
                                                       "entityid": 163,
                                                       "text": "@sys.entity.song:Name"}],
                                        "textIsEmpty": False}],
                       "paramlist": [
                           {"paramname": "Name", "anynum": "", "entityname": "sys.entity.song", "entityid": "163",
                            "required": False, "extendable": False, "prompt": "", "isexistincorpus": True}]
                       }
        :return:
        """
        domain_id = self.get_custom_domain_id_by_name(domain_name)
        try:
            url1 = "/v2/ux/agents/{}/domains/{}/intents".format(self.agent_id, domain_id)
            intent_payload["domainid"] = domain_id
            intent_payload["agentid"] = self.agent_id

            res = self.sv_request(method="POST", url=url1, json=intent_payload)
            if res.status_code == 200:
                print("在指定服务{}上  创建意图{}  成功".format(domain_name, intent_payload["intentname"]))
            else:
                print("在指定服务{}上  创建意图{}  失败  原因：".format(domain_name, intent_payload["intentname"]),
                      res.json()["error"])
            return res
        except Exception as e:
            print("在指定服务{}上  创建意图  失败  原因：".format(domain_name), e)


class UnitTest(SmartVoiceHWMange):
    def main(self):
        # res = self.add_hw("什么事儿鸭")
        res = self.get_hw_list()
        # res = self.del_hw_by_name("什么事儿鸭")
        try:
            print(res.json())
        except Exception as e:
            print(res, e)
        finally:
            print(type(res))
        return res


if __name__ == '__main__':
    t = UnitTest("http://172.16.23.85:30950", "admin@cloudminds", "Smartvoice1506", "1496").main()
