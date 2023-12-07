from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models.normal_homework import NormalHomework
from users.settings import MEDIA_ADDRESS


class NormalHomeworkSubmit(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='学生')
    homework = models.ForeignKey(NormalHomework, on_delete=models.CASCADE, verbose_name='作业')
    score = models.IntegerField(
        validators=[
            MinValueValidator(0, message="Grade must be at least 0."),
            MaxValueValidator(100, message="Grade must be at most 100.")
        ],
        blank=True,
        null=True
    )
    submit_time = models.DateTimeField(verbose_name='提交时间', auto_now_add=True)
    file = models.FileField(upload_to='homework/')

    def get_file_url(self):
        return MEDIA_ADDRESS + str(self.file)