from django.db import models

from users.models import User, Course


class Category(models.TextChoices):
    CLASS = 'c', "通知"
    WORK = 'w', "作业批改"
    DISCUSSION = 'd', "讨论区更新"
    OTHER = 'o', "其他通知"


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='received_messages', null=True, on_delete=models.SET_NULL)
    receiver = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    send_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    type = models.CharField(choices=Category.choices, max_length=100, null=True, blank=True)
    read = models.BooleanField(default=False, verbose_name="是否已读")