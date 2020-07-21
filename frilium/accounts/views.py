from django.contrib.auth import login as auth_views
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import SignupForm, LoginForm, CustomAuthenticationForm, CustomSetPasswordForm


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password-reset-done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = CustomSetPasswordForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = CustomAuthenticationForm
    authentication_form = LoginForm


custom_login = CustomLoginView.as_view()
password_reset_view = CustomPasswordResetView.as_view()
password_reset_done_view = CustomPasswordResetDoneView.as_view()
password_reset_confirm = CustomPasswordResetConfirmView.as_view()


def signup(request, backend='accounts.backends.EmailAuthBackend'):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_views(request, user, backend)
            return redirect('boards:home')
    else:
        form = SignupForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)
