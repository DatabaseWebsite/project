from django.db import models


class LoginLog(models.Model):
    ip = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    browser = models.CharField(max_length=20)
    time = models.DateTimeField(verbose_name='登录时间')
    username = models.CharField(max_length=20)


class OperationLog(models.Model):
    request_module = models.CharField(max_length=20)
    api = models.CharField(max_length=100)
    operation = models.CharField(max_length=20)
    ip = models.CharField(max_length=20)
    browser = models.CharField(max_length=20)
    time = models.DateTimeField(verbose_name='操作时间')
    status = models.CharField(max_length=20)
    code = models.CharField(max_length=20)
    username = models.CharField(max_length=20)