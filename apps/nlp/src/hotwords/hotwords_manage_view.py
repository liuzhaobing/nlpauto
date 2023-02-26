#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from django.http import JsonResponse

from apps.nlp.src.common.smartvoice import SmartVoiceHWMange
import json


def hotwords(request):
    """
    request.body:
    {
        "base_url": "http://172.16.23.85:30950",
        "login_user": "admin@cloudminds",
        "login_passwd": "Smartvoice1506",
        "agent_id": "1223",
        "agent_name": "",
        "action": "del",
        "hws": [
            "今天天气针不戳",
            "小乔流水人家",
            "师公许可",
            "640层ct室",
            "为什么我的眼里常含泪水"
        ]
    }
    """

    if request.method == "POST":
        try:
            req_payload = json.loads(request.body)
            hw_instance = SmartVoiceHWMange(req_payload["base_url"],
                                            req_payload["login_user"],
                                            req_payload["login_passwd"],
                                            req_payload["agent_id"],
                                            req_payload["agent_name"])
        except Exception as e:
            return JsonResponse({"status": "failure", "error": e})

        if req_payload["action"] == "add":
            try:
                for hw in req_payload["hws"]:
                    hw_instance.add_hw(hw)
                hw_instance.activate_hw()
                return JsonResponse({"status": "success", "error": ""})
            except Exception as e:
                return JsonResponse({"status": "failure", "error": e})

        elif req_payload["action"] == "del":
            try:
                hws = req_payload["hws"]
                hw_instance.del_hw_by_names(hws)
                return JsonResponse({"status": "success", "error": ""})
            except Exception as e:
                return JsonResponse({"status": "failure", "error": e})
