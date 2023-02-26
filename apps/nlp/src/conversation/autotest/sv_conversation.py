#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
from apps.nlp.src.common.smartvoice import SmartVoiceCustomIntentMange, SmartVoiceSettingsMange
from utils.handler import Handlers


class ConversationMangeTest(SmartVoiceCustomIntentMange, SmartVoiceSettingsMange):
    """
    先从excel中读取case
    再从case中读取ng配置 使ng配置生效
    然后运行case本身并断言
    最后清理ng配置
    """

    def add_user_service(self, domain):
        """新增配置"""
        # 先在sv上配置debug 参数
        self.add_additional_setting(key="dmkit_switch", value="on")
        self.add_additional_setting(key="dmkit_debuginfo_switch", value="on")

        # 读取配置文件中 domain所需要的 意图模板
        model_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data", domain["smartvoice_json"])
        one_domain_sv_models = Handlers.load_json(model_json_path)

        # sv 用户技能 的模板配置信息 一键初始化
        for conf in one_domain_sv_models:
            self.case_domain_name = conf["domain"]
            self.del_custom_domain(self.case_domain_name)
            self.create_custom_domain(self.case_domain_name)
            for intent in conf["intents"]:
                self.case_intent_name = intent["intent_name"]
                self.case_intent_text = intent["intent_text"]
                self.inputcontext = intent["inputcontext"]
                self.outputcontext = intent["outputcontext"]
                self.intent_payload = self.compose_create_custom_intent_payload(self.case_intent_name,
                                                                                self.case_intent_text,
                                                                                self.inputcontext,
                                                                                self.outputcontext)
                self.create_custom_intent(self.case_domain_name, self.intent_payload)

    def del_user_service(self, domain):
        """删除配置"""
        self.del_additional_setting(key="dmkit_switch")
        model_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data", domain["smartvoice_json"])
        one_domain_sv_models = Handlers.load_json(model_json_path)

        for conf in one_domain_sv_models:
            self.del_custom_domain(conf["domain"])


if __name__ == '__main__':
    tester = ConversationMangeTest("http://172.16.23.85:30950", "admin@cloudminds", "Smartvoice1506", "1516")
    setup_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data", "setup.json")
    domains = Handlers.load_json(setup_json_path)

    for d in domains:
        if d["domain"] == "crosstalk":
            tester.add_user_service(d)
            # tester.del_user_service(d)
