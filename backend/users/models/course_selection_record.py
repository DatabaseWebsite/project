from django.db import models

from users.models import User, Course


class Category(models.TextChoices):
    TEACHER = 't', "老师"
    ASSISTANT = 'a', "助教"
    STUDENT = 's', "学生"
    ADMIN = 'd', '管理员'


class CourseSelectionRecord(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户'
    )

    selected_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='所选课程',
        null=True,
        blank=True
    )

    type = models.CharField(
        verbose_name="人员类型",
        max_length=10,
        choices=Category.choices,
        null=False,
        blank=False
    )
