from datetime import timedelta

from django.db import models
from django.utils import timezone

from users.models import Course


class NormalHomework(models.Model):
    start_time = models.DateTimeField(verbose_name='作业开始时间', auto_now_add=True)
    end_time = models.DateTimeField(verbose_name='作业结束时间')
    title = models.CharField(max_length=100, verbose_name='作业题目', default='无题目')
    content = models.CharField(max_length=1000, verbose_name='作业内容')
    belong_to_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='隶属课程')
    file = models.FileField(upload_to="homework/", blank=True, null=True)

