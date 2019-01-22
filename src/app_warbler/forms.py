#!/usr/bin/python3.7
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from . import models
from betterforms.multiform import MultiModelForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model  = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileForm(forms.ModelForm):
    class Meta:
        model  = models.Profile
        fields = ['photo', 'about_myself']


class UserAndProfileUpdateForm(MultiModelForm):
    form_classes = {
        'user': UpdateUserForm,
        'profile': ProfileForm
    }


class TweetForm(forms.ModelForm):
    class Meta:
        model  = models.Tweet
        fields = '__all__'


class MessageForm(forms.ModelForm):
    class Meta:
        model  = models.Message
        fields = ['message_content']


class CommentForm(forms.ModelForm):
    class Meta:
        model  = models.Comment
        fields = ['comment_content']
