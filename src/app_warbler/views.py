from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from . import (
    models,
    forms
)


class ListAllTweetsView(generic.ListView):
    model         = models.Tweet
    template_name = 'app_warbler/all_tweets.html'
    paginate_by   = 10
    ordering      = ['-update_datetime']


class TweetDetailsView(generic.DetailView):
    model         = models.Tweet
    template_name = 'app_warbler/tweet_details.html'


class CreateTweetView(LoginRequiredMixin, generic.CreateView):
    model         = models.Tweet
    template_name = 'app_warbler/create_tweet.html'
    fields        = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

