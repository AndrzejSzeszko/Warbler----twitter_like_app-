from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import (
    render,
    redirect,
    reverse
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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comments'] = self.get_object().comment_set.all().order_by('creation_datetime')
        return ctx


class CreateTweetView(LoginRequiredMixin, generic.CreateView):
    model         = models.Tweet
    template_name = 'app_warbler/create_tweet.html'
    fields        = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTweetView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model         = models.Tweet
    template_name = 'app_warbler/update_tweet.html'
    fields        = ['content']

    def test_func(self):
        return self.request.user.id == self.get_object().author.id

    def handle_no_permission(self):
        messages.error(self.request, 'Only the author of the following post can edit it! Log in as one!')
        return redirect('tweet-details', pk=self.get_object().pk)


class ProfileDetailsView(generic.DetailView):
    model         = models.Profile
    template_name = 'app_warbler/profile_details.html'

    def get_context_data(self, **kwargs):
        ctx           = super().get_context_data(**kwargs)
        ctx['tweets'] = self.object.user.tweet_set.all().order_by('-update_datetime')
        return ctx


class CreateMessageView(generic.CreateView):
    model         = models.Message
    template_name = 'app_warbler/create_message.html'
    form_class    = forms.MessageForm
    pk_url_kwarg  = 'to_user'

    def get_context_data(self, **kwargs):
        ctx            = super().get_context_data(**kwargs)
        ctx['to_user'] = User.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
        return ctx

    def get_success_url(self):
        return reverse('user-messages', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        form.instance.from_user = self.request.user
        form.instance.to_user   = self.get_context_data()['to_user']
        rsp                     = super().form_valid(form)
        messages.success(self.request, f'Message to {form.instance.to_user} successfully sent.')
        return rsp


class ListUserMessagesView(generic.ListView):
    model         = models.Message
    template_name = 'app_warbler/user_messages.html'
    paginate_by   = 10
    ordering      = ['-creation_datetime']

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(from_user=self.request.user) |
            Q(to_user=self.request.user)
        )


class MessageDetailsView(generic.DetailView):
    model         = models.Message
    template_name = 'app_warbler/message_details.html'

    def get_queryset(self):
        return self.model.objects.filter(pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        self.get_queryset().update(is_read=True)
        return super().get(self.request)
