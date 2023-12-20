from django.db import models

from users.models import User, Course


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    send_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
