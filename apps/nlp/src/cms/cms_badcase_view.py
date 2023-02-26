#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import os.path
from django.http import HttpResponse
from apps.nlp.src.cms.cms_badcase import runner
from conf.env import SKILL_BADCASE_AUTO_PULL_PATH, SKILL_BADCASE_AUTO_PULL_PATH_RELATIVE
from utils.handler import Handlers


def auto_pull_badcase(request):
    file_path = SKILL_BADCASE_AUTO_PULL_PATH_RELATIVE
    Handlers.make_parent_dirs(SKILL_BADCASE_AUTO_PULL_PATH)
    file_name, case_num = runner(file_path=file_path)
    return HttpResponse(json.dumps({"success": True,
                                    "file_name": file_name,
                                    "file_path": file_path,
                                    "count": case_num}))
