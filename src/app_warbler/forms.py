#!/usr/bin/python3.7
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from . import models


class CreateUserForm(UserCreationForm):
    class Meta:
        model  = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model  = models.Profile
        fields = '__all__'


class TweetForm(forms.ModelForm):
    class Meta:
        model  = models.Tweet
        fields = '__all__'
