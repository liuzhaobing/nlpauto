#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import os
from concurrent.futures import ThreadPoolExecutor
from apps.nlp.src.common.intent_recognize import IntentRecognize
from conf.env import TEST_SDK_ENTITY_PATH_RELATIVE, BASE_DIR
from utils.handler import Handlers


class EntityTest:

    def __init__(self):
        self.test_results = []

    @staticmethod
    def excel_case_run(url, test_case):
        """运行单条用例并返回结果"""
        res, cost = IntentRecognize.run(url, "", test_case["query"], "1", "", "")

        # 提取entity
        dic = {}
        if res["data"]["parameters"]:
            for p in res["data"]["parameters"]:
                dic[p["name"]] = p["beforevalue"]

        test_case["act_domain"] = res["data"]["domainname"]
        test_case["act_intent"] = res["data"]["intentname"]
        test_case["act_entity"] = json.dumps(dic, ensure_ascii=False)  # 字符串格式
        test_case["edg_cost"] = cost
        return test_case

    @staticmethod
    def excel_case_assertion(test_case):
        """单条用例执行后断言"""
        if test_case["domain"] == test_case["act_domain"] and \
                test_case["intent"] == test_case["act_intent"]:
            test_case["intentIsPass"] = True
        else:
            test_case["intentIsPass"] = False

        exp_entity_dict = json.loads(test_case["entity"])
        act_entity_dict = json.loads(test_case["act_entity"])
        if exp_entity_dict == act_entity_dict:
            test_case["entityIsPass"] = True
        else:
            test_case["entityIsPass"] = False

        if test_case["intentIsPass"] and test_case["entityIsPass"]:
            test_case["CaseIsPass"] = True
        else:
            test_case["CaseIsPass"] = False
        return test_case

    @staticmethod
    def excel_case_report(test_results, output_file, sheet_name):
        """整体测试用例输出测试结果"""
        Handlers.write_list_map_as_excel(test_results, excel_writer=output_file, sheet_name=sheet_name, index=False)

        # 测试结果汇总
        report = {"intentIsPass": 0, "entityIsPass": 0, "CaseIsPass": 0}
        for result in test_results:
            if result["intentIsPass"]:
                report["intentIsPass"] += 1
            if result["entityIsPass"]:
                report["entityIsPass"] += 1
            if result["CaseIsPass"]:
                report["CaseIsPass"] += 1
        total_case = len(test_results)
        fmt = "用例总数：{}，意图通过率：{}，实体通过率：{}，用例通过率：{}".format(total_case,
                                                          report["intentIsPass"] / total_case,
                                                          report["entityIsPass"] / total_case,
                                                          report["CaseIsPass"] / total_case)
        with open(output_file + ".txt", "w", encoding="UTF-8") as f:
            f.writelines(fmt)
        return fmt

    def excel_one_case_runner(self, url, test_case, test_results):
        """单条用例执行并断言 记录结果到全局变量"""
        test_results.append(self.excel_case_assertion(self.excel_case_run(url, test_case)))
        return test_results

    def excel_batch_case_runner(self, url, input_file, output_file, sheet_name, case_chan_num):
        """单个excel文件 多条用例执行 并输出测试报告"""
        threadpool = ThreadPoolExecutor(case_chan_num)
        test_cases = Handlers.read_excel_as_list_map(io=input_file, sheet_name=sheet_name)
        for test_case in test_cases:
            threadpool.submit(self.excel_one_case_runner, url, test_case, self.test_results)
        threadpool.shutdown(True)

        self.excel_case_report(self.test_results, output_file, sheet_name)
        return self.test_results


# TODO 待测试
def excel_batch_file_runner(url, file_names, sheet_name, file_chan_num, case_chan_num):
    """多个excel文件 多条用例执行 并输出测试报告"""
    files_info = []
    for file_name in file_names:
        name = Handlers.return_file_name(file_name).split(".")[0] + Handlers.time_strf_now()
        # files_info.append({"input_file": file_name, "one_file_results": [],
        #                    "output_file": os.path.join(TEST_SDK_ENTITY_PATH_RELATIVE, name + ".xlsx")})
        files_info.append({"input_file": file_name, "one_file_results": [],
                           "output_file": os.path.join(BASE_DIR, TEST_SDK_ENTITY_PATH_RELATIVE, name + ".xlsx")})

    threadpool = ThreadPoolExecutor(file_chan_num)
    for info in files_info:
        print(info)
        threadpool.submit(EntityTest().excel_batch_case_runner, url, info["input_file"], info["output_file"],
                          sheet_name, case_chan_num)

    threadpool.shutdown(True)
    return files_info


if __name__ == '__main__':
    sdk_url = "http://172.16.23.15:30068/nlp-sdk/nlu/intent-recognize"  # FIT
    inf1 = os.path.join(BASE_DIR, "media", "upload", "实体测试通用case1.xlsx")
    inf2 = os.path.join(BASE_DIR, "media", "upload", "实体测试通用case2.xlsx")
    inf3 = os.path.join(BASE_DIR, "media", "upload", "实体测试通用case3.xlsx")
    inf4 = os.path.join(BASE_DIR, "media", "upload", "实体测试通用case4.xlsx")
    inf5 = os.path.join(BASE_DIR, "media", "upload", "实体测试通用case5.xlsx")

    inf6 = os.path.join(BASE_DIR, "media", "upload", "实体测试通用case6.xlsx")
    files = [inf1, inf2, inf3, inf4, inf5]
    file = [inf6]
    s = excel_batch_file_runner(url=sdk_url, file_names=file, sheet_name="Sheet1", file_chan_num=1, case_chan_num=10)
    print(s)
