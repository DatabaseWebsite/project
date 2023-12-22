from django.db import models

from users.models import User
from users.models.forum import Post


class SubscriptionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

