from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import signup, custom_login

app_name = 'accounts'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', custom_login, name='login')
]
