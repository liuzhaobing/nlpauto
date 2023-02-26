#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from rest_framework.response import Response

from utils.base_model import BaseModel
from django.db import models
from rest_framework import serializers, viewsets


class JobModel(BaseModel):
    class Meta:
        db_table = "job"
        verbose_name = "测试任务"
        verbose_name_plural = "测试任务"

    id = models.AutoField(primary_key=True, help_text="测试任务id")
    name = models.CharField(verbose_name="测试任务名称name", max_length=50, unique=True, help_text="测试任务名称name")
    desc = models.CharField(verbose_name="测试任务描述desc", null=True, max_length=100, help_text="测试任务描述desc")
    task_type = models.TextField(verbose_name="任务类型", null=True, help_text="任务类型")
    plan_id = models.IntegerField(verbose_name="关联的测试计划id", help_text="关联的测试计划id", default=1)
    base_config = models.TextField(verbose_name="任务共有配置", null=True, help_text="任务共有配置")
    task_config = models.TextField(verbose_name="任务私有配置", help_text="任务私有配置")
    file_name = models.TextField(verbose_name="文件", help_text="文件")
    db_filter = models.TextField(verbose_name="数据库过滤条件", null=True, help_text="数据库过滤条件")


class JobModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobModel
        fields = "__all__"


class JobView(viewsets.ModelViewSet):
    queryset = JobModel.objects.all()
    serializer_class = JobModelSerializer
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # job_info = serializer.data
        # if job_info["task_type"] == "skill_db":
        #     pass
        return Response(serializer.data)
