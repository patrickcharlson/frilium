from django.contrib.auth import login as auth_views
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from .forms import SignupForm, LoginForm, CustomAuthenticationForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = CustomAuthenticationForm
    authentication_form = LoginForm


custom_login = CustomLoginView.as_view()


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
