# -*- coding:utf-8 -*-
from django.http import HttpResponse

from apps.nlp.src.cms.badcase_tagging import badcase_tagging_push


def auto_badcase_tagging_push(request):
    result, task_name = badcase_tagging_push(exclude_domain=["indoornavigation", "around"])
    if result:
        return HttpResponse(f"success! {task_name}")
    return HttpResponse(f"failure! {task_name}")
