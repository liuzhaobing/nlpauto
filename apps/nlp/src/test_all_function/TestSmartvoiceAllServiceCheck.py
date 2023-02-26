#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import os
from apps.nlp.src.common.smartvoice import SmartVoiceCustomIntentMange, SvSystemModule
from utils.handler import Handlers


class TestSmartVoice(SmartVoiceCustomIntentMange, SvSystemModule):
    skill_all_result = []

    # 测试报告写入excel
    @classmethod
    def report_export_to_excel(cls):
        file_name = Handlers.time_strf_now() + ".xlsx"
        Handlers.write_list_map_as_excel(cls.skill_all_result, excel_writer=file_name,
                                         sheet_name="Sheet1", index=False)
        return file_name

    # 按照版本汇报结果
    @classmethod
    def skill_report_by_version(cls):
        skill_results = cls.skill_all_result
        case_versions = {"max1": 0, "max2": 0}
        for skill_result in skill_results:
            if skill_result["case_version"] >= case_versions["max1"]:
                case_versions["max1"] = skill_result["case_version"]
        for skill_result in skill_results:
            if case_versions["max2"] <= skill_result["case_version"] < case_versions["max1"]:
                case_versions["max2"] = skill_result["case_version"]

        fmt_new = "用例版本：%.2f," % case_versions["max1"]
        fmt_new += cls.skill_result_reporter(skill_results)

        if case_versions["max2"]:
            fmt_old = "用例版本：%.2f," % case_versions["max2"]
            old_skill_results = skill_results
            for old_skill_result in old_skill_results:
                if old_skill_result["case_version"] > case_versions["max2"]:
                    old_skill_results.remove(old_skill_result)
            fmt_old += cls.skill_result_reporter(old_skill_results)
            return fmt_new + "\n" + fmt_old
        else:
            return fmt_new

    # 统计数据
    @classmethod
    def skill_result_reporter(cls, skill_results):
        skill_all_report = {
            "is_intent_pass": 0,
            "is_intent_fail": 0,
            "is_paraminfo_pass": 0,
            "is_paraminfo_fail": 0,
            "is_case_pass": 0,
            "is_case_fail": 0,
            "algo": 0,
            "regex": 0,
            "time_max": 0,
            "time_min": 1000000,
            "time_total": 0
        }
        for skill_result in skill_results:
            # 最大耗时
            if skill_result["edg_cost"] > skill_all_report["time_max"]:
                skill_all_report["time_max"] = skill_result["edg_cost"]
            # 最小耗时
            if skill_result["edg_cost"] < skill_all_report["time_min"]:
                skill_all_report["time_min"] = skill_result["edg_cost"]
            # 总计耗时
            skill_all_report["time_total"] += skill_result["edg_cost"]
            # intent count
            if skill_result["is_intent_pass"]:
                skill_all_report["is_intent_pass"] += 1
            else:
                skill_all_report["is_intent_fail"] += 1
            # paraminfo count
            if skill_result["is_paraminfo_pass"]:
                skill_all_report["is_paraminfo_pass"] += 1
            else:
                skill_all_report["is_paraminfo_fail"] += 1
            # case pass count
            if skill_result["is_case_pass"]:
                skill_all_report["is_case_pass"] += 1
            else:
                skill_all_report["is_case_fail"] += 1
            # algo count
            if skill_result["algo"] == "regex":
                skill_all_report["regex"] += 1
            else:
                skill_all_report["algo"] += 1
        fmt = "用例总数:%d,正确数:%d,错误数:%d,意图正确率:%.4f,槽位正确率:%.4f," \
              "意图支撑中算法占比%.4f,工程模板占比%.4f,最大耗时:%.4fms,平均耗时:%.4fms,最小耗时:%.4fms" % (
                  len(skill_results),
                  skill_all_report["is_case_pass"],
                  skill_all_report["is_case_fail"],
                  skill_all_report["is_intent_pass"] / len(skill_results),
                  skill_all_report["is_paraminfo_pass"] / len(skill_results),
                  skill_all_report["algo"] / len(skill_results),
                  skill_all_report["regex"] / len(skill_results),
                  skill_all_report["time_max"],
                  skill_all_report["time_total"] / len(skill_results),
                  skill_all_report["time_min"]
              )
        return fmt

    # 收集单条用例执行结果
    def skill_result_collect_one(self, case_info, ret, c_pass=None):
        qa_answer = ret[0]
        edg_cost = ret[1]
        service_info = self.get_agent_system_service_info_dict(case_info['domain'])
        service_status = service_info['系统服务开启状态']
        closedrecg_status = service_info['关闭后命中状态']
        if service_status and closedrecg_status:
            is_intent_pass = self.check_source_domain_intent_pass(case_info, qa_answer)
        elif closedrecg_status:
            is_intent_pass = self.check_source_domain_intent_pass(case_info, qa_answer)
        else:
            is_intent_pass = self.check_source_domain_intent_fail(case_info, qa_answer)

        one_result = {
            'id': case_info['id'],
            'question': case_info['question'],
            'exp_source': case_info['source'],
            'act_source': self.get_result_source(qa_answer),
            'exp_domain': case_info['domain'],
            'act_domain': self.get_result_domain(qa_answer),
            'exp_intent': case_info['intent'],
            'act_intent': self.get_result_intent(qa_answer),
            'service_status': service_status,
            'closedrecg_status': closedrecg_status,
            'is_intent_pass': is_intent_pass,
            'edg_cost': edg_cost,
            'exp_paraminfo': case_info['paraminfo'],
            'act_paraminfo': str(self.get_result_param_info(qa_answer)),
            # 'is_paraminfo_pass': self.check_paraminfo_pass(case_info, qa_answer),
            'resp_text': self.get_result_text(qa_answer),
            'resp_url': self.get_result_url(qa_answer),
            'algo': self.get_result_algo(qa_answer),
            'algo_score': self.get_result_algo_score(qa_answer),
            'case_version': case_info['case_version'],
            'traceId': self.get_result_trace_id(qa_answer),
            # 'is_case_pass': self.check_source_domain_intent_pass(case_info, qa_answer) if c_pass is None else c_pass
        }
        return self.skill_all_result.append(one_result)

    def check_source_domain_intent_pass(self, case_info, qa_answer):
        flag = [self.check_source_pass(case_info, qa_answer),
                self.check_domain_pass(case_info, qa_answer),
                self.check_intent_pass(case_info, qa_answer)]
        return False if False in flag else True

    def check_source_domain_intent_fail(self, case_info, qa_answer):
        flag = [
            self.check_source_fail(case_info, qa_answer),
            # self.check_domain_fail(case_info, qa_answer),
            # self.check_intent_fail(case_info, qa_answer)
        ]
        return False if False in flag else True

    def check_source_pass(self, case_info, qa_answer):
        if case_info["source"] == self.get_result_source(qa_answer):
            return True
        else:
            print("  - 测试提示：预期source[{}]与实际source[{}]不一致 测试Fail".format(case_info["source"],
                                                                        self.get_result_source(qa_answer)))
            return False

    def check_domain_pass(self, case_info, qa_answer):
        if case_info["domain"] == self.get_result_domain(qa_answer):
            return True
        else:
            print("  - 测试提示：预期domain[{}]与实际domain[{}]不一致 测试Fail".format(case_info["domain"],
                                                                        self.get_result_domain(qa_answer)))
            return False

    def check_intent_pass(self, case_info, qa_answer):
        if case_info["intent"] == self.get_result_intent(qa_answer):
            return True
        else:
            print("  - 测试提示：预期intent[{}]与实际intent[{}]不一致 测试Fail".format(case_info["intent"],
                                                                        self.get_result_intent(qa_answer)))
            return False

    def check_paraminfo_pass(self, case_info, qa_answer):
        flag = []
        exp_param = case_info["paraminfo"]
        act_param = self.get_result_param_info(qa_answer)
        if "{" in str(act_param) and "{" in str(exp_param):
            exp_param = json.loads(exp_param)
            # 判断所有实际结果是否符合预期
            for act in act_param:
                # 不开上下文的断言
                if act['BeforeValue'] in case_info['question']:
                    exp_param_str = str(exp_param)
                    if act['BeforeValue'] in exp_param_str \
                            and act['EntityType'] in exp_param_str \
                            and act['Name'] in exp_param_str and \
                            act['Value'] is not None:
                        flag.append(True)
                    else:
                        flag.append(False)  # 实际槽位不符合期望槽位
                # 开上下文的断言
                else:
                    pass

            # 判断所有预期结果是否都命中
            for exp in exp_param:
                act_param_str = str(act_param)
                if exp['BeforeValue'] in act_param_str \
                        and exp['EntityType'] in act_param_str \
                        and exp['Name'] in act_param_str:
                    flag.append(True)
                else:
                    flag.append(False)
        elif "{" not in str(act_param) and "{" not in str(exp_param):
            flag.append(True)
        else:
            flag.append(False)

        return False if False in flag else True

    def check_source_fail(self, case_info, qa_answer):
        if case_info["source"] != self.get_result_source(qa_answer):
            return True
        else:
            print("  - 测试提示：预期source[{}] 实际source[{}] 测试Fail".format(case_info["source"],
                                                                     self.get_result_source(qa_answer)))
            return False

    def check_domain_fail(self, case_info, qa_answer):
        if case_info["domain"] != self.get_result_domain(qa_answer):
            return True
        else:
            print("  - 测试提示：预期domain[{}] 实际domain[{}] 测试Fail".format(case_info["domain"],
                                                                     self.get_result_domain(qa_answer)))
            return False

    def check_intent_fail(self, case_info, qa_answer):
        if case_info["intent"] != self.get_result_intent(qa_answer):
            return True
        else:
            print("  - 测试提示：预期intent[{}] 实际intent[{}] 测试Fail".format(case_info["intent"],
                                                                     self.get_result_intent(qa_answer)))
            return False

    # 从返回值获取指定信息
    @staticmethod
    def get_result_source(qa_answer):
        try:
            return qa_answer['source']
        except:
            return ""

    # 从返回值获取指定信息
    @staticmethod
    def get_result_domain(qa_answer):
        try:
            return qa_answer['hitlog']['domain']
        except:
            return ""

    # 从返回值获取指定信息
    @staticmethod
    def get_result_intent(qa_answer):
        try:
            return qa_answer['hitlog']['intent']
        except:
            return ""

    # 从返回值获取指定信息
    @staticmethod
    def get_result_text(qa_answer):
        try:
            return qa_answer['tts'][0]['text']
        except:
            return ""

    # 从返回值获取指定信息
    @staticmethod
    def get_result_url(qa_answer):
        try:
            return qa_answer['tts'][0]['action']['url']
        except:
            return ""

    # 从返回值获取指定信息
    @staticmethod
    def get_result_pic_url(qa_answer):
        try:
            return qa_answer['tts'][0]['action']['pic_url']
        except:
            return ""

    # 从返回值获取指定信息
    @staticmethod
    def get_result_videl_url(qa_answer):
        try:
            return qa_answer['tts'][0]['action']['videl_url']
        except:
            return ""

    # 从返回值获取指定信息
    @staticmethod
    def get_result_param_info(qa_answer):
        if qa_answer['hitlog']['paraminfo']:
            return qa_answer['hitlog']['paraminfo']
        else:
            return ""

    # 从返回值获取指定信息
    @staticmethod
    def get_result_algo(qa_answer):
        try:
            return qa_answer['hitlog']['algo']
        except:
            return ""

    # 从返回值获取指定信息
    @staticmethod
    def get_result_algo_score(qa_answer):
        try:
            return qa_answer['hitlog']['qaresult']['answer']['score']
        except:
            return ""

    # 从返回值获取指定信息
    @staticmethod
    def get_result_trace_id(qa_answer):
        try:
            return qa_answer['hitlog']['traceId']
        except:
            return ""

    # 从返回值获取指定信息
    @staticmethod
    def get_result_template(qa_answer):
        try:
            return qa_answer['hitlog']['machedtemlate']
        except:
            return ""

    # 从返回值获取指定信息
    @staticmethod
    def get_result_third_call(qa_answer):
        if qa_answer['thirdCost']:
            return True
        else:
            return False

    # 从返回值获取指定信息
    @staticmethod
    def get_result_simquestions(qa_answer):
        try:
            return qa_answer['simqs']
        except:
            return ""


class TestSmartVoiceAllServiceCheck(TestSmartVoice):
    case_file = os.path.join("data", "skill_all_function_test.xlsx")
    case_file_sheet = "Sheet1"

    def test_engine(self, case_info, domain_switch="开启", closedrecg_switch="开启"):
        action_result = self.operate_system_service_action(case_info["domain"], domain_switch)
        if action_result:
            action_result = self.operate_system_service_closedrecg(case_info["domain"], closedrecg_switch)
            if action_result:
                ret = self.send_qa(case_info["question"])
                case_pass = self.check_domain_pass(case_info, ret[0])
                return self.skill_result_collect_one(case_info, ret, case_pass)

    def all_function_check(self, case_info):
        print("执行步骤：开启服务 服务匹配 预期匹配成功")
        self.test_engine(case_info, "开启", "开启")

        print("执行步骤：关闭服务 将[关闭后命中状态] 开启 服务匹配 预期匹配成功")
        self.test_engine(case_info, "关闭", "开启")

        print("执行步骤：关闭服务 将[关闭后命中状态] 关闭 服务匹配 预期匹配失败")
        self.test_engine(case_info, "关闭", "关闭")

    def get_test_cases(self):
        self.test_cases = Handlers.read_excel_as_list_map(io=self.case_file, sheet_name=self.case_file_sheet)
        return self.test_cases

    def run(self):
        for case in self.get_test_cases():
            self.all_function_check(case)
        return self.report_export_to_excel()


if __name__ == '__main__':
    test = TestSmartVoiceAllServiceCheck("http://172.16.23.85:30950", "admin@cloudminds", "Smartvoice1506", "1223")
    test.run()
