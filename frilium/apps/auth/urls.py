from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = 'auth'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', views.custom_login, name='login'),
    path('forgotten-password/', views.password_reset_view, name='password-reset'),
    path('password-reset/done', views.password_reset_done_view, name='password-reset-done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password-reset-confirm')
]
