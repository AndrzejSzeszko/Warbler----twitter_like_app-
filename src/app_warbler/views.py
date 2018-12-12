from django.contrib import messages
from django.shortcuts import (
    render,
    redirect
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
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


class UpdateTweetView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model           = models.Tweet
    template_name   = 'app_warbler/update_tweet.html'
    fields          = ['content']

    def test_func(self):
        return self.request.user.id == self.get_object().author.id

    def handle_no_permission(self):
        messages.error(self.request, f'Only author of this post can edit it! Log in as one!')
        return redirect('tweet-details', pk=self.get_object().pk)
