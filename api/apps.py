import logging

from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    # 初始化
    logger = logging.getLogger('log')

# 全局变量方便调用
logger = ApiConfig.logger
