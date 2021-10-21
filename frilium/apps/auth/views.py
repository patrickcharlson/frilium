from django import http
from django.conf import settings
from django.contrib.auth import login as auth_views
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from . import signals
from .forms import SignupForm, LoginForm, CustomAuthenticationForm, CustomSetPasswordForm, RegistrationForm, SignInForm


class CustomPasswordResetView(PasswordResetView):
    template_name = 'frilium/auth/password_reset.html'
    email_template_name = 'frilium/auth/password_reset_email.html'
    subject_template_name = 'frilium/auth/password_reset_subject.txt'
    success_url = reverse_lazy('frilium:auth:password-reset-done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'frilium/auth/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'frilium/auth/password_reset_confirm.html'
    form_class = CustomSetPasswordForm


class CustomLoginView(LoginView):
    template_name = 'frilium/auth/login.html'
    form_class = CustomAuthenticationForm
    authentication_form = LoginForm


custom_login = CustomLoginView.as_view()
password_reset_view = CustomPasswordResetView.as_view()
password_reset_done_view = CustomPasswordResetDoneView.as_view()
password_reset_confirm = CustomPasswordResetConfirmView.as_view()


def signup(request, backend='auth.backends.EmailAuthBackend'):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_views(request, user, backend)
            return redirect(settings.LOGIN_URL)
    else:
        form = SignupForm()
    context = {'form': form}
    return render(request, 'frilium/auth/signup.html', context)


class AccountAuthView(generic.TemplateView):
    template_name = 'frilium/auth/login.html'
    login_prefix, registration_prefix = 'login', 'registration'
    login_form_class = SignInForm
    registration_form_class = RegistrationForm
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'login_form' not in kwargs:
            context['login_form'] = self.get_login_form()
        if 'registration_form' not in kwargs:
            context['registration_form'] = self.get_registration_form()
        return context

    def post(self, request, *args, **kwargs):
        if 'login_submit' in request.POST:
            return self.validate_login_form()
        elif 'registration_submit' in request.POST:
            return self.validate_registration_form()
        return http.HttpResponseBadRequest()

    # LOGIN

    def get_login_form(self, bind_data=False):
        return self.login_form_class(
            **self.get_login_form_kwargs(bind_data))

    def get_login_form_kwargs(self, bind_data=False):
        kwargs = {
            'request': self.request,
            'host': self.request.get_host(),
            'prefix': self.login_prefix,
            'initial': {
                'redirect_url': self.request.GET.get(self.redirect_field_name, '')
            }}

        if bind_data and self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def validate_login_form(self):
        form = self.get_login_form(bind_data=True)
        if form.is_valid():
            user = form.get_user()

            old_session_key = self.request.session.session_key

            auth_views(self.request, form.get_user())

            signals.user_logged_in.send_robust(
                sender=self, request=self.request, user=user, old_session_key=old_session_key
            )
            return redirect(settings.LOGIN_REDIRECT_URL)

        context = self.get_context_data(login_form=form)
        return self.render_to_response(context)

    # REGISTRATION
    def get_registration_form(self, bind_data=False):
        return self.registration_form_class(**self.get_registration_form_kwargs(bind_data))

    def get_registration_form_kwargs(self, bind_data=False):
        kwargs = {
            'host': self.request.get_host(),
            'prefix': self.registration_prefix,
            'initial': {
                'redirect_url': self.request.GET.get(self.redirect_field_name, '')
            }
        }
        if bind_data and self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES
            })
        return kwargs

    def validate_registration_form(self):
        form = self.get_registration_form(bind_data=True)
        if form.is_valid():
            user = form.save()
            auth_views(self.request, user)
            return redirect(settings.LOGIN_URL)

        context = self.get_context_data(registration_form=form)
        return self.render_to_response(context)


login_register = AccountAuthView.as_view()
