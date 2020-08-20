from django.urls import path

from ...user.admin.views import create_user, delete_user, edit_user, list_users

app_name = 'user'
urlpatterns = [
    path('', list_users, name='user-list'),
    path('<int:pk>/edit/', edit_user, name='edit'),
    path('new/', create_user, name='new-user'),
    path('u/<int:pk>/delete/', delete_user, name='user-delete')
]
