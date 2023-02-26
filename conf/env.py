#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
from pathlib import Path
# ================================================= #
# ************** 数据库 配置  ************** #
# ================================================= #

# sqlite3 设置
# DATABASE_ENGINE = "django.db.backends.sqlite3"
# DATABASE_NAME = os.path.join(BASE_DIR, 'db.sqlite3')

# mysql 配置
DATABASE_ENGINE = "django.db.backends.mysql"
DATABASE_MYSQL_GO = 'nlpautotest'
DATABASE_MYSQL_PYTHON = 'nlpauto'
DATABASE_HOST = "localhost"
DATABASE_PORT = 3306
DATABASE_USER = "root"
DATABASE_PASSWORD = ""

# cms 备库
CMS_DB = 'kbs_cms'
CMS_HOST = "172.16.13.134"
CMS_PORT = 31145
CMS_USER = "bigdata_sync"
CMS_PASSWORD = "1qaz@WSX"

# 测试用例 库
CASE_DB = "nlpautotest"
CASE_HOST = "172.16.23.33"
CASE_PORT = 3306
CASE_USER = "root"
CASE_PASSWORD = ""

# 文件路径配置
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_PATH = os.path.join(BASE_DIR, 'media', 'logs', 'mytest.log')
UPLOAD_PATH_RELATIVE = os.path.join('media', 'upload')
UPLOAD_PATH = os.path.join(BASE_DIR, UPLOAD_PATH_RELATIVE, 'upload_file.xlsx')
TEXT_AGGREGATION_PATH_RELATIVE = os.path.join('media', 'tts', 'text_aggregation')
TEXT_AGGREGATION_PATH = os.path.join(BASE_DIR, TEXT_AGGREGATION_PATH_RELATIVE, '文本聚类结果.xlsx')
TEST_SDK_ENTITY_PATH_RELATIVE = os.path.join('media', 'nlp', 'test_sdk_entity')
TEST_SDK_ENTITY_PATH = os.path.join(BASE_DIR, TEST_SDK_ENTITY_PATH_RELATIVE, '实体测试结果.xlsx')
SKILL_BADCASE_AUTO_PULL_PATH_RELATIVE = os.path.join('media', 'nlp', 'skill')
SKILL_BADCASE_AUTO_PULL_PATH = os.path.join(BASE_DIR, SKILL_BADCASE_AUTO_PULL_PATH_RELATIVE, 'week2022-07-04_07-11.xlsx')

# mongo 配置
"""
auto_task:用于存放测试任务相关配置信息
auto_task_rl:用于存放关系（auto_task._id,execute_time,auto_task_cases._id,auto_task_results._id）
auto_task_cases:用于存放测试用例
auto_task_results:用于存放测试结果
"""
MG_HOST = "mongodb://root:123456@10.12.32.30:27017"
MG_DB = "nluauto"
MG_COL_TASK = "auto_task"
MG_COL_RL = "auto_task_rl"
MG_COL_CASES = "auto_task_cases"
MG_COL_RESULTS = "auto_task_results"
