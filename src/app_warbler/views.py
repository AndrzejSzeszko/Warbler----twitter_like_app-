from django.contrib.auth.models import User
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


class CreateUserView(generic.CreateView):
    model         = User
    template_name = 'app_warbler/create_user.html'
    form_class    = forms.CreateUserForm
    success_url   = 'login'


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
        messages.error(self.request, 'Only the author of the following post can edit it! Log in as one!')
        return redirect('tweet-details', pk=self.get_object().pk)


class ProfileDetailsView(generic.DetailView):
    model         = models.Profile
    template_name = 'app_warbler/profile_details.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tweets'] = self.object.user.tweet_set.all().order_by('-update_datetime')
        return ctx
