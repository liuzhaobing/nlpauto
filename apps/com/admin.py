from django.contrib import admin
from apps.com.src.upload_views import *


class UploadAdmin(admin.ModelAdmin):
    list_display = ["id", "file_name", "file_path"]


admin.site.register(UploadFileModel, UploadAdmin)
