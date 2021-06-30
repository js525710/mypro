# -*- coding: utf-8 -*-
"""
@Time ： 2020/12/15 10:35
@Auth ： shan.jin01
@Function ：项目错误码和返回体
"""
from rest_framework import serializers
from api.models import UserInfo


# 对Response字段的描述
class UserInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, help_text="用户id")
    username = serializers.IntegerField(read_only=True, help_text="用户名")
    pwd = serializers.IntegerField(read_only=True, help_text="登录密码")
    nickname = serializers.CharField(read_only=True, help_text="昵称")
    description = serializers.CharField(read_only=True, help_text="描述")

    class Meta:
        model = UserInfo
        # 全要的话写__all__
        fields = '__all__'
        # 必须保证和上面你要描述的字段一模一样
        # fields = ('id', 'username', 'pwd', 'nickname','description')


# 对错误码的描述
class UserErrCode(serializers.ModelSerializer):
    code_1000 = serializers.IntegerField(read_only=True, help_text="登录成功")
    code_1001 = serializers.IntegerField(read_only=True, help_text="用户名密码错误")

    class Meta:
        model = UserInfo
        # 全要的话写__all__
        fields = '__all__'
        # 必须保证和上面你要描述的字段一模一样
        fields = ('code_1000', 'code_1001')
