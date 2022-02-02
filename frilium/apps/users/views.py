from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from .forms import CustomPasswordChangeForm, EmailChangeForm, UserForm
from ..posts.models import Post
from ..topics.models import Topic
from ..topics.private.models import TopicPrivate

User = get_user_model()

private_topics = TopicPrivate.objects.all()


class UserPostsView(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        posts = Post.objects.exclude(topic__private_topics__in=private_topics).select_related('topic').filter(
            user=user).order_by('-created_at')
        context = {'posts': posts,
                   'user_p': user}
        return render(request, 'frilium/users/all_posts.html', context)


def user_topics(request, username):
    user = get_object_or_404(User, username=username)
    topics = (Topic.objects
              .exclude(private_topics__in=private_topics)
              .select_related().filter(user=user)
              .order_by('-date_created')
              .annotate(replies=Count('posts') - 1))
    context = {'topics': topics, 'user_p': user}
    return render(request, 'frilium/users/all_topics.html', context)


@login_required
def password_change(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.info(request, 'Your password has been changed')
            return redirect(reverse('frilium:users:password-change'))
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {'form': form, 'user_p': user}
    return render(request, 'frilium/users/password_change.html', context)


@login_required
def email_change(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = EmailChangeForm(request.POST or None, request.user)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your email has been changed!')
            return redirect(reverse('frilium:users:email-change'))
    else:
        form = EmailChangeForm(request.user)
    context = {'form': form, 'user_p': user}
    return render(request, 'frilium/users/email_change.html', context)


@login_required
def update(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = UserForm(request.POST or None, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('frilium:users:edit-users', user.username)
    else:
        form = UserForm(instance=request.user)
    context = {'form': form, 'user_p': user}
    return render(request, 'frilium/users/edit-details.html', context)


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {'user_p': user}
    return render(request, 'frilium/users/user_profile.html', context)


user_posts = UserPostsView.as_view()
