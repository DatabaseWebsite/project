from django.db import models

from users.models import User


class Notice(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="创建者")
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
