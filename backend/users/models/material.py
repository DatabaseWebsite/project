from django.db import models

from users.models import User, Course
from users.settings import MEDIA_ADDRESS


class Material(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="上传用户"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="所属课程"
    )

    file = models.FileField(upload_to='material/')

    file_name = models.CharField(max_length=255, verbose_name="材料名称")

    created_at = models.DateTimeField(auto_now_add=True)

    def get_file_url(self):
        return MEDIA_ADDRESS + str(self.file)
