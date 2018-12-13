from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='Deleted user')[0]


class Profile(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE)
    # photo        = models.ImageField(default='default_user.jpg', upload_to='profile_pics')
    about_myself = models.TextField(max_length=256, null=True, blank=True)


class Tweet(models.Model):
    author            = models.ForeignKey(User, on_delete=models.CASCADE)
    content           = models.TextField()
    creation_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime   = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('tweet-details', kwargs={'pk': self.pk})


# class Comment(models.Model):
#     author = models.ForeignKey(
#         User,
#         on_delete=models.SET(get_sentinel_user),
#         related_name='messages_from_user'
#     )
#     content           = models.TextField()
#     creation_datetime = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.SET(get_sentinel_user),
        related_name='messages_from_user'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.SET(get_sentinel_user),
        related_name='messages_to_user'
    )
    content           = models.TextField()
    creation_datetime = models.DateTimeField(auto_now_add=True)
    is_read           = models.BooleanField(default=False)
