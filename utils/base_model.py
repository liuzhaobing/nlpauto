#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from django.db import models


class BaseModel(models.Model):
    """
    数据库表公共字段
    """
    class Meta:
        abstract = True  # 为抽象模型类，用于其他模型来继承，数据库迁移时不会创建此表
        verbose_name = "公共字段表"
        db_table = "BaseModel"

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name="逻辑删除", help_text="逻辑删除")
