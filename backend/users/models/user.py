from django.contrib.auth.models import AbstractUser
from django.db import models

from users.models.course import Course
from users.settings import MEDIA_ADDRESS


class User(AbstractUser):
    name = models.CharField(
        max_length=150,
        verbose_name='姓名',
        blank=True
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default.png',
        verbose_name='头像'
    )

    current_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="当前课程",
        null=True,
        blank=True
    )

    is_admin = models.BooleanField(
        default=False,
        verbose_name='是否为管理员'
    )

    grade = models.CharField(
        max_length=100,
        verbose_name='年级',
        blank=True
    )

    college = models.CharField(
        max_length=100,
        verbose_name='学院',
        blank=True
    )

    major = models.CharField(
        max_length=100,
        verbose_name='专业',
        blank=True
    )

    def get_avatar_url(self):
        return MEDIA_ADDRESS + str(self.avatar)
