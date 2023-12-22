from django.db import models

from users.settings import MEDIA_ADDRESS


class Picture(models.Model):
    picture = models.ImageField(
        upload_to='markdownPictures/',
        verbose_name='图片'
    )

    def get_pic_url(self):
        return MEDIA_ADDRESS + str(self.picture)