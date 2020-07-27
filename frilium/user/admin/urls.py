from django.urls import path

from frilium.user.admin.views import user_list, edit, create_user

app_name = 'user'
urlpatterns = [
    path('', user_list, name='user-list'),
    path('<int:pk>/edit/', edit, name='edit'),
    path('new/', create_user, name='new-user')
]
