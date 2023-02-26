#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from django.urls import path

from apps.nlp.src.cms.badcase_tagging_view import auto_badcase_tagging_push
from apps.nlp.src.cms.cms_syn_auto_view import auto_sync
from apps.nlp.src.hotwords.hotwords_manage_view import hotwords

urlpatterns = [
    path('cms/qa_sync', auto_sync),
    path('tagging/push', auto_badcase_tagging_push),
    path('sv/hotwords', hotwords)
]
