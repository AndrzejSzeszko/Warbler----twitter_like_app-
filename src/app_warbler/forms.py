#!/usr/bin/python3.7

from django import forms
from . import models


class ProfileForm(forms.ModelForm):
    class Meta:
        model  = models.Profile
        fields = '__all__'


class TweetForm(forms.ModelForm):
    class Meta:
        model  = models.Tweet
        fields = '__all__'
