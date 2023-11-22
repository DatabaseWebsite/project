from django.contrib.auth import get_user_model
from django.db import models


class AuthRecord(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True, verbose_name='登录信息id')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='登录用户')
    login_at = models.DateTimeField(verbose_name='登录时间')
    expires_by = models.DateTimeField(verbose_name='有效期时长')

    class Meta:
        default_permissions = ()
