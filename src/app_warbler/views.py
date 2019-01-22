from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.shortcuts import (
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
    success_url   = reverse_lazy('login')


class DeleteUserView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model         = User
    template_name = 'app_warbler/delete_user.html'
    success_url   = reverse_lazy('create-user-sign-in')

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        messages.error(self.request, 'Only the owner of the following profile can delete it! Log in as one!')
        return redirect('profile-details', pk=self.get_object().pk)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        rsp = super().delete(request, *args, **kwargs)
        messages.success(request, f'Profile {obj} has been successfully deleted.')
        return rsp


class UpdateUserAndProfileView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model         = User
    template_name = 'app_warbler/update_user_and_profile.html'
    form_class    = forms.UserAndProfileUpdateForm

    def get_queryset(self):
        return self.model.objects.filter(profile__is_blocked=False)

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.get_object().profile.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(instance={
            'user': self.object,
            'profile': self.object.profile
        })
        return kwargs

    def test_func(self):
        return self.get_object() == self.request.user


class ListAllTweetsView(LoginRequiredMixin, generic.ListView):
    model         = models.Tweet
    template_name = 'app_warbler/all_tweets.html'
    paginate_by   = 10
    ordering      = ['-update_datetime']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_blocked=False)


class TweetDetailsView(LoginRequiredMixin, generic.DetailView):
    model         = models.Tweet
    template_name = 'app_warbler/tweet_details.html'
    form_class    = forms.CommentForm

    def get_success_url(self):
        return reverse('tweet-details', kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        ctx                 = super().get_context_data(**kwargs)
        ctx['comments']     = self.get_object().comment_set.all().order_by('creation_datetime')
        ctx['comment_form'] = self.form_class()
        return ctx

    def get_queryset(self):
        return self.model.objects.filter(pk=self.kwargs.get('pk'), is_blocked=False)

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            form.instance.author = self.request.user
            form.instance.tweet  = self.get_object()
            form.save()
            messages.success(self.request, 'Your comment has been successfully posted.')
        else:
            messages.error(self.request, 'We were unable to post your comment.')
        return redirect(self.get_success_url())


class CreateTweetView(LoginRequiredMixin, generic.CreateView):
    model         = models.Tweet
    template_name = 'app_warbler/create_tweet.html'
    fields        = ['tweet_content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTweetView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model         = models.Tweet
    template_name = 'app_warbler/update_tweet.html'
    fields        = ['tweet_content']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_blocked=False)

    def test_func(self):
        return self.request.user.id == self.get_object().author.id

    def handle_no_permission(self):
        messages.error(self.request, 'Only the author of the following post can edit it! Log in as one!')
        return redirect('tweet-details', pk=self.get_object().pk)


class DeleteTweetView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model         = models.Tweet
    template_name = 'app_warbler/delete_tweet.html'

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.get_object().author.id})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_blocked=False)

    def test_func(self):
        return self.request.user.id == self.get_object().author.id

    def handle_no_permission(self):
        messages.error(self.request, 'Only the author of the following post can delete it! Log in as one!')
        return redirect('tweet-details', pk=self.get_object().pk)


class ProfileDetailsView(LoginRequiredMixin, generic.DetailView):
    model         = models.Profile
    template_name = 'app_warbler/profile_details.html'

    def get_context_data(self, **kwargs):
        ctx           = super().get_context_data(**kwargs)
        ctx['tweets'] = self.object.user.tweet_set.all().order_by('-update_datetime')
        return ctx


class CreateMessageView(LoginRequiredMixin, generic.CreateView):
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


class ListUserMessagesView(LoginRequiredMixin, generic.ListView):
    model         = models.Message
    template_name = 'app_warbler/user_messages.html'
    paginate_by   = 10
    ordering      = ['-creation_datetime']

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(is_blocked=False),
            Q(from_user=self.request.user) | Q(to_user=self.request.user)
        )


class MessageDetailsView(LoginRequiredMixin, generic.DetailView):
    model         = models.Message
    template_name = 'app_warbler/message_details.html'

    def get_queryset(self):
        return self.model.objects.filter(pk=self.kwargs.get('pk'), is_blocked=False)

    def get(self, request, *args, **kwargs):
        self.get_queryset().update(is_read=True)
        return super().get(self.request)


class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
        model         = models.Comment
        template_name = 'app_warbler/delete_comment.html'

        def get_success_url(self):
            return reverse_lazy('tweet-details', kwargs={'pk': self.get_object().tweet.id})

        def get_queryset(self):
            queryset = super().get_queryset()
            return queryset.filter(is_blocked=False)

        def test_func(self):
            return self.request.user.id == self.get_object().author.id

        def handle_no_permission(self):
            messages.error(self.request, 'Only the author of that comment can delete it! Log in as one!')
            return redirect('tweet-details', pk=self.get_object().tweet.pk)
