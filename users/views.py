from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, TemplateView

User = get_user_model()


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'users/user_profile.html'
    login_url = 'account_login'


class ProfileTemplateView(TemplateView):
    template_name = 'users/profile.html'


def all_user_posts(request, username, pk):
    user = get_object_or_404(User, username=username, pk=pk)
    posts = user.all_posts()
    context = {'posts': posts}
    return render(request, 'users/all_posts.html', context)
