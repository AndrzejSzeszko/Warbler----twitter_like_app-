from django.contrib import admin
from .models import (
    Profile,
    Comment,
    Tweet,
    Message
)


def block_object(model_admin, request, queryset):
    queryset.update(is_blocked=True)


block_object.short_description = 'Block selected objects'


def comment_abstract(comment_obj):
    return f'{comment_obj.comment_content[:10]}...'


def tweet_abstract(tweet_obj):
    return f'{tweet_obj.tweet_content[:10]}...'


def message_abstract(message_obj):
    return f'{message_obj.message_content[:10]}...'


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'about_myself'
    ]
    actions = [block_object]


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'author',
        'tweet',
        comment_abstract,
        'creation_datetime',
        'is_blocked'
    ]
    actions = [block_object]


class TweetAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'author',
        tweet_abstract,
        'creation_datetime',
        'update_datetime',
        'is_blocked'
    ]
    actions = [block_object]


class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'from_user',
        'to_user',
        message_abstract,
        'creation_datetime',
        'is_read',
        'is_blocked'
    ]
    actions = [block_object]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tweet, TweetAdmin)
admin.site.register(Message, MessageAdmin)
