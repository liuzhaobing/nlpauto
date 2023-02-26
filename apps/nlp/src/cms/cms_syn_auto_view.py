#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from django.http import HttpResponse

from apps.nlp.src.cms.cms_syn_auto import CMSSync


def auto_sync(request):
    days = 15
    CMSSync().main(days)
    return HttpResponse("CMS最近{}天数据变更同步到QA测试集成功！".format(days))
