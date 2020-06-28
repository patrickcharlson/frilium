from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView, ListView

from boards.models import Post, Topic

User = get_user_model()


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'users/user_profile.html'
    login_url = 'account_login'


class ProfileTemplateView(TemplateView):
    template_name = 'users/profile.html'


class UserPosts(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'users/all_posts.html'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        queryset = Post.objects.filter(created_by=user).order_by('-created_at')
        return queryset


class UserTopics(ListView):
    model = Topic
    context_object_name = 'topics'
    paginate_by = 5
    template_name = 'users/all_topics.html'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        queryset = Topic.objects.filter(created_by=user).order_by('-date_created')
        return queryset
