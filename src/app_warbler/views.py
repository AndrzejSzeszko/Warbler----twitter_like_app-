from django.shortcuts import render
from django.views import generic
from . import models


class ListAllTweetsView(generic.ListView):
    model = models.Tweet
    template_name = 'app_warbler/all_tweets.html'
    paginate_by = 10
