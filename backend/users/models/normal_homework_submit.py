from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver

from users.models import User
from users.models.normal_homework import NormalHomework
from users.settings import MEDIA_ADDRESS


class NormalHomeworkSubmit(models.Model):
    user = models.ForeignKey(User, related_name="submitter", on_delete=models.CASCADE, verbose_name='学生')
    homework = models.ForeignKey(NormalHomework, on_delete=models.CASCADE, verbose_name='作业')
    score = models.IntegerField(blank=True, null=True)
    submit_time = models.DateTimeField(verbose_name='提交时间', auto_now_add=True)
    content = models.CharField(max_length=1000, verbose_name='作业文本', default="空", blank=True, null=True)
    file = models.FileField(upload_to='homework_submit/', blank=True, null=True)
    markingPerson = models.ForeignKey(User, related_name="marker", on_delete=models.SET_NULL, verbose_name='评分人', blank=True, null=True)

    def get_file_url(self):
        return MEDIA_ADDRESS + str(self.file)


@receiver(pre_save, sender=NormalHomeworkSubmit)
def check_and_adjust_score(sender, instance, **kwargs):
    if instance.score and int(instance.score) > 100:
        instance.score = instance.homework.totalScorse
