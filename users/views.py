from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
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
