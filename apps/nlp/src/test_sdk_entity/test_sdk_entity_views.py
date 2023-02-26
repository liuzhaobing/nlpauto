#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json

from apps.nlp.src.test_sdk_entity.test_sdk_entity import excel_batch_file_runner


def run_sdk_entity_views(job_config, *args, **kwargs):
    """
    job_config = {
                "id": 1,
                "name": "实体测试任务",
                "desc": "实体测试任务",
                "task_type": entity_test,
                "plan_id": 1,
                "base_config": "",
                "task_config": "",
                "file_name": "",
                "db_filter": "usetest=1"
            }
    base_config = {"feishuwebhook":"https://open.feishu.cn/open-apis/bot/v2/hook/c0ea24df-4894-4aeb-a9df-812b6653564d","cronstring":"0 2 * * *","name":"实体测试任务"}
    task_config = "{"chan_num":5,"conn_addr":"http://172.16.23.15:30068/nlp-sdk/nlu/intent-recognize","file_names":[],"sheet_name":"Sheet1","file_chan_num":5}"
    """
    base_config = json.loads(job_config["base_config"])
    task_config = json.loads(job_config["task_config"])
    excel_batch_file_runner(url=task_config["conn_addr"],
                            file_names=task_config["files"],
                            sheet_name=task_config["sheet_name"],
                            file_chan_num=task_config["file_chan_num"],
                            case_chan_num=task_config["chan_num"])
    pass
