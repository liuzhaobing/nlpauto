# -*- coding:utf-8 -*-
import datetime
import json
import random
import uuid

import requests

from utils.handler import Handlers
from utils.utils_mysql import DataBaseMySQL


def execute_sql(sql=""" SELECT id, question FROM fqaitem WHERE need_push = "no"  AND is_del = "no" """):
    """从数据库中获取随机用例"""
    dbinfo = {
        "host": "172.16.13.134",
        "user": "bigdata_sync",
        "password": "1qaz@WSX",
        "port": 31145,
        "dbname": "kbs_cms",
        "dbtype": "mysql",
        "dbengine": "pymysql"
    }
    data = DataBaseMySQL(dbinfo).query(sql)

    return data


def execute_one_test_2022(question, exp_group_id):
    url = f"http://172.16.23.9:8000/api/getSimilarQueryLdg?threshold=0.7&uQuery={question}"
    res = requests.request(method="GET", url=url, verify=False, timeout=30)
    try:
        result = res.json()["finalCandidate"]
        act_group_id = result["qgroupId"]
        if str(act_group_id) == str(exp_group_id):
            success = True
        else:
            success = False
    except:
        result = "null"
        act_group_id = ""
        success = False
    return {"status_code": res.status_code,
            "success": success,
            "question": question,
            "exp_group_id": exp_group_id,
            "act_group_id": act_group_id,
            "response_data": result}


def execute_one_test_2023(question, exp_group_id):
    """执行单条测试"""
    # url = f"http://172.16.23.9:8000/api/getSimilarQuery?threshold=0.88&uQuery={question}"
    url = f"http://172.16.23.9:8000/api/getSimilarQueryTmp?threshold=0.8&uQuery={question}"
    res = requests.request(method="GET", url=url, verify=False, timeout=30)
    try:
        result = res.json()["finalCandidate"]
        act_group_id = result["qgroupId"]
        if str(act_group_id) == str(exp_group_id):
            success = True
        else:
            success = False
    except:
        result = "null"
        act_group_id = ""
        success = False
    return {"status_code": res.status_code,
            "success": success,
            "question": question,
            "exp_group_id": exp_group_id,
            "act_group_id": act_group_id,
            "response_data": result}


def qa_test_2023(case_data):
    """执行多条测试"""
    test_results = []
    for d in case_data:
        questions = d["question"]
        if "[" in questions and "]" in questions:
            question = json.loads(questions)[-1]
        else:
            question = questions

        if d.__contains__("exp_group_id"):
            exp_group_id = d["exp_group_id"]
        elif d.__contains__("id"):
            exp_group_id = d["id"]
        else:
            exp_group_id = 0
        result = execute_one_test_2023(question, exp_group_id)
        test_results.append(result)
    return test_results


def qa_test_2022(case_data):
    test_results = []
    for d in case_data:
        questions = d["question"]
        if len(questions) < 3:
            continue
        if type(questions) != str:
            continue
        if "[" in questions and "]" in questions:
            question = json.loads(questions)[-1]
        else:
            question = questions

        if d.__contains__("exp_group_id"):
            exp_group_id = d["exp_group_id"]
        elif d.__contains__("id"):
            exp_group_id = d["id"]
        else:
            exp_group_id = 0
        result = execute_one_test_2022(question, exp_group_id)
        test_results.append(result)
    return test_results


def write_results(results_data, algo_type):
    """测试报告写入到xlsx 保存至本地"""
    file_name = f"./fqa测试algo{algo_type}-{str(datetime.datetime.now())[:10]}-{uuid.uuid4()}.xlsx"
    print(file_name)
    Handlers.write_list_map_as_excel(list_map=results_data,
                                     excel_writer=file_name,
                                     sheet_name="Sheet1", index=False)


def handle_original_data(original_data, sample=10000):
    """从原始数据中随机sample出来 按照既定格式组装成用例"""
    data = random.sample(original_data, sample)
    return data


cases = []


def get_cases_from_database(sample=10000):
    """按照规则查找并返回用例集"""
    original_sql = """ SELECT id, question FROM fqaitem WHERE need_push = "no"  AND is_del = "no"; """
    total_sql = """ SELECT count(1) as total FROM fqaitem WHERE need_push = "no"  AND is_del = "no"; """
    total_result = execute_sql(total_sql)
    total = total_result[0]["total"]  # 符合条件的用例的总数

    group_by_sql = """
        SELECT cate_id, count( 1 ) AS total 
        FROM fqaitem 
        WHERE need_push = "no"  AND is_del = "no" 
        GROUP BY cate_id 
        ORDER BY total DESC;
        """
    group_by_result = execute_sql(group_by_sql)
    for g in group_by_result:
        cate_id = g["cate_id"]
        type_sample = int((int(g["total"]) / int(total)) * sample) + 1
        type_sql = f""" SELECT id, question, answer FROM fqaitem 
        WHERE need_push = "no"  AND is_del = "no" AND cate_id = {cate_id}; """
        data = execute_sql(type_sql)
        original_data = handle_original_data(data, type_sample)
        for case in original_data:
            questions = case["question"]
            if type(questions) != str:
                continue
            try:
                # 观测用例总数是否已满足
                if len(cases) >= sample:
                    return cases

                questions = json.loads(questions)
                # 去除q中含有空格的部分
                while '' in questions:
                    questions.remove('')
                # 排除一个group中只有两个以下q的组
                if len(questions) < 2:
                    continue

                if "/" in questions[-1] or \
                        "《" in questions[-1] or \
                        "，" in questions[-1] or \
                        '"' in questions[-1] or \
                        '(' in questions[-1]:
                    continue

                answers = json.loads(case["answer"])
                while '' in answers:
                    answers.remove("")
                cases.append({
                    "exp_group_id": case["id"],
                    "cate_id": cate_id,
                    "question": questions[-1],
                    "answer": "&&".join(answers)
                })
            except:
                continue
    if len(cases) < sample:
        return get_cases_from_database(sample)
    return cases


def get_cases_from_database_about_data():
    """查询达闼机器人相关fqaitem"""
    inner_cases, cate_ids, result = [], [], [{"cate_id": "51"}]
    while len(result) > 0:
        this_search_pids = [str(it["cate_id"]) for it in result]
        cate_ids += this_search_pids
        result = execute_sql(f"""select id cate_id from fqacate 
        where is_del='no' and need_push='no' and pid in ({",".join(this_search_pids)});""")

    data_sql = f""" SELECT id, question, answer, cate_id FROM fqaitem 
        WHERE need_push = "no"  AND is_del = "no" AND cate_id in ({",".join(cate_ids)}); """
    data_result = execute_sql(data_sql)

    for case in data_result:
        questions = case["question"]
        if type(questions) != str:
            continue
        try:
            questions = json.loads(questions)
            # 去除q中含有空格的部分
            while '' in questions:
                questions.remove('')

            answers = json.loads(case["answer"])
            while '' in answers:
                answers.remove("")
            inner_cases.append({
                "exp_group_id": case["id"],
                "cate_id": case["cate_id"],
                "question": questions[-1],
                "answer": "&&".join(answers)
            })
        except:
            continue
    return inner_cases


def execute_cases_randomly_from_database(algo_type=2023):
    """根据模型版本 执行数据库用例测试"""
    original_data = get_cases_from_database(sample=10000)
    if algo_type == 2022:
        test_result = qa_test_2022(original_data)
    else:
        test_result = qa_test_2023(original_data)
    write_results(test_result, algo_type)


def execute_cases_by_xlsx(filename, sheet_name="Sheet1", algo_type=2022):
    """根据模型版本 执行xlsx表格用例测试"""
    cases = Handlers.read_excel_as_list_map(io=filename, sheet_name=sheet_name)
    if algo_type == 2022:
        test_result = qa_test_2022(cases)
    else:
        test_result = qa_test_2023(cases)
    write_results(test_result, algo_type)


if __name__ == '__main__':
    """收集用例流程 写入xlsx"""
    duplicated_data = Handlers.read_excel_as_list_map(io="./fqaitem_duplication2-2023-01-17.xlsx", sheet_name="Sheet1")
    duplicated_questions = []
    for item in duplicated_data:
        duplicated_questions.append(item["问法"])

    final_cases = []
    c = get_cases_from_database(20000)
    for case in c:
        if case["question"] not in duplicated_questions:
            final_cases.append(case)
    # 补充达闼相关的case
    final_cases += get_cases_from_database_about_data()

    Handlers.write_list_map_as_excel(list_map=final_cases,
                                     excel_writer=f"./fqa测试用例-{str(datetime.datetime.now())[:10]}.xlsx",
                                     sheet_name="Sheet1", index=False)

if __name__ != '__main__':
    # execute_cases_by_xlsx(r"D:\GitLab\develop\nlpauto\test\fqa测试用例-2023-01-05.xlsx",
    #                       sheet_name="Sheet1", algo_type=2022)
    execute_cases_by_xlsx(r"D:\GitLab\develop\nlpauto\test\fqa测试用例-2023-01-05.xlsx",
                          sheet_name="Sheet1", algo_type=2023)
