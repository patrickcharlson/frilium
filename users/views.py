from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView

from boards.models import Post, Topic
from users.forms import CustomPasswordChangeForm, EmailChangeForm, UserForm

User = get_user_model()


class UserPosts(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'users/all_posts.html'
    login_url = settings.LOGIN_URL

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        queryset = Post.objects.select_related().filter(created_by=user).order_by('-created_at')
        return queryset


class UserTopics(LoginRequiredMixin, ListView):
    model = Topic
    context_object_name = 'topics'
    paginate_by = 5
    template_name = 'users/all_topics.html'
    login_url = settings.LOGIN_URL

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        queryset = Topic.objects.select_related().filter(created_by=user).order_by('-date_created')
        return queryset


@login_required
def password_change(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.info(request, 'Your password has been changed')
            return redirect(reverse('users:password-change'))
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'users/password_change.html', context)


@login_required
def email_change(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your email has been changed!')
            return redirect(reverse('users:email-change'))
    else:
        form = EmailChangeForm(request.user)
    context = {'form': form}
    return render(request, 'users/profile_email_change.html', context)


@login_required
def update(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('users:edit-user')
    else:
        form = UserForm(instance=request.user)
    context = {'form': form}
    return render(request, 'users/edit-details.html', context)


def user_details(request, username, pk):
    user = get_object_or_404(User, username=username, pk=pk)
    context = {'user': user}
    return render(request, 'users/details.html', context)
