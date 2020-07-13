from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import signup, custom_login, password_reset_view, password_reset_done_view, \
    password_reset_confirm

app_name = 'accounts'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', custom_login, name='login'),
    path('forgotten-password/', password_reset_view, name='password-reset'),
    path('password-reset/done', password_reset_done_view, name='password-reset-done'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password-reset-confirm')
]
