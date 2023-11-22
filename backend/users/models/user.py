from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

MEDIA_ADDRESS = ''


class Category(models.TextChoices):
    TEACHER = 't', "老师"
    ASSISTANT = 'a', "助教"
    STUDENT = 's', "学生"


class User(AbstractUser):
    # 姓名
    name = models.CharField(max_length=150, verbose_name='姓名')
    # 人员类别
    category = models.CharField(verbose_name="Task status", max_length=1, choices=Category.choices)
    # 头像
    avatar = models.ImageField(upload_to='avatars/', default='avatar/default.png', verbose_name='头像')
    # 所选课程
    course = models.CharField(max_length=123, default='数据库', verbose_name='所选课程，temp，以后要改成外键')

    def get_avatar_url(self):
        return MEDIA_ADDRESS + str(self.avatar)
