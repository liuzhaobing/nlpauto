# -*- coding:utf-8 -*-
import requests


def run_task_by_id(task_id):
    res = requests.request(method="GET", url=f"http://172.16.23.33:8087/api/v1/task/runtask?task_id={task_id}")
    if res.status_code == 200:
        return True
    return False


def get_all_tasks():
    res = requests.request(method="GET", url="http://172.16.23.33:8087/api/v1/task/getInfolist")
    if res.status_code == 200:
        return res.json()["data"]
    return None


def get_task_id(user_query, data):
    for job in data:
        if user_query == job["task_config"]["base_config"]["name"]:
            task_id = job["task_id"]
            return task_id
        if user_query == str(job["task_id"]):
            task_id = int(user_query)
            return task_id
    return 0


def check_user_query():
    user_query = proResult["quresult"]["request_params"]["query"]
    data = get_all_tasks()
    if not data:
        return "不好意思，未能成功获取到任务列表~"

    if user_query == "展开全部":
        jobs = ""
        for job in data:
            task_id = job["task_id"]
            task_name = job["task_config"]["base_config"]["name"]
            jobs += f"[{task_id}] {task_name}\n"
        return jobs

    task_id = get_task_id(user_query, data)
    if task_id:
        result = run_task_by_id(task_id)
        if result:
            return f"已成功运行task_id={task_id}，请稍等~"
        else:
            return "运行失败，请重试~"
    else:
        return "未找到对应任务，请重试~"


proResult["answers"] = [check_user_query()]


def get_task_list():
    res = requests.request(method="GET", url="http://172.16.23.33:8087/api/v1/task/getInfolist")
    if res.status_code == 200:
        data = res.json()["data"]
        jobs = ""
        for i in range(10):
            job = data[i]
            task_id = job["task_id"]
            task_name = job["task_config"]["base_config"]["name"]
            jobs += f"\n[{task_id}] {task_name}"
        return jobs, data
    return None, None


jobs, data = get_task_list()
if jobs:
    answer_string = "找到如下任务，通过输入任务id来执行测试任务。\n如果列表中没有想要执行的任务，请输入【展开全部】"
    proResult["answers"] = [answer_string + jobs]
else:
    proResult["answers"] = ["不好意思，未能成功获取到任务列表~"]
