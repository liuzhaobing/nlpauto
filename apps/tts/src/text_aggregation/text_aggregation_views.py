#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import threading
from django.db import models
from rest_framework import serializers
from rest_framework.response import Response

from apps.tts.src.text_aggregation.text_aggregation import main
from utils.base_model import BaseModel
from conf.env import *
from utils.handler import Handlers
from utils.viewset import CustomModelViewSet


class TextAggregationModel(BaseModel):
    class Meta:
        db_table = "tts_ta"
        verbose_name = "文本聚合"
        verbose_name_plural = "文本聚合"

    id = models.AutoField(primary_key=True, help_text="文本聚合任务id")
    name = models.CharField(verbose_name="文本聚合任务名称name", max_length=50, unique=True, help_text="文本聚合任务名称name")
    desc = models.CharField(verbose_name="文本聚合任务描述desc", null=True, max_length=100, help_text="文本聚合任务描述desc")
    source_file = models.TextField(verbose_name="文本聚合任务原文件source_file", null=True, help_text="文本聚合任务原文件source_file")
    output_file = models.TextField(verbose_name="文本聚合任务目标文件output_file", null=True, help_text="文本聚合任务目标文件output_file")
    sheet_name = models.TextField(verbose_name="文件sheet_name", help_text="文件sheet_name")
    column_name = models.TextField(verbose_name="文件column_name", help_text="文件column_name")
    distance = models.FloatField(verbose_name="distance", null=True, help_text="distance", default=0.2)
    min_samples = models.IntegerField(verbose_name="min_samples", null=True, help_text="min_samples", default=3)


class TextAggregationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextAggregationModel
        fields = "__all__"


class TextAggregationView(CustomModelViewSet):
    """文本聚合"""
    queryset = TextAggregationModel.objects.all()
    serializer_class = TextAggregationSerializer
    lookup_field = "id"

    # GET aggregation/{id}/
    def retrieve(self, request, *args, **kwargs):
        # 查询任务详情
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        info = serializer.data
        if "http" in info["source_file"]:
            try:
                info["source_file"] = "media" + info["source_file"].split("media")[1]
            except:
                pass

        # 先定义输出的文件全路径
        path = os.path.join(TEXT_AGGREGATION_PATH_RELATIVE,
                            Handlers.return_file_name(info["source_file"]).split(".")[0] + Handlers.time_strf_now() + ".xlsx")
        info["output_file"] = path.replace("\\", "/")

        # 开启子线程去执行文本聚合任务
        t = threading.Thread(target=main, args=(info["source_file"], info["output_file"], info["sheet_name"],
                                                info["column_name"], info["distance"], info["min_samples"],))
        t.start()  # t.join()  # 阻塞线程

        # 主线程不用等子线程，直接处理数据库并返回结果给前端
        partial = kwargs.pop('partial', False)
        instance2 = self.get_object()
        serializer2 = self.get_serializer(instance2, data=info, partial=partial)
        serializer2.is_valid(raise_exception=True)
        self.perform_update(serializer2)

        if getattr(instance2, '_prefetched_objects_cache', None):
            instance2._prefetched_objects_cache = {}

        return Response(serializer2.data)
