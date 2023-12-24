from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='课程名称')
    startTime = models.DateTimeField(blank=True, null=True)
    endTime = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=1000, default="无", null=True, blank=True)
