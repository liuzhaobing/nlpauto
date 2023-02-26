#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import re

from django.db import models
from django.http import HttpResponse
from rest_framework import serializers, status
from rest_framework.response import Response

from conf.env import *
from utils.base_model import BaseModel
from utils.handler import Handlers
from utils.viewset import CustomModelViewSet


class UploadFileModel(BaseModel):
    class Meta:
        db_table = "media_files"
        verbose_name = "文件上传"
        verbose_name_plural = "文件上传"

    id = models.AutoField(primary_key=True, help_text="文件id")
    file_name = models.CharField(max_length=200, null=True, verbose_name="文件名称", help_text="文件名称")
    file_path = models.CharField(max_length=200, null=True, verbose_name="文件路径", help_text="文件路径")


class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFileModel
        fields = "__all__"


class UploadFileView(CustomModelViewSet):
    """文件上传"""
    queryset = UploadFileModel.objects.all()
    serializer_class = UploadFileSerializer
    lookup_field = "id"

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        from urllib import parse  # 解决ascii编码问题
        return HttpResponse(parse.unquote(json.dumps(serializer.data)))

    def create(self, request, *args, **kwargs):
        # 提取文件
        data = request.data
        req = request.FILES.get('file')
        file_type = re.match(r'.*\.(txt|xlsx|xls)', req.name)

        if not file_type:
            response = {'status': 'failure', 'msg': '文件类型不匹配, 请重新上传'}
            return HttpResponse(json.dumps(response))

        file_name = req.name
        file_name = file_name.split(".")[0] + Handlers.time_strf_now() + "." + file_name.split(".")[-1]
        file_path = os.path.join(UPLOAD_PATH_RELATIVE, file_name)

        # 判断入参中是否有file_name
        if "file_name" in data.keys():
            if not data["file_name"]:
                data["file_name"] = file_name
        else:
            data["file_name"] = file_name

        data["file_path"] = file_path

        # 指定目录下的打开并写入文件
        with open(file_path, 'wb+') as f:
            for chunk in req.chunks():  # 分块写入文件
                f.write(chunk)

        # 存入数据库
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
