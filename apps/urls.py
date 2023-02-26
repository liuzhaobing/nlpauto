#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from django.urls import path, include, re_path

urlpatterns = [
    # apps
    path('common/', include('apps.com.urls')),
    path('tts/', include('apps.tts.urls')),
    path('asr/', include('apps.asr.urls')),
    path('nlp/', include('apps.nlp.urls')),

]
