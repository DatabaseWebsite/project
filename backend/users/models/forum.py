from django.contrib.auth.models import AbstractUser
from django.db import models

from users.models import User
from users.models.course import Course
from users.settings import MEDIA_ADDRESS


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="创建者")
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    post_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="隶属课程")


class Reply(models.Model):
    replier = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="创建者")
    content = models.CharField(max_length=2000)
    reply_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="隶属帖子")
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name="回复对象", blank=True, null=True)