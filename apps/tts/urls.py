#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from rest_framework import routers

from apps.tts.src.text_aggregation.text_aggregation_views import TextAggregationView

tts_url = routers.SimpleRouter(trailing_slash=False)
tts_url.register(r"aggregation", TextAggregationView, basename="aggregation")

urlpatterns = [
]
urlpatterns += tts_url.urls
