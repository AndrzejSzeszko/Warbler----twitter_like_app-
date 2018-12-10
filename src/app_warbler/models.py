from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE)
    # photo        = models.
    about_myself = models.TextField(max_length=256, null=True, blank=True)


class Tweet(models.Model):
    user              = models.ForeignKey(User, on_delete=models.CASCADE)
    content           = models.TextField()
    creation_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime   = models.DateTimeField(auto_now=True)

