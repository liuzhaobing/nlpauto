#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# coding:utf-8

import json
import os
from django.http import HttpResponse, StreamingHttpResponse
from django.utils.encoding import escape_uri_path
from rest_framework import viewsets, status
from rest_framework.decorators import action
from utils.handler import Handlers


class ExportFile(viewsets.GenericViewSet):
    @staticmethod
    def file_iterator(download_file, chunk_size=1024):
        with open(download_file, "rb") as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    @action(methods=["GET"], detail=False)
    def download(self, request):
        """文件下载"""
        file_path = request.GET["file"]
        if not os.path.exists(file_path):
            return HttpResponse(json.dumps({"success": False, "error": u"文件不存在，请稍后再试！"}),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content_type="text/json")
        try:
            file_name = os.path.basename(file_path)
            # file_name = "download_{timestamp}_{file_name}".format(file_name=file_name,
            #                                                       timestamp=Handlers.time_strf_now())
            response = StreamingHttpResponse(self.file_iterator(file_path))
            response["Content-Type"] = "application/octet-stream"
            response["COntent-Disposition"] = "attachment;filename*=utf-8''{}".format(escape_uri_path(file_name))
            return response

        except Exception as e:
            return HttpResponse(json.dumps({"success": False, "error": u"文件下载失败，原因：" + str(e)}),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                content_type="text/json")
