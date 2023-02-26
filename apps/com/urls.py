#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from django.urls import path, re_path
from rest_framework import routers

from apps.com.src.upload_views import *
from apps.com.src.download_views import *


tts_url = routers.SimpleRouter(trailing_slash=False)
tts_url.register(r"upload", UploadFileView, basename="upload")
tts_url.register(r"", ExportFile, basename="download")

urlpatterns = [
]
urlpatterns += tts_url.urls
