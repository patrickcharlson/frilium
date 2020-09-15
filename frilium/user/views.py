from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CustomPasswordChangeForm, EmailChangeForm, UserForm
from ..post.models import Post
from ..thread.models import Topic
from ..thread.private.models import TopicPrivate

User = get_user_model()

private_topics = TopicPrivate.objects.all()


@login_required
def user_posts(request, username, pk):
    user = get_object_or_404(User, username=username, pk=pk)
    posts = Post.objects.exclude(topic__private_topics__in=private_topics).select_related().filter(user=user).order_by(
        '-created_at')
    context = {'posts': posts, 'user_p': user}
    return render(request, 'frilium/user/all_posts.html', context)


@login_required
def user_topics(request, username, pk):
    user = get_object_or_404(User, username=username, pk=pk)
    topics = Topic.objects.exclude(private_topics__in=private_topics).select_related().filter(user=user).order_by(
        '-date_created')
    context = {'topics': topics, 'user_p': user}
    return render(request, 'frilium/user/all_topics.html', context)


@login_required
def password_change(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.info(request, 'Your password has been changed')
            return redirect(reverse('frilium:user:password-change'))
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'frilium/user/password_change.html', context)


@login_required
def email_change(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your email has been changed!')
            return redirect(reverse('frilium:user:email-change'))
    else:
        form = EmailChangeForm(request.user)
    context = {'form': form}
    return render(request, 'frilium/user/email_change.html', context)


@login_required
def update(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('frilium:user:edit-user')
    else:
        form = UserForm(instance=request.user)
    context = {'form': form}
    return render(request, 'frilium/user/edit-details.html', context)


@login_required
def user_details(request, username, pk):
    user = get_object_or_404(User, username=username, pk=pk)
    context = {'user_p': user}
    return render(request, 'frilium/user/details.html', context)
