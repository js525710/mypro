from django.db import models


# Create your models here.

class UserInfo1(models.Model):
    class Meta:
        # 指定数据表名
        db_table = 'userinfo'
    # 下面表的字段必须和表的字段名称一样
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=31, default=None)
    pwd = models.CharField(max_length=31, default=None)
    nickname = models.CharField(max_length=255, default=None)
    description = models.CharField(max_length=255, default=None)
