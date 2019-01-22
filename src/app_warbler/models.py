from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models
from PIL import Image


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='Deleted user')[0]


class Profile(models.Model):
    user         = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    photo        = models.ImageField(default='default_user.jpg', upload_to='profile_pics', )
    about_myself = models.TextField(max_length=256, null=True, blank=True)
    is_blocked   = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}\' profile'

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.photo)
        if img.height > 250 or img.width > 250:
            output_size = (250, 250)
            img.thumbnail(output_size)
            img.save(self.photo.path)


class Tweet(models.Model):
    author            = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tweet_content     = models.TextField()
    creation_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime   = models.DateTimeField(auto_now=True)
    is_blocked        = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('tweet-details', kwargs={'pk': self.pk})

    def __str__(self):
        return f'Tweet {self.pk} by {self.author} on {self.update_datetime.strftime("%Y/%m/%d %H:%M:%S")}'


class Comment(models.Model):
    author            = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user))
    tweet             = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    comment_content   = models.TextField()
    creation_datetime = models.DateTimeField(auto_now_add=True)
    is_blocked        = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment {self.pk} on tweet {self.tweet_id} by {self.author} on {self.creation_datetime.strftime("%Y/%m/%d %H:%M:%S")}'


class Message(models.Model):
    from_user         = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), related_name='messages_from_user')
    to_user           = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user), related_name='messages_to_user')
    message_content   = models.TextField()
    creation_datetime = models.DateTimeField(auto_now_add=True)
    is_read           = models.BooleanField(default=False)
    is_blocked        = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.from_user} -> {self.to_user} on {self.creation_datetime.strftime("%Y/%m/%d %H:%M:%S")}'
